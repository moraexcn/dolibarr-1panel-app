# Dolibarr 更新与验收

当前本地应用包提供 `24.0.1` 版本目录，并保留旧版目录。`crossVersionUpdate: true` 使管理员可以通过 1Panel 的升级入口选择跨大版本目标；它不会自动升级已安装实例。已有测试环境反馈 23.x → 24.0.1 可正常更新，但不同数据库和自定义模块仍须在各自环境验证。跨大版本操作可按[验收清单](UPGRADE_24_TEST.md)逐项检查。

## 1Panel 本地应用更新

将完整的 `dolibarr` 目录放到 `/opt/1panel/resource/apps/local/dolibarr`（按实际 1Panel 安装目录调整），保留旧版目录。随后在 1Panel 的“应用商店 → 本地应用”刷新应用列表，再从已安装应用的“升级”入口选择目标版本。1Panel 会读取目标版本目录，保留现有实例数据，并在启动新版本容器前执行目标版本的 `scripts/upgrade.sh`。

## 更新前

1. 在维护窗口内暂停 Web 写入和定时任务，避免备份和更新期间的数据变化。
2. 分别备份 1Panel 托管的 MySQL/MariaDB 数据库，以及实例目录中的 `data/documents` 和 `data/custom`。确认备份可读取，并记录当前镜像版本。数据库、文档和自定义模块应作为同一时点的恢复集。1Panel 升级对话框中也要勾选“升级前备份”；它不能代替对外部数据库的独立备份。
3. 在 1Panel 中选择目标版本并执行升级。目标版本的 `upgrade.sh` 会在旧容器停止、备份完成后检查文档目录并移除 `install.lock`，使新容器启动时执行 Dolibarr 的数据库版本检查。不要只替换容器镜像标签，也不要提前手工移除锁文件。

## 更新后

1. 检查 Web 容器日志和 `data/documents/initdb.log`，确认数据库迁移成功且 `install.lock` 已重新生成；若 `migration_error.html` 中记录错误或日志报告迁移失败，应停止验收。
2. 确认页面、登录、业务数据、文档附件和自定义模块可用，再启动并检查定时任务。至少运行或等待一项实际作业，确认其日志和结果。
3. 重启应用并再次检查上述数据与作业。若更新失败，应将镜像、数据库及两个数据目录一起恢复到更新前状态；仅回退镜像不能回退数据库结构。

首次安装还应核对安装表单中的 Base URL 是否为用户实际访问的完整地址，包括协议及需要的端口。更改安装表单不会自动改写已经生成的 Dolibarr `conf.php`。

## 数据库排序规则

新安装时，MySQL/MariaDB 的 1Panel 建库表单默认选择 `utf8mb4` 字符集和 `utf8mb4_unicode_ci` 排序规则。这与 Dolibarr 官方 Docker 示例一致；安装前仍应确认目标数据库服务支持该排序规则。该预设只影响新建数据库，不会修改已经安装的实例。

已有实例可先执行 `SELECT DEFAULT_COLLATION_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'dolibarr_hwd73j';` 核实数据库当前默认值。若确需修改，先备份数据库，再由有 `ALTER` 权限的账号执行 `ALTER DATABASE dolibarr_hwd73j CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`，随后重新查询确认。此语句只修改数据库默认值，不会自动转换已有表或列的字符集及排序规则；如涉及已有表，需另行盘点和迁移。

依据：[Dolibarr 官方 Docker 示例](https://github.com/Dolibarr/dolibarr-docker/blob/main/docker-compose.yml)、[Dolibarr 官方 Docker 升级说明](https://github.com/Dolibarr/dolibarr-docker/blob/main/README.md#upgrading-dolibarr-version-and-migrating-db)、[官方容器启动脚本](https://github.com/Dolibarr/dolibarr-docker/blob/main/docker-run.sh)、[1Panel 本地应用目录规范](https://github.com/1Panel-dev/appstore/wiki/%E5%A6%82%E4%BD%95%E6%8F%90%E4%BA%A4%E8%87%AA%E5%B7%B1%E6%83%B3%E8%A6%81%E7%9A%84%E5%BA%94%E7%94%A8)、[1Panel 升级实现](https://github.com/1Panel-dev/1Panel/blob/dev-v2/agent/app/service/app_upgrade.go)。
