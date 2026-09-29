# Dolibarr for 1Panel

This repository contains the Dolibarr local app package for 1Panel.

The Dolibarr package is in [`apps/dolibarr`](apps/dolibarr), with versions `23.0.3` and `23.0.4`. For a 1Panel installation, copy the entire `dolibarr` directory to `/opt/1panel/resource/apps/local/dolibarr` and refresh the local app list. The ready-to-copy archive is [`apps/dolibarr.zip`](apps/dolibarr.zip).

Read [`apps/dolibarr/UPGRADE.md`](apps/dolibarr/UPGRADE.md) before updating an existing installation. The package supports 23.0.3 to 23.0.4 updates; cross-major updates are disabled.

`specs/dolibarr.json` records the package source specification. Application data and credentials are supplied by 1Panel at installation time and are not stored here.
