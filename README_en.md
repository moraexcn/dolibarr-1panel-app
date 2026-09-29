# Dolibarr Local App for 1Panel

[简体中文](README.md) | [English](README_en.md)

This repository provides a Dolibarr local app package for 1Panel. The app directory is [`apps/dolibarr`](apps/dolibarr) and includes versions `23.0.3` and `23.0.4`. [`apps/dolibarr.zip`](apps/dolibarr.zip) contains the same app directory.

## Installation

1. Copy the entire `apps/dolibarr` directory to your 1Panel local app directory, for example `/opt/1panel/resource/apps/local/dolibarr`. Use the actual local app path if 1Panel is installed elsewhere.
2. Refresh **App Store → Local Apps** in 1Panel, then select Dolibarr to install it.
3. Enter the database service, administrator account, actual access URL, and other installation settings. For a new MySQL/MariaDB database, the form defaults to the `utf8mb4` character set and `utf8mb4_unicode_ci` collation. This does not change an existing database.

See [`apps/dolibarr/README_en.md`](apps/dolibarr/README_en.md) for the app overview and features.

## Upgrading

The package retains `23.0.3` and offers `23.0.4` as an update within the same major version. Automatic cross-major updates are disabled. Before upgrading an existing instance, read the [upgrade, backup, and verification guide](apps/dolibarr/UPGRADE.md). Back up and restore the database, documents, and custom modules together; do not update only the image tag. The detailed upgrade guide is currently in Chinese.

## Repository contents

| Path | Purpose |
| --- | --- |
| [`apps/dolibarr`](apps/dolibarr) | 1Panel local app directory and version configuration |
| [`apps/dolibarr.zip`](apps/dolibarr.zip) | Ready-to-copy archive of the app directory |
| [`specs/dolibarr.json`](specs/dolibarr.json) | Source specification for the package |

Instance data and credentials are provided by 1Panel at installation time and are not stored in this repository.
