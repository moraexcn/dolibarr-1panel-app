# Dolibarr 23.x → 24.0.1 升级验收清单

> 官方 `dolibarr/dolibarr:24.0.1` 镜像已发布。本清单用于升级前的隔离环境验证和正式升级验收。不要用 `24` 或 `24.0.0` 标签代替 `24.0.1`。

## 1. 测试前确认

1. 在 [Dolibarr 官方 Docker Hub 标签页](https://hub.docker.com/r/dolibarr/dolibarr/tags?name=24.0.1)确认 **精确的 `24.0.1` 标签**存在，且测试服务器的 `amd64` 或 `arm64` 架构可用；在服务器上执行 `docker manifest inspect dolibarr/dolibarr:24.0.1` 再次确认。
2. 确认测试环境的 MySQL 版本至少为 5.7.7，或 MariaDB 至少为 10.3；核对外部模块、定制代码与 Dolibarr 24 的兼容性。Dolibarr 24 的 PHP 兼容范围以[官方版本表](https://wiki.dolibarr.org/index.php/Releases)为准；官方镜像自带 PHP。
3. 在隔离的 1Panel 测试环境中，从实际使用的 23.x 版本和数据副本开始。不要在生产实例上首次验证跨大版本迁移。
4. 记录旧版本、数据库版本、实例目录、使用中的模块和一项可重复核对的业务记录及附件。不要在反馈中发送密码、令牌或客户数据。

## 2. 一致性备份和恢复演练

1. 在维护窗口停止 Web 写入和 Dolibarr 定时任务。
2. 独立备份 1Panel 托管的数据库、实例的 `data/documents` 和 `data/custom`。保存为同一时点的恢复集，并确认备份可读取。1Panel 升级对话框中的“升级前备份”也应勾选，但不能代替数据库的独立备份。
3. 在隔离环境先用这套备份恢复一次 23.x，确认登录、业务记录、附件和自定义模块可用。恢复验证通过后，再用该实例测试升级。

## 3. 1Panel 升级测试

1. 从本仓库对应的 [Release](https://github.com/moraexcn/dolibarr-1panel-app/releases) 下载 `dolibarr.zip` 附件；将完整 `dolibarr/` 目录导入服务器的 `/opt/1panel/resource/apps/local/`（路径以实际安装位置为准）。保留旧版目录。先在隔离环境验证，再处理生产实例。
2. 在“应用商店 → 本地应用”刷新列表，确认 24.0.1 出现；从已安装 Dolibarr 的“升级”入口选择 24.0.1，勾选升级前备份。不要卸载旧实例后重新安装，也不要只改 Compose 镜像标签。
3. 升级后确认 Web 和 cron 容器使用 24.0.1 镜像；查看容器日志、`data/documents/initdb.log` 与 `migration_error.html`。确认数据库迁移成功、`install.lock` 已重新生成，且没有未处理的迁移错误。
4. 检查页面与登录、测试前记录的业务数据及附件、自定义模块、至少一项实际定时任务；重启应用后重复检查。记录 1Panel 版本、测试源版本、目标版本、数据库版本、镜像摘要及结果。

## 4. 失败时恢复

停止 24.0.1 实例，使用第 2 节的**同一恢复集**恢复旧版镜像、数据库、`data/documents` 和 `data/custom`，再确认旧版登录、数据、附件和任务。数据库迁移后只回退镜像无法恢复旧数据库结构；不要把升级后生成的数据混入旧版恢复集。

记录每一步的“通过/失败”、脱敏日志片段和失败发生的阶段，以便定位问题并验证恢复。

依据：[Dolibarr 官方 Docker 升级说明](https://github.com/Dolibarr/dolibarr-docker#upgrading-dolibarr-version-and-migrating-db)、[Dolibarr 升级说明](https://wiki.dolibarr.org/index.php/Installation_-_Upgrade)、[1Panel 应用操作说明](https://1panel.cn/docs/v2/user_manual/appstore/installed/)。
