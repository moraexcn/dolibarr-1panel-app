# Dolibarr 1Panel 本地应用

[简体中文](README.md) | [English](README_en.md)

本仓库提供 Dolibarr 的 1Panel 本地应用包。应用目录位于 [`apps/dolibarr`](apps/dolibarr)，包含 `23.0.3` 和 `23.0.4` 两个版本；[`apps/dolibarr.zip`](apps/dolibarr.zip) 是同一应用目录的打包文件。

## 安装

1. 将完整的 `apps/dolibarr` 目录复制到 1Panel 的本地应用目录，例如 `/opt/1panel/resource/apps/local/dolibarr`。如果 1Panel 安装在其他位置，请使用实际的本地应用目录。
2. 在 1Panel 的“应用商店 → 本地应用”刷新列表，然后选择 Dolibarr 安装。
3. 填写数据库服务、管理员账号、实际访问地址等安装参数。新建 MySQL/MariaDB 数据库时，表单默认使用 `utf8mb4` 字符集和 `utf8mb4_unicode_ci` 排序规则；现有数据库不会因此自动修改。

应用简介与功能见 [`apps/dolibarr/README.md`](apps/dolibarr/README.md)。

## 更新

本地应用包保留 `23.0.3`，提供 `23.0.4` 作为同一大版本内的更新目标，并关闭跨大版本自动更新。更新现有实例前，请阅读[更新、备份与验收说明](apps/dolibarr/UPGRADE.md)。数据库、文档及自定义模块需要一起备份和恢复；不要仅替换镜像标签。

## 仓库文件

| 路径 | 用途 |
| --- | --- |
| [`apps/dolibarr`](apps/dolibarr) | 1Panel 本地应用目录与版本配置 |
| [`apps/dolibarr.zip`](apps/dolibarr.zip) | 可复制的应用目录压缩包 |
| [`specs/dolibarr.json`](specs/dolibarr.json) | 应用包源规格 |

实际实例的数据和凭据由 1Panel 在安装时提供，不存放在本仓库。
