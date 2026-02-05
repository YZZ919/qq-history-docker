# qq-history-docker

本仓库是一个个人工具集合：

- `qzone-history/qzone-history-main/`：Qzone 历史内容导出/重建相关的 Go 项目
- `logout_qq.py`：清理 `app.db` 中某个 QQ 的登录 cookies（强制退出）

## 注意

本项目运行过程中会生成/使用包含个人信息的文件（例如 `app.db`、导出结果等），已在根目录 `.gitignore` 中默认忽略，建议不要提交到 GitHub。
