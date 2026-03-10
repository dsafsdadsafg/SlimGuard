# SlimGuard v2.0 🥗

> 极简主义私人饮食管理助手  
> 参考 [edict](https://github.com/cft0808/edict) 架构设计  
> **独立 OpenClaw Agent - 只记录数据，不聊天**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Agent-blue)](https://openclaw.ai)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)

---

## 🚀 快速开始

```bash
git clone https://github.com/你的用户名/SlimGuard.git
cd SlimGuard
install.bat  # Windows
./install.sh # macOS/Linux
openclaw gateway restart
```

详细安装指南 → [INSTALL.md](INSTALL.md)

## 特性

- ✅ **极简输出** - 只返回数据，不聊天
- ✅ **被动响应** - 不打扰用户
- ✅ **每日总结** - 22:00 自动推送
- ✅ **JSON 约束** - 结构化数据输出
- ✅ **零依赖** - 仅 Python 标准库

## 安装

```bash
cd SlimGuard-OpenClaw
install.bat  # Windows
./install.sh # macOS/Linux
```

安装后重启：
```bash
openclaw gateway restart
```

## 使用

### Telegram/飞书

```
吃了 2 片面包
米饭热量多少
喝了 300ml 水
跑步 30 分钟
今天的报告
```

### 输出示例

```
用户：吃了 2 片面包
SlimGuard: ✅ 面包 x2 片 - 530kcal

用户：今天的报告
SlimGuard: 📊 今日饮食报告 - 2026-03-10
           ========================
           🍽️ 3 餐 | 总热量：1200kcal
           蛋白质：45g | 碳水：180g | 脂肪：35g
           
           💧 饮水：1500ml / 2000ml
           🏃 运动：200kcal
           
           📈 热量余额：800kcal
```

## 架构

```
Telegram/飞书 → SlimGuard Agent → diet_core.py → JSON 数据
                     ↓
              cron (22:00) → 每日总结
```

## 文件结构

```
SlimGuard-OpenClaw/
├── agents/
│   └── slimguard/
│       ├── agent.json    # Agent 配置
│       └── SOUL.md       # 角色定义
├── scripts/
│   └── diet_core.py      # 核心逻辑
├── tools/
│   └── food_database.json # 食物数据库
├── install.bat           # 安装脚本
└── requirements.txt      # 依赖（无）
```

## 许可证

MIT
