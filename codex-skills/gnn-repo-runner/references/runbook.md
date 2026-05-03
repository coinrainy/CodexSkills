# 仓库执行操作手册

## 适用场景

- 仓库很陌生或文档很差
- 不清楚第一条命令该跑什么
- 环境问题和代码问题交织在一起

## 快速排查顺序

1. 找主入口。
重点看 `train.py`、`main.py`、`run.sh`、`scripts/*.sh` 和配置驱动的启动器。

2. 找依赖声明。
检查 `requirements.txt`、`environment.yml`、`setup.py`、`pyproject.toml` 和 README 的安装说明。

3. 找运行证据。
已有日志、checkpoint、tensorboard 文件夹和输出目录经常能反推出作者原本想运行的命令。

4. 找数据集假设。
确认第一次运行前是否需要特定路径、下载开关或手动预处理。

## 常见修复点

1. 版本漂移
老仓库经常因为新版 PyTorch、PyG、DGL、NumPy 或 Python 而失效。

2. 路径过硬
硬编码绝对路径或只适配 Linux 的假设很常见。优先做小范围路径修复，不要上来大改。

3. 仅 shell 脚本可运行
必要时把 shell 脚本翻译成等价的本地命令，但要保留原始意图。

4. 设备假设
如果用户当前目标只是先跑通，在 GPU-only 代码遇到环境不匹配时，可以安全退回 CPU 或兼容的 CUDA 配置。

## 日志记录规范

每次有意义的尝试都应记录：
- command
- purpose
- result
- error summary
- fix summary
- follow-up decision
