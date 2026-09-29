# Dolibarr Local App for 1Panel

[简体中文](README.md) | [English](README_en.md)

This project builds a Dolibarr app package for 1Panel using [1Panel](https://github.com/1Panel-dev/1Panel)'s local app mechanism, the package conventions in 1Panel's official [Appstore Skills](https://github.com/1Panel-dev/1Panel-appstore-skills), and [Dolibarr](https://github.com/Dolibarr/dolibarr)'s [official Docker deployment](https://github.com/Dolibarr/dolibarr-docker).

To install a specific version, choose the corresponding entry in [Releases](https://github.com/moraexcn/dolibarr-1panel-app/releases) and download its `dolibarr.zip` asset. The repository's [`apps/dolibarr`](apps/dolibarr) directory generally tracks the latest package content and is not a substitute for historical Release assets.

## Before installation

- Install and sign in to 1Panel on a Linux server, and confirm Docker is running.
- Install a MySQL or MariaDB database service through 1Panel and confirm it is running. You will select that service in the Dolibarr installation form.
- Decide how users will access Dolibarr: through the server address and port, or through an already configured domain and reverse proxy. Choose an unused Web UI port.

## Import and install

1. Open this project's [Releases](https://github.com/moraexcn/dolibarr-1panel-app/releases), choose the version you want, download its `dolibarr.zip` asset, and upload it to the server running 1Panel. Download the Release asset, not GitHub's automatically generated Source code ZIP. The app archive already has a top-level `dolibarr/` directory.
2. Extract it into the 1Panel local app directory. This example uses the default installation path; replace it if 1Panel is installed elsewhere:

   ```bash
   sudo mkdir -p /opt/1panel/resource/apps/local
   sudo unzip dolibarr.zip -d /opt/1panel/resource/apps/local
   ```

   After extraction, `/opt/1panel/resource/apps/local/dolibarr/data.yml` and the complete version directories should exist. Alternatively, copy the entire `apps/dolibarr` directory from a repository checkout to that location.
3. In 1Panel, open **App Store → Local Apps**, refresh the app list, find **Dolibarr**, and click **Install**.
4. Select the version and MySQL/MariaDB service. Enter the database name, user, and password; Dolibarr administrator username and password; company information; cron security key; and instance secret. Use separately generated random values for the security keys and store them safely.
5. Set **Base URL** to the full address users will actually use, including `http://` or `https://` and a port if needed. Set an unused **Web UI port**. Review the timezone, PHP upload limits, and demo data setting as needed. For a new database, the form defaults to `utf8mb4` and `utf8mb4_unicode_ci`; this does not alter an existing database.
6. Review 1Panel's advanced settings, including port exposure, and click **Confirm**. Wait for the installation log to complete. Check that the app and containers are running in **Installed Apps**, open the Base URL, and sign in with the administrator account you set.

See the [official 1Panel Appstore Skills guide](https://1panel.cn/docs/v2/dev_manual/appstore_skills/) for the local app directory and entry point, and the [1Panel installation guide](https://1panel.cn/docs/v2/user_manual/appstore/install/) for the form and confirmation flow. See [`apps/dolibarr/README_en.md`](apps/dolibarr/README_en.md) for the app overview and features.

## Upgrading

The package disables automatic cross-major updates. New versions must be packaged and tested separately against 1Panel's app format and Dolibarr's database migration requirements. Before upgrading an existing instance, read the [upgrade, backup, and verification guide](apps/dolibarr/UPGRADE.md). Back up and restore the database, documents, and custom modules together. Upgrade installed instances through 1Panel's upgrade flow; replacing the local app directory or image alone does not upgrade an instance. The detailed upgrade guide is currently in Chinese.

## Scheduled sync of the latest Release

[`scripts/sync_latest_release.py`](scripts/sync_latest_release.py) downloads the `dolibarr.zip` asset from the latest **published, non-prerelease** GitHub Release, verifies GitHub's SHA-256 digest and the ZIP layout, and syncs it into 1Panel's local app directory. It preserves older version definitions absent from the new archive and skips a Release already synced. It **only updates the app catalog; it does not upgrade installed instances or migrate the database**. After syncing, refresh **App Store → Local Apps** in 1Panel and follow the upgrade guide before upgrading manually.

Download the script to a fixed location on the 1Panel server, such as `/opt/dolibarr-1panel-app/sync_latest_release.py`. The server needs Python 3 and access to the GitHub API and Release assets. You can run:

```bash
sudo mkdir -p /opt/dolibarr-1panel-app
sudo curl -fL https://raw.githubusercontent.com/moraexcn/dolibarr-1panel-app/main/scripts/sync_latest_release.py -o /opt/dolibarr-1panel-app/sync_latest_release.py
python3 /opt/dolibarr-1panel-app/sync_latest_release.py --dry-run
```

Confirm that the dry run downloads and validates the latest package before creating the scheduled job.

Then, in 1Panel, go to **Cron Jobs → Create Cron Job**, select **Shell script**, and run it on the host (do not enable execution inside a container). Ensure the job can write to the local app directory. Set a schedule, for example `0 3 * * *` for 3 a.m. daily. Use this script content:

```bash
python3 /opt/dolibarr-1panel-app/sync_latest_release.py
```

If 1Panel uses a non-default installation path, append `--appstore-dir /actual/path/resource/apps/local`. When there is no published Release, the script reports that and leaves the local app unchanged. A missing `dolibarr.zip` asset or failed validation makes the job fail. Each published package must include an asset named `dolibarr.zip`; GitHub's automatic source archives are not app packages. See the [1Panel cron job guide](https://1panel.cn/docs/v2/user_manual/cronjobs/).

## Repository contents

| Path | Purpose |
| --- | --- |
| [`apps/dolibarr`](apps/dolibarr) | 1Panel local app directory and current version configurations |
| [`apps/dolibarr.zip`](apps/dolibarr.zip) | Archive of the current repository directory; use Releases for a specific version |
| [`scripts/sync_latest_release.py`](scripts/sync_latest_release.py) | Script for scheduled sync of the latest published Release |
| [`specs/dolibarr.json`](specs/dolibarr.json) | Source specification for the package |

Instance data and credentials are provided by 1Panel at installation time and are not stored in this repository.
