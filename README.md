# Dolibarr 1Panel 本地应用

[简体中文](README.md) | [English](README_en.md)

本项目基于 [1Panel](https://github.com/1Panel-dev/1Panel) 的本地应用机制、1Panel 官方 [Appstore Skills](https://github.com/1Panel-dev/1Panel-appstore-skills) 的应用包规范，以及 [Dolibarr](https://github.com/Dolibarr/dolibarr) 的[官方 Docker 部署方案](https://github.com/Dolibarr/dolibarr-docker)制作，提供可导入 1Panel 的 Dolibarr 应用包。

应用目录为 [`apps/dolibarr`](apps/dolibarr)。**当前仓库收录** `23.0.3` 和 `23.0.4` 两个版本目录；这只是目前打包的版本，不限制项目今后增加其他版本。实际可安装版本以应用目录中的版本配置为准。[`apps/dolibarr.zip`](apps/dolibarr.zip) 是当前应用目录的压缩包。

## 安装前准备

- 在 Linux 服务器上安装并登录 1Panel，确认 Docker 服务可用。
- 先通过 1Panel 安装一个 MySQL 或 MariaDB 数据库服务，并确认其运行正常。安装 Dolibarr 时需要在表单中选择该服务。
- 确定访问方式：直接通过服务器地址和端口访问，或使用已配置好的域名及反向代理。准备一个未占用的 Web UI 端口。

## 导入并安装

1. 从本仓库下载 [`apps/dolibarr.zip`](apps/dolibarr.zip)，上传到运行 1Panel 的服务器。压缩包顶层已经包含 `dolibarr/` 目录。
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

当前应用包提供从 `23.0.3` 到 `23.0.4` 的同大版本更新路径，并关闭跨大版本自动更新。新增版本需要按 1Panel 的应用包和 Dolibarr 的数据库迁移要求单独制作、测试。更新现有实例前，请阅读[更新、备份与验收说明](apps/dolibarr/UPGRADE.md)；数据库、文档及自定义模块应一起备份和恢复。

## 仓库文件

| 路径 | 用途 |
| --- | --- |
| [`apps/dolibarr`](apps/dolibarr) | 1Panel 本地应用目录及当前版本配置 |
| [`apps/dolibarr.zip`](apps/dolibarr.zip) | 当前应用目录的压缩包 |
| [`specs/dolibarr.json`](specs/dolibarr.json) | 应用包源规格 |

实际实例的数据和凭据由 1Panel 在安装时提供，不存放在本仓库。
