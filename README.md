# Dolibarr 1Panel 本地应用

[简体中文](README.md) | [English](README_en.md)

本项目基于 [1Panel](https://github.com/1Panel-dev/1Panel) 的本地应用机制、1Panel 官方 [Appstore Skills](https://github.com/1Panel-dev/1Panel-appstore-skills) 的应用包规范，以及 [Dolibarr](https://github.com/Dolibarr/dolibarr) 的[官方 Docker 部署方案](https://github.com/Dolibarr/dolibarr-docker)制作，提供可导入 1Panel 的 Dolibarr 应用包。

需要安装指定版本时，请到 [Releases](https://github.com/moraexcn/dolibarr-1panel-app/releases) 选择对应的发布版本，下载其中的 `dolibarr.zip` 附件。仓库中的 [`apps/dolibarr`](apps/dolibarr) 目录一般保持最新的应用包内容，不能代替历史版本的 Release 附件。

## 安装前准备

- 在 Linux 服务器上安装并登录 1Panel，确认 Docker 服务可用。
- 先通过 1Panel 安装一个 MySQL 或 MariaDB 数据库服务，并确认其运行正常。安装 Dolibarr 时需要在表单中选择该服务。
- 确定访问方式：直接通过服务器地址和端口访问，或使用已配置好的域名及反向代理。准备一个未占用的 Web UI 端口。

## 导入并安装

1. 前往本项目的 [Releases](https://github.com/moraexcn/dolibarr-1panel-app/releases)，选择要安装的发布版本，下载其 `dolibarr.zip` 附件并上传到运行 1Panel 的服务器。请下载发布附件，而不是 GitHub 自动生成的 Source code ZIP；应用包顶层已经包含 `dolibarr/` 目录。
2. 在服务器上将压缩包解压到 1Panel 本地应用目录。默认安装路径的示例如下；若 1Panel 安装在其他位置，请替换目录：

   ```bash
   sudo mkdir -p /opt/1panel/resource/apps/local
   sudo unzip dolibarr.zip -d /opt/1panel/resource/apps/local
   ```

   解压后应存在 `/opt/1panel/resource/apps/local/dolibarr/data.yml`，并保留 `dolibarr` 下的完整版本目录。也可以直接复制仓库中的整个 `apps/dolibarr` 目录到相同位置。
3. 打开 1Panel 的“应用商店 → 本地应用”，刷新应用列表，找到 **Dolibarr** 并点击“安装”。
4. 在安装表单中选择要安装的版本和 MySQL/MariaDB 服务，填写数据库名称、数据库用户及密码；填写 Dolibarr 管理员用户名和密码、公司信息、定时任务安全密钥与实例密钥。安全密钥应使用各自生成的随机值，并妥善保存。
5. 填写 **Base URL** 为用户实际访问 Dolibarr 的完整地址，包括 `http://` 或 `https://` 及必要的端口；设置未占用的 **Web UI 端口**。按需要检查时区、PHP 上传限制及演示数据选项。新建数据库的表单默认使用 `utf8mb4` 和 `utf8mb4_unicode_ci`；该预设不会修改现有数据库。
6. 检查 1Panel 的端口开放等高级选项，点击“确认”，等待安装日志显示完成。进入“已安装”列表确认应用和容器正在运行，然后按所填 Base URL 访问页面，并用刚设置的管理员账号登录。

安装入口与本地目录可参阅 [1Panel Appstore Skills 官方说明](https://1panel.cn/docs/v2/dev_manual/appstore_skills/)；安装表单和确认流程可参阅 [1Panel 应用安装文档](https://1panel.cn/docs/v2/user_manual/appstore/install/)。应用简介与功能见 [`apps/dolibarr/README.md`](apps/dolibarr/README.md)。

## 更新

应用包允许通过 1Panel 的升级入口选择已收录的跨大版本目标；升级仍需由管理员手动执行。更新现有实例前，请阅读[更新、备份与验收说明](apps/dolibarr/UPGRADE.md)，并先在隔离环境验证数据库迁移及自定义模块兼容性；数据库、文档及自定义模块应一起备份和恢复。不能只覆盖本地应用目录或替换镜像来升级已安装实例。

## 定时同步最新 Release

[`scripts/sync_latest_release.py`](scripts/sync_latest_release.py) 可从 GitHub 最新的**正式 Release** 获取 `dolibarr.zip` 附件，核对 GitHub 提供的 SHA-256 摘要与 ZIP 目录结构，再同步到 1Panel 本地应用目录。脚本保留原目录中尚未包含在新包里的旧版本配置，重复运行同一 Release 不会重新覆盖。它**只同步应用商店定义，不会自动升级已安装实例或迁移数据库**；同步后仍需在 1Panel 的“应用商店 → 本地应用”刷新，再按更新说明手动升级。

将脚本下载到 1Panel 服务器上一个固定位置，例如 `/opt/dolibarr-1panel-app/sync_latest_release.py`。服务器需要 Python 3，并能访问 GitHub API 和 Release 附件。可在服务器上执行：

```bash
sudo mkdir -p /opt/dolibarr-1panel-app
sudo curl -fL https://raw.githubusercontent.com/moraexcn/dolibarr-1panel-app/main/scripts/sync_latest_release.py -o /opt/dolibarr-1panel-app/sync_latest_release.py
python3 /opt/dolibarr-1panel-app/sync_latest_release.py --dry-run
```

先确认试运行显示最新发布包可下载且校验通过，再创建计划任务。

然后在 1Panel 的“计划任务 → 创建计划任务”中选择 **Shell 脚本**，在宿主机执行（不要选择容器内执行），确保任务对本地应用目录有写入权限。按需要设置执行周期，例如每天凌晨 3 点使用 `0 3 * * *`。脚本内容为：

```bash
python3 /opt/dolibarr-1panel-app/sync_latest_release.py
```

若 1Panel 安装目录不是默认路径，请在命令末尾加上 `--appstore-dir /实际路径/resource/apps/local`。没有已发布的 Release 时，脚本会提示并保持本地应用不变；Release 缺少 `dolibarr.zip` 附件或校验失败时，任务会报错。使用的发布包应包含名为 `dolibarr.zip` 的附件，而非仅有 GitHub 自动生成的源码压缩包。参阅 [1Panel 计划任务文档](https://1panel.cn/docs/v2/user_manual/cronjobs/)。

## 仓库文件

| 路径 | 用途 |
| --- | --- |
| [`apps/dolibarr`](apps/dolibarr) | 1Panel 本地应用目录及当前版本配置 |
| [`apps/dolibarr.zip`](apps/dolibarr.zip) | 仓库当前应用目录的压缩包；安装指定版本请使用 Releases 附件 |
| [`scripts/sync_latest_release.py`](scripts/sync_latest_release.py) | 定时同步最新正式 Release 的脚本 |
| [`specs/dolibarr.json`](specs/dolibarr.json) | 应用包源规格 |

实际实例的数据和凭据由 1Panel 在安装时提供，不存放在本仓库。
