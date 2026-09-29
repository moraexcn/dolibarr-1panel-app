#!/usr/bin/env python3
"""Sync the latest published Dolibarr Release into 1Panel's local app catalog.

This updates app definitions only. It never upgrades an installed instance.
The Release must contain an asset named ``dolibarr.zip`` with a SHA-256 digest.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile


REPOSITORY = "moraexcn/dolibarr-1panel-app"
RELEASE_API = f"https://api.github.com/repos/{REPOSITORY}/releases/latest"
ASSET_NAME = "dolibarr.zip"
DEFAULT_APPSTORE_DIR = Path("/opt/1panel/resource/apps/local")
MAX_ARCHIVE_SIZE = 50 * 1024 * 1024
MAX_UNCOMPRESSED_SIZE = 100 * 1024 * 1024
USER_AGENT = "dolibarr-1panel-release-sync"


class SyncError(Exception):
    """An expected release or package validation failure."""


def request(url: str):
    return Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )


def latest_release() -> dict | None:
    try:
        with urlopen(request(RELEASE_API), timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            return None
        raise SyncError(f"GitHub Release API returned HTTP {exc.code}") from exc
    except (URLError, ValueError) as exc:
        raise SyncError(f"Could not read GitHub Release API: {exc}") from exc


def release_asset(release: dict) -> tuple[str, str, str]:
    tag = release.get("tag_name")
    if not isinstance(tag, str) or not tag:
        raise SyncError("Latest Release has no tag")

    asset = next(
        (item for item in release.get("assets", []) if item.get("name") == ASSET_NAME),
        None,
    )
    if not asset or asset.get("state") != "uploaded":
        raise SyncError(f"Release {tag} has no uploaded {ASSET_NAME} asset")

    url = asset.get("browser_download_url", "")
    parsed = urlsplit(url)
    expected_prefix = f"/{REPOSITORY}/releases/download/"
    if parsed.scheme != "https" or parsed.netloc != "github.com" or not parsed.path.startswith(expected_prefix):
        raise SyncError("Release asset URL is outside this GitHub repository")

    digest = asset.get("digest", "")
    if not isinstance(digest, str) or not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", digest):
        raise SyncError("Release asset has no usable GitHub SHA-256 digest")
    return tag, url, digest.split(":", 1)[1].lower()


def download_asset(url: str, destination: Path, expected_sha256: str) -> None:
    actual = hashlib.sha256()
    size = 0
    try:
        with urlopen(request(url), timeout=60) as response, destination.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_ARCHIVE_SIZE:
                    raise SyncError("Release archive exceeds the size limit")
                actual.update(chunk)
                output.write(chunk)
    except (HTTPError, URLError) as exc:
        raise SyncError(f"Could not download Release asset: {exc}") from exc
    if actual.hexdigest() != expected_sha256:
        raise SyncError("Release archive SHA-256 does not match GitHub's asset digest")


def validate_archive(archive: Path) -> None:
    try:
        with ZipFile(archive) as bundle:
            names: set[str] = set()
            total_size = 0
            for entry in bundle.infolist():
                name = entry.filename
                path = PurePosixPath(name)
                if (
                    not name.startswith("dolibarr/")
                    or path.is_absolute()
                    or ".." in path.parts
                    or "\\" in name
                    or path.as_posix() != name.rstrip("/")
                    or name in names
                ):
                    raise SyncError(f"Unsafe or duplicate archive path: {name}")
                names.add(name)
                mode = entry.external_attr >> 16
                if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                    raise SyncError(f"Unsupported archive entry type: {name}")
                total_size += entry.file_size
                if total_size > MAX_UNCOMPRESSED_SIZE:
                    raise SyncError("Extracted package exceeds the size limit")
            if not {"dolibarr/data.yml", "dolibarr/logo.png"}.issubset(names):
                raise SyncError("Archive is missing Dolibarr app metadata")
            versions = {
                parts[1]
                for name in names
                if (parts := PurePosixPath(name).parts)
                and len(parts) == 3
                and parts[0] == "dolibarr"
                and parts[2] == "data.yml"
            }
            if not versions or any(f"dolibarr/{version}/docker-compose.yml" not in names for version in versions):
                raise SyncError("Archive has no complete version directory")
    except BadZipFile as exc:
        raise SyncError("Release asset is not a valid ZIP archive") from exc


def check_no_symlinks(directory: Path) -> None:
    if directory.is_symlink() or any(path.is_symlink() for path in directory.rglob("*")):
        raise SyncError("Existing local app directory contains a symlink")


def apply_package(archive: Path, appstore_dir: Path, tag: str, temporary: Path) -> None:
    target = appstore_dir / "dolibarr"
    incoming_root = temporary / "incoming"
    with ZipFile(archive) as bundle:
        bundle.extractall(incoming_root)
    incoming = incoming_root / "dolibarr"
    merged = temporary / "merged"
    shutil.copytree(incoming, merged)

    # Keep older version definitions so 1Panel can still recognize update paths.
    if target.exists():
        if not target.is_dir():
            raise SyncError(f"Local app path is not a directory: {target}")
        check_no_symlinks(target)
        for previous in target.iterdir():
            if (
                previous.is_dir()
                and not (merged / previous.name).exists()
                and (previous / "data.yml").is_file()
                and (previous / "docker-compose.yml").is_file()
            ):
                shutil.copytree(previous, merged / previous.name)

    backup = temporary / "previous"
    moved_existing = False
    if target.exists():
        os.replace(target, backup)
        moved_existing = True
    try:
        os.replace(merged, target)
    except OSError:
        if moved_existing:
            os.replace(backup, target)
        raise

    state_file = appstore_dir / ".dolibarr-release-tag"
    state_temporary = temporary / "release-tag"
    state_temporary.write_text(tag + "\n", encoding="utf-8")
    os.replace(state_temporary, state_file)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--appstore-dir", type=Path, default=DEFAULT_APPSTORE_DIR,
        help="1Panel local app directory (default: %(default)s)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Download and validate without installing")
    parser.add_argument("--force", action="store_true", help="Re-sync an already recorded Release")
    args = parser.parse_args()

    try:
        appstore_dir = args.appstore_dir
        if not appstore_dir.is_dir():
            raise SyncError(f"1Panel local app directory does not exist: {appstore_dir}")
        with (appstore_dir / ".dolibarr-release-sync.lock").open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            release = latest_release()
            if release is None:
                print("No published GitHub Release yet; local app was not changed.")
                return 0
            tag, url, digest = release_asset(release)
            state_file = appstore_dir / ".dolibarr-release-tag"
            current = state_file.read_text(encoding="utf-8").strip() if state_file.exists() else None
            if current == tag and (appstore_dir / "dolibarr").is_dir() and not args.force and not args.dry_run:
                print(f"Release {tag} is already synced; local app was not changed.")
                return 0
            with tempfile.TemporaryDirectory(prefix=".dolibarr-release-", dir=appstore_dir) as work:
                temporary = Path(work)
                archive = temporary / ASSET_NAME
                download_asset(url, archive, digest)
                validate_archive(archive)
                if args.dry_run:
                    print(f"Release {tag}: asset digest and package structure verified; dry run only.")
                    return 0
                apply_package(archive, appstore_dir, tag, temporary)
            print(f"Synced Release {tag}. Refresh 1Panel Local Apps; upgrade installed instances manually.")
            return 0
    except (OSError, SyncError) as exc:
        print(f"Release sync failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
