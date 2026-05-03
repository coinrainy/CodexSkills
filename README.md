# CodexSkills

这是我自定义的 Codex skills 仓库，主要面向 GNN / GCL 论文复现、原始仓库跑通、实验复盘和研究 idea 生成。

## 当前包含的 skills

- `gnn-paper-reproduction`
- `gnn-repo-runner`
- `gnn-idea-lab`
- `gnn-experiment-review`

## 仓库结构

- `codex-skills/`: 可直接安装到 Codex 的 skills 副本
- `SKILLS_GITHUB_SETUP.md`: 上传、同步、远程安装说明

## 本地更新

如果我先在本机 `~/.codex/skills` 中修改了某个 skill，再把改动同步回仓库副本：

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-skills\sync_from_local_codex.ps1
```

## Windows 安装

```powershell
powershell -ExecutionPolicy Bypass -File .\codex-skills\install_to_codex.ps1
```

## Linux / 远程服务器安装

```bash
chmod +x codex-skills/install_to_codex.sh
./codex-skills/install_to_codex.sh
```

默认安装目录：

```text
~/.codex/skills
```

## 使用建议

- 先在本地把新 skill 调通，再同步到这个仓库
- 远程机器优先保持 UTF-8 环境，减少中文乱码风险
- 如果要长期保持中文工作流，除了同步 skills，也建议同步项目级 `AGENTS.md`
