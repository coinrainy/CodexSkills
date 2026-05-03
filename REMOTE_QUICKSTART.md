# Ubuntu 远程服务器快速跑通

适用场景：

- 远程服务器是 Ubuntu
- 还没安装 Codex
- 还没接入这个 GitHub skills 仓库

## 1. 先准备基础环境

```bash
sudo apt update
sudo apt install -y git curl build-essential
```

## 2. 安装 Node.js / npm

Codex CLI 通过 `npm` 安装。

先检查：

```bash
node -v
npm -v
```

如果还没有 `node` 或 `npm`，先按 Node.js 官方 Ubuntu 安装说明安装 LTS：

- https://nodejs.org/en/download/package-manager

## 3. 安装并登录 Codex

```bash
npm install -g @openai/codex
codex --login
```

登录完成后，可用下面命令确认：

```bash
codex --version
```

## 4. 拉取这套 skills

```bash
git clone https://github.com/coinrainy/CodexSkills.git
cd CodexSkills
chmod +x codex-skills/install_to_codex.sh
./codex-skills/install_to_codex.sh
```

## 5. 安装后检查

```bash
ls ~/.codex/skills
ls ~/.codex/skills/gnn-repo-runner
ls ~/.codex/skills/gnn-paper-reproduction
```

## 6. 后续更新

```bash
cd CodexSkills
git pull
./codex-skills/install_to_codex.sh
```

## 最短命令版

如果你的 Ubuntu 服务器已经装好 Node.js / npm，只需要执行：

```bash
npm install -g @openai/codex
codex --login
git clone https://github.com/coinrainy/CodexSkills.git
cd CodexSkills
chmod +x codex-skills/install_to_codex.sh
./codex-skills/install_to_codex.sh
```
