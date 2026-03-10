# 📤 推送到 GitHub 指南

## 方式一：使用 Personal Access Token（推荐）

### 1. 创建 Token

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 勾选 **repo** 权限
4. 生成并复制 Token（格式：`ghp_xxxxxxxxxxxx`）

### 2. 推送代码

```bash
cd C:\Users\admin\.openclaw\SlimGuard-OpenClaw

# 添加 remote（如果已添加可跳过）
git remote add origin https://github.com/dsafsdadsafg/SlimGuard.git

# 推送（使用你的 Token）
git push -u origin main
```

输入密码时，粘贴你的 Token（不会显示字符）

---

## 方式二：使用 SSH

### 1. 生成 SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. 添加 SSH Key 到 GitHub

1. 复制公钥：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
2. 访问 https://github.com/settings/keys
3. 点击 **New SSH key**
4. 粘贴公钥

### 3. 使用 SSH URL 推送

```bash
cd C:\Users\admin\.openclaw\SlimGuard-OpenClaw

# 移除 HTTPS remote
git remote remove origin

# 添加 SSH remote
git remote add origin git@github.com:dsafsdadsafg/SlimGuard.git

# 推送
git push -u origin main
```

---

## 方式三：使用 GitHub Desktop

1. 下载 https://desktop.github.com
2. 登录 GitHub
3. 添加本地仓库：`C:\Users\admin\.openclaw\SlimGuard-OpenClaw`
4. 发布到 GitHub

---

## 验证推送

访问 https://github.com/dsafsdadsafg/SlimGuard 确认文件已上传。

---

## 安装说明

用户安装时运行：

```bash
git clone https://github.com/dsafsdadsafg/SlimGuard.git
cd SlimGuard
install.bat  # Windows
./install.sh # macOS/Linux
openclaw gateway restart
```
