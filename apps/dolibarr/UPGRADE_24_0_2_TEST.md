# Dolibarr 24.0.1 → 24.0.2 测试验收清单

本文件适用于测试分支中的 1Panel 24.0.2 候选包。官方 Docker 镜像 `dolibarr/dolibarr:24.0.2` 已提供 amd64 与 arm64。此包尚未经用户实测，不能作为正式 Release 或直接用于生产升级。

[Dolibarr 官方 24.0.2 发布说明](https://github.com/Dolibarr/dolibarr/releases/tag/24.0.2) · [官方 Docker 镜像](https://hub.docker.com/r/dolibarr/dolibarr/tags?name=24.0.2)

1. 从测试分支下载 `apps/dolibarr.zip`，核对公布的 SHA-256。解压到隔离测试服务器的 1Panel 本地应用目录，保留原有版本目录。
2. 使用现有 24.0.1 实例的副本。暂停写入与定时任务，独立备份数据库、`data/documents` 和 `data/custom`，并做一次恢复演练。记录 1Panel、数据库和镜像版本。
3. 刷新“应用商店 → 本地应用”，从已安装应用的“升级”入口选择 24.0.2，勾选升级前备份。不要只改镜像标签，也不要卸载旧实例。
4. 确认 Web 与 cron 都运行 24.0.2 镜像；检查容器日志、`data/documents/initdb.log`、`migration_error.html`，确认迁移完成且 `install.lock` 已重新生成。
5. 检查登录、原有业务数据、附件、自定义模块和至少一项实际定时任务；重启后复查。
6. 在隔离环境使用同一恢复集演练回退：同时恢复旧版镜像、数据库、文档和自定义模块。只回退镜像不能还原数据库结构。

反馈时请提供通过/失败、源版本、1Panel 与数据库版本、脱敏日志；不要发送密码、令牌或客户数据。测试通过后，才更新 `main` 并发布正式 Release。
