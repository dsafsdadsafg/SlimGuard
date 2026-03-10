# SlimGuard 🥗 - 私人饮食管理助手

> 极简主义 OpenClaw Agent - 只记录数据，不聊天  
> 参考 [edict](https://github.com/cft0808/edict) 架构设计

---

## ⚡ 30 秒快速安装

### 前置条件

- ✅ OpenClaw 已安装
- ✅ Python 3.8+
- ✅ Windows / macOS / Linux

### 一键安装

```bash
# 1. 下载项目
git clone https://github.com/你的用户名/SlimGuard.git
cd SlimGuard

# 2. 运行安装脚本
# Windows
install.bat

# macOS/Linux
chmod +x install.sh && ./install.sh
```

### 配置 Telegram Bot（可选）

安装过程中会提示输入 Bot Token，如果没有准备，可以跳过，后续手动配置。

**获取 Bot Token：**
1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot`
3. 按提示设置 Bot 名称和用户名
4. 复制 Token（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

### 重启 Gateway

```bash
openclaw gateway restart
```

---

## 🔧 手动配置（如果自动安装失败）

### 步骤 1：复制 Agent 文件

```bash
# 复制 Agent 配置
cp -r agents/slimguard ~/.openclaw/agents/slimguard

# 复制工作区文件
cp -r scripts ~/.openclaw/workspace/slimguard/scripts
cp -r tools ~/.openclaw/workspace/slimguard/tools
```

### 步骤 2：注册 Agent

编辑 `~/.openclaw/openclaw.json`，在 `agents.list` 中添加：

```json
{
  "id": "slimguard",
  "name": "SlimGuard",
  "workspace": "/Users/你的用户名/.openclaw/workspace/slimguard"
}
```

**Windows 路径示例：**
```json
{
  "id": "slimguard",
  "name": "SlimGuard",
  "workspace": "C:\\Users\\你的用户名\\.openclaw\\workspace\\slimguard"
}
```

### 步骤 3：配置 Telegram Bot

编辑 `~/.openclaw/openclaw.json`，在 `channels.telegram.accounts` 中添加：

```json
{
  "slimguard": {
    "dmPolicy": "pairing",
    "botToken": "你的 Bot Token",
    "groupPolicy": "allowlist",
    "streaming": "partial"
  }
}
```

在 `bindings` 中添加：

```json
{
  "agentId": "slimguard",
  "match": {
    "channel": "telegram",
    "accountId": "slimguard"
  }
}
```

### 步骤 4：配置定时任务（每日 22:00 总结）

编辑 `~/.openclaw/cron/jobs.json`，添加：

```json
{
  "id": "slimguard-daily-summary",
  "name": "SlimGuard 每日总结",
  "schedule": {
    "kind": "cron",
    "expr": "0 22 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "generate_daily_report"
  },
  "delivery": {
    "mode": "announce",
    "channel": "last"
  }
}
```

### 步骤 5：重启 Gateway

```bash
openclaw gateway restart
```

---

## 📱 配对使用

### 1. 在 Telegram 中找到 Bot

搜索你配置的 Bot 名称（或用户名）

### 2. 发送配对消息

给 Bot 发送任意消息，如：`你好`

### 3. 批准配对（如果需要）

如果收到配对码，在终端运行：

```bash
openclaw pairing approve telegram 配对码
```

---

## 💬 使用示例

### 记录饮食

```
用户：吃了 2 片面包和 1 个鸡蛋
SlimGuard: ✅ 面包 x2 片 - 159kcal
           ✅ 鸡蛋 x1 个 - 71kcal
           小计：230kcal
```

### 查询热量

```
用户：米饭热量多少
SlimGuard: 📊 米饭 (100g): 116kcal | 蛋白质 2.6g | 碳水 25.6g | 脂肪 0.3g
```

### 记录饮水

```
用户：喝了 300ml 水
SlimGuard: 💧 300ml / 2000ml
```

### 记录运动

```
用户：跑步 30 分钟
SlimGuard: 🏃 30 分钟 - 300kcal
```

### 每日报告

```
用户：今天的报告
SlimGuard: 📊 今日饮食报告 - 2026-03-10
           ========================
           🍽️ 3 餐 | 总热量：1200kcal
           蛋白质：45g | 碳水：180g | 脂肪：35g
           
           💧 饮水：1500ml / 2000ml
           🏃 运动：200kcal
           
           📈 热量余额：800kcal
```

---

## 📁 项目结构

```
SlimGuard/
├── agents/
│   └── slimguard/
│       ├── agent.json    # Agent 配置（systemPrompt、工具权限）
│       └── SOUL.md       # 角色定义（极简主义原则）
├── scripts/
│   └── diet_core.py      # 核心逻辑（饮食记录、查询、报告）
├── tools/
│   └── food_database.json # 食物数据库（30+ 种常见食物）
├── install.bat           # Windows 安装脚本
├── install.sh            # macOS/Linux 安装脚本
├── requirements.txt      # 依赖（无，仅标准库）
└── README.md             # 本文档
```

---

## 🛠️ 故障排查

### 问题 1：Bot 不回复

**检查：**
```bash
# 1. 确认 Agent 已注册
cat ~/.openclaw/openclaw.json | grep slimguard

# 2. 确认 Bot Token 正确
cat ~/.openclaw/openclaw.json | grep botToken

# 3. 确认 binding 配置
cat ~/.openclaw/openclaw.json | grep -A3 '"agentId": "slimguard"'
```

**解决：** 重启 Gateway
```bash
openclaw gateway restart
```

### 问题 2：食物数据找不到

**原因：** `food_database.json` 路径不对

**解决：** 确保文件在 `~/.openclaw/workspace/slimguard/tools/food_database.json`

### 问题 3：定时任务不执行

**检查：**
```bash
# 查看 cron 配置
cat ~/.openclaw/cron/jobs.json | grep slimguard

# 查看 cron 运行日志
openclaw cron runs slimguard-daily-summary
```

**解决：** 确认时区正确（`Asia/Shanghai`）

### 问题 4：中文乱码

**原因：** Windows 编码问题

**解决：** 在 `diet_core.py` 开头添加：
```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

---

## 📊 数据管理

### 数据位置

所有数据存储在 `~/.openclaw/workspace/slimguard/scripts/memory/`

```
memory/
├── meals.json        # 饮食记录
├── water.json        # 饮水记录
├── exercise.json     # 运动记录
├── weight.json       # 体重记录
├── user_profile.json # 用户信息
└── goals.json        # 目标设置
```

### 备份数据

```bash
cp -r ~/.openclaw/workspace/slimguard/scripts/memory ~/backup/slimguard-memory-$(date +%Y%m%d)
```

### 重置数据

```bash
rm ~/.openclaw/workspace/slimguard/scripts/memory/*.json
# 重启 Gateway 后会自动创建默认文件
openclaw gateway restart
```

---

## 🎯 自定义

### 修改默认目标

编辑 `~/.openclaw/workspace/slimguard/scripts/memory/goals.json`：

```json
{
  "calorie_goal": 1500,    // 每日热量目标
  "protein_goal": 80,      // 蛋白质目标 (g)
  "carbs_goal": 150,       // 碳水目标 (g)
  "fat_goal": 50,          // 脂肪目标 (g)
  "water_goal": 2500       // 饮水目标 (ml)
}
```

### 添加新食物

编辑 `~/.openclaw/workspace/slimguard/tools/food_database.json`：

```json
{
  "新分类": {
    "新食物": {
      "calories": 100,
      "protein": 5,
      "carbs": 20,
      "fat": 2,
      "unit": "100g"
    }
  }
}
```

### 修改输出风格

编辑 `~/.openclaw/agents/slimguard/agent.json` 中的 `systemPrompt`

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - Agent 框架
- [edict](https://github.com/cft0808/edict) - 架构参考

---

## 📞 支持

遇到问题？提交 Issue 或联系作者。
