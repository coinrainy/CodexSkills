# Codex Skills 上传与远程复用方案

## 目标

把你已经调通的自定义 Codex skills 放进一个 GitHub 仓库，后面无论换电脑还是切到远程服务器，都能快速恢复同一套技能与中文工作流。

## 我已经帮你落地的内容

- 已把 4 个自定义 skills 复制到仓库内的 [codex-skills](C:\Users\coinrainy\Desktop\GNN_Papers\GCL\Code\ML2-GCL - 副本\codex-skills)。
- 已新增 Windows 本地同步脚本：
  [sync_from_local_codex.ps1](C:\Users\coinrainy\Desktop\GNN_Papers\GCL\Code\ML2-GCL - 副本\codex-skills\sync_from_local_codex.ps1)
- 已新增 Windows 安装脚本：
  [install_to_codex.ps1](C:\Users\coinrainy\Desktop\GNN_Papers\GCL\Code\ML2-GCL - 副本\codex-skills\install_to_codex.ps1)
- 已新增 Linux/远程服务器安装脚本：
  [install_to_codex.sh](C:\Users\coinrainy\Desktop\GNN_Papers\GCL\Code\ML2-GCL - 副本\codex-skills\install_to_codex.sh)

## 推荐仓库方案

最推荐的是单独建一个个人仓库，例如 `codex-skills`，专门存：

- `codex-skills/`
- 这份说明文档
- 以后如果需要，也可以再加入你自己的项目级 `AGENTS.md` 模板和常用 prompt 模板

这样做的好处是：

- 不会污染论文代码仓库历史
- 后续在任何机器都能独立 clone
- 维护边界清晰，skills 更新和实验代码更新彼此解耦

## 当前仓库状态提醒

当前工作区的 Git 远端仍然是：

```text
https://github.com/a-hou/ML2-GCL
```

这更像论文代码仓库，而不是你的个人 skills 仓库。所以不建议直接把 skills 推到这个 `origin`。

## 本地维护流程

当你在 `C:\Users\coinrainy\.codex\skills` 里改完 skill 后，运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-skills\sync_from_local_codex.ps1
```

它会把这 4 个 skill 的最新内容同步回仓库副本：

- `gnn-paper-reproduction`
- `gnn-repo-runner`
- `gnn-idea-lab`
- `gnn-experiment-review`

## 上传到 GitHub 的推荐做法

### 方案 A：新建一个独立仓库

1. 在 GitHub 上新建个人仓库，比如 `codex-skills`
2. 本地新建一个干净目录，把下面这些文件复制进去：

- `codex-skills/`
- `SKILLS_GITHUB_SETUP.md`

3. 在那个新目录里执行：

```powershell
git init
git add .
git commit -m "Initial Codex skills bundle"
git branch -M main
git remote add origin <你的 GitHub 仓库 URL>
git push -u origin main
```

### 方案 B：继续在当前目录准备，但改推送目标

如果你就是想复用当前目录做一次中转，也可以：

1. 新建个人 GitHub 仓库
2. 不要直接 push 到当前 `origin`
3. 改为新增一个单独 remote，比如：

```powershell
git remote add skills-origin <你的 GitHub 仓库 URL>
git add codex-skills SKILLS_GITHUB_SETUP.md
git commit -m "Add portable Codex skills bundle"
git push -u skills-origin HEAD:main
```

这样不会影响原论文仓库的 `origin`。

## 远程服务器安装流程

远程机器 clone 你的 skills 仓库后，进入仓库根目录执行：

```bash
chmod +x codex-skills/install_to_codex.sh
./codex-skills/install_to_codex.sh
```

脚本会把 skills 安装到：

```text
~/.codex/skills
```

## Windows 本地安装流程

如果你想在另一台 Windows 机器上恢复，也可以直接执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-skills\install_to_codex.ps1
```

## 远程最小验证清单

迁移后至少检查以下几点：

1. `~/.codex/skills/gnn-paper-reproduction/SKILL.md` 存在
2. `~/.codex/skills/gnn-repo-runner/agents/openai.yaml` 存在
3. 中文内容显示正常，没有乱码
4. 能显式调用 `$gnn-repo-runner`
5. 能显式调用 `$gnn-paper-reproduction`

## 我建议你下一步这样做

如果你要最稳的方案，就按下面顺序：

1. 先新建一个个人 GitHub 仓库 `codex-skills`
2. 我再帮你把当前这些文件整理成一次干净 commit
3. 你把仓库 URL 发我，我继续帮你配置 remote、提交并推送
