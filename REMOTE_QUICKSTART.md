# 远程服务器快速跑通

适用场景：

- 远程服务器还没安装 Codex
- 远程服务器已经能用 Codex，但还没接入这套 skills

## 情况 1：服务器还没装 Codex

先完成 Codex 的官方安装与登录。

完成后进入下面流程。

## 情况 2：Codex 已可用，但还没接入 skills

在远程服务器执行：

```bash
git clone https://github.com/coinrainy/CodexSkills.git
cd CodexSkills
chmod +x codex-skills/install_to_codex.sh
./codex-skills/install_to_codex.sh
```

## 安装后检查

确认下面文件存在：

```bash
ls ~/.codex/skills
ls ~/.codex/skills/gnn-repo-runner
ls ~/.codex/skills/gnn-paper-reproduction
```

## 之后怎么更新

远程服务器上执行：

```bash
cd CodexSkills
git pull
./codex-skills/install_to_codex.sh
```

## 最短结论

如果远程已经有 Codex，可直接执行这 4 行：

```bash
git clone https://github.com/coinrainy/CodexSkills.git
cd CodexSkills
chmod +x codex-skills/install_to_codex.sh
./codex-skills/install_to_codex.sh
```
