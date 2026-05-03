# Codex Skills Sync Package

这个目录是可提交到 GitHub 的自定义 Codex skills 副本。

## 当前包含的 skills

- `gnn-paper-reproduction`
- `gnn-repo-runner`
- `gnn-idea-lab`
- `gnn-experiment-review`

## 推荐用途

- 本地把 `C:\Users\coinrainy\.codex\skills` 里的自定义 skills 同步到仓库
- 把本目录上传到你自己的 GitHub 仓库
- 在远程服务器拉取仓库后，一键安装到 `~/.codex/skills/`

## 常用脚本

- Windows 本地同步：`sync_from_local_codex.ps1`
- Windows 本地安装：`install_to_codex.ps1`
- Linux/远程服务器安装：`install_to_codex.sh`

## 最短工作流

### 1. 本地刷新仓库副本

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-skills\sync_from_local_codex.ps1
```

### 2. 提交并推送到你的 GitHub 仓库

```powershell
git add codex-skills SKILLS_GITHUB_SETUP.md
git commit -m "Add portable Codex skills bundle"
git push
```

### 3. 远程服务器安装

```bash
chmod +x codex-skills/install_to_codex.sh
./codex-skills/install_to_codex.sh
```

## 说明

- 默认保留 UTF-8 中文内容。
- 如果后续你新增 skill，先在本地 `~/.codex/skills` 调通，再运行同步脚本更新仓库副本。
