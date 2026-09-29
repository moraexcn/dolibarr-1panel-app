# Dolibarr Local App for 1Panel

[简体中文](README.md) | [English](README_en.md)

This project builds a Dolibarr app package for 1Panel using [1Panel](https://github.com/1Panel-dev/1Panel)'s local app mechanism, the package conventions in 1Panel's official [Appstore Skills](https://github.com/1Panel-dev/1Panel-appstore-skills), and [Dolibarr](https://github.com/Dolibarr/dolibarr)'s [official Docker deployment](https://github.com/Dolibarr/dolibarr-docker).

The app directory is [`apps/dolibarr`](apps/dolibarr). The **current repository** contains version directories for `23.0.3` and `23.0.4`; these are the versions packaged today, not a limit on future releases. Available install versions are determined by the version configurations in the app directory. [`apps/dolibarr.zip`](apps/dolibarr.zip) is an archive of the current app directory.

## Before installation

- Install and sign in to 1Panel on a Linux server, and confirm Docker is running.
- Install a MySQL or MariaDB database service through 1Panel and confirm it is running. You will select that service in the Dolibarr installation form.
- Decide how users will access Dolibarr: through the server address and port, or through an already configured domain and reverse proxy. Choose an unused Web UI port.

## Import and install

1. Download [`apps/dolibarr.zip`](apps/dolibarr.zip) from this repository and upload it to the server running 1Panel. The archive already has a top-level `dolibarr/` directory.
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

The current package supports an update from `23.0.3` to `23.0.4` within the same major version and disables automatic cross-major updates. New versions must be packaged and tested separately against 1Panel's app format and Dolibarr's database migration requirements. Before upgrading an existing instance, read the [upgrade, backup, and verification guide](apps/dolibarr/UPGRADE.md). Back up and restore the database, documents, and custom modules together. The detailed upgrade guide is currently in Chinese.

## Repository contents

| Path | Purpose |
| --- | --- |
| [`apps/dolibarr`](apps/dolibarr) | 1Panel local app directory and current version configurations |
| [`apps/dolibarr.zip`](apps/dolibarr.zip) | Archive of the current app directory |
| [`specs/dolibarr.json`](specs/dolibarr.json) | Source specification for the package |

Instance data and credentials are provided by 1Panel at installation time and are not stored in this repository.
