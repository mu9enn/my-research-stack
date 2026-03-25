# 从零开始：配置 SSH 实现 Git Clone

本指南指导你在一台**未安装 Git** 的电脑上，完成从安装到使用 **SSH 协议** 进行 `git clone` 的全过程。

---

## 1. 安装 Git

首先需要下载并安装 Git 工具。

- **Windows 用户**:
  访问 [git-scm.com](https://git-scm.com/download/win)。
- **macOS 用户**:
  打开终端，输入 `git --version`。如果未安装，系统会提示安装命令行工具，按提示操作即可。
- **Linux 用户**:
  使用包管理器安装，例如 Ubuntu: `sudo apt install git`。

---

## 2. 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "sun4382@gmail.com"
```
- 生成成功后，会显示保存路径（通常是 `~/.ssh/id_ed25519`）。

---

## 3. 获取公钥内容

你需要将生成的**公钥**复制到代码托管平台。

在终端输入：

  ```bash
  cat ~/.ssh/id_ed25519.pub
  ```

**复制** 输出的全部内容（以 `ssh-ed25519` 开头，以邮箱结尾）。

---

## 4. 添加公钥到托管平台


---

## 5. 测试连接

在终端输入以下命令测试 SSH 连接是否成功：

```bash
ssh -T git@github.com
```

