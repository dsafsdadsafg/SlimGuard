#!/bin/bash
# SlimGuard v2.0 - 安装脚本 (macOS/Linux)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OC_DIR="$HOME/.openclaw"

echo "============================================"
echo "  SlimGuard v2.0 - 安装脚本"
echo "  极简主义饮食管理助手"
echo "============================================"
echo ""

# 步骤 1: 检查 OpenClaw
echo "[1/6] 检查 OpenClaw..."
if [ ! -d "$OC_DIR" ]; then
    echo "[错误] 未找到 OpenClaw"
    echo "请先安装：https://openclaw.ai"
    exit 1
fi
echo "      ✓ OpenClaw 已安装"

# 步骤 2: 备份配置
echo ""
echo "[2/6] 备份已有配置..."
if [ -f "$OC_DIR/openclaw.json" ]; then
    cp "$OC_DIR/openclaw.json" "$OC_DIR/openclaw.json.backup.$(date +%Y%m%d%H%M%S)"
    echo "      ✓ 已备份"
else
    echo "      - 无旧配置"
fi

# 步骤 3: 复制 Agent 文件
echo ""
echo "[3/6] 复制 Agent 文件..."
AGENT_DIR="$OC_DIR/agents/slimguard"
mkdir -p "$AGENT_DIR"
cp -r "$SCRIPT_DIR/agents/slimguard/"* "$AGENT_DIR/"
echo "      ✓ 已复制到 $AGENT_DIR"

# 步骤 4: 复制工作区文件
echo ""
echo "[4/6] 复制工作区文件..."
WORKSPACE_DIR="$OC_DIR/workspace/slimguard"
mkdir -p "$WORKSPACE_DIR/scripts"
mkdir -p "$WORKSPACE_DIR/tools"
cp -r "$SCRIPT_DIR/scripts/"* "$WORKSPACE_DIR/scripts/"
cp -r "$SCRIPT_DIR/tools/"* "$WORKSPACE_DIR/tools/"
echo "      ✓ 已复制到 $WORKSPACE_DIR"

# 步骤 5: 注册 Agent
echo ""
echo "[5/6] 注册 Agent..."
python3 << PYTHON_SCRIPT
import json
import sys

config_path = "$OC_DIR/openclaw.json"
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    exists = any(a['id'] == 'slimguard' for a in config.get('agents', {}).get('list', []))
    if not exists:
        if 'agents' not in config:
            config['agents'] = {'list': []}
        if 'list' not in config['agents']:
            config['agents']['list'] = []
        
        config['agents']['list'].append({
            'id': 'slimguard',
            'name': 'SlimGuard',
            'workspace': '$WORKSPACE_DIR'
        })
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print('      ✓ 已注册 slimguard Agent')
    else:
        print('      - slimguard 已存在')
except Exception as e:
    print(f'      ✗ 注册失败：{e}')
    sys.exit(1)
PYTHON_SCRIPT

# 步骤 6: 配置定时任务
echo ""
echo "[6/6] 配置定时任务..."
python3 << PYTHON_SCRIPT
import json
import os

cron_file = "$OC_DIR/cron/jobs.json"
if os.path.exists(cron_file):
    try:
        with open(cron_file, 'r', encoding='utf-8') as f:
            cron = json.load(f)
        
        exists = any(j['id'] == 'slimguard-daily-summary' for j in cron.get('jobs', []))
        if not exists:
            cron['jobs'].append({
                'id': 'slimguard-daily-summary',
                'name': 'SlimGuard 每日总结',
                'schedule': {
                    'kind': 'cron',
                    'expr': '0 22 * * *',
                    'tz': 'Asia/Shanghai'
                },
                'sessionTarget': 'isolated',
                'payload': {
                    'kind': 'agentTurn',
                    'message': 'generate_daily_report'
                },
                'delivery': {
                    'mode': 'announce',
                    'channel': 'last'
                }
            })
            
            with open(cron_file, 'w', encoding='utf-8') as f:
                json.dump(cron, f, indent=2, ensure_ascii=False)
            
            print('      ✓ 已添加 22:00 每日总结任务')
        else:
            print('      - 定时任务已存在')
    except Exception as e:
        print(f'      ✗ 配置失败：{e}')
else:
    print('      - cron/jobs.json 不存在，跳过')
PYTHON_SCRIPT

echo ""
echo "============================================"
echo "  安装完成！"
echo "============================================"
echo ""
echo "下一步："
echo "1. 运行：openclaw gateway restart"
echo "2. 在 Telegram 中联系 SlimGuard Bot"
echo "3. 说：\"早餐吃了 2 片面包\""
echo ""
echo "每日 22:00 自动推送饮食总结"
echo ""
