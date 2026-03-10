@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   SlimGuard v2.0 - 安装脚本
echo   极简主义饮食管理助手
echo ============================================
echo.

set "SCRIPT_DIR=%~dp0"
set "OC_DIR=%USERPROFILE%\.openclaw"

echo [1/6] 检查 OpenClaw...
if not exist "%OC_DIR%" (
    echo [错误] 未找到 OpenClaw
    echo 请先安装：https://openclaw.ai
    exit /b 1
)
echo       ✓ OpenClaw 已安装

echo.
echo [2/6] 备份已有配置...
if exist "%OC_DIR%\openclaw.json" (
    copy "%OC_DIR%\openclaw.json" "%OC_DIR%\openclaw.json.backup.%date:~0,4%%date:~5,2%%date:~8,2%" >nul
    echo       ✓ 已备份
) else (
    echo       - 无旧配置
)

echo.
echo [3/6] 复制 Agent 文件...
set "AGENT_DIR=%OC_DIR%\agents\slimguard"
if not exist "%AGENT_DIR%" mkdir "%AGENT_DIR%"
xcopy /E /I /Y "%SCRIPT_DIR%agents\slimguard" "%AGENT_DIR%" >nul
echo       ✓ 已复制到 %AGENT_DIR%

echo.
echo [4/6] 复制脚本和工具...
set "WORKSPACE_DIR=%OC_DIR%\workspace\slimguard"
if not exist "%WORKSPACE_DIR%" mkdir "%WORKSPACE_DIR%"
xcopy /E /I /Y "%SCRIPT_DIR%scripts" "%WORKSPACE_DIR%\scripts" >nul
xcopy /E /I /Y "%SCRIPT_DIR%tools" "%WORKSPACE_DIR%\tools" >nul
echo       ✓ 已复制到 %WORKSPACE_DIR%

echo.
echo [5/6] 注册 Agent...
powershell -Command "& {
    $config = Get-Content '%OC_DIR%\openclaw.json' -Raw | ConvertFrom-Json
    $exists = $config.agents.list | Where-Object { $_.id -eq 'slimguard' }
    if (-not $exists) {
        $config.agents.list += @{
            id = 'slimguard'
            name = 'SlimGuard'
            workspace = '%WORKSPACE_DIR%'
        }
        $config | ConvertTo-Json -Depth 10 | Set-Content '%OC_DIR%\openclaw.json' -Encoding UTF8
        Write-Host '       ✓ 已注册 slimguard Agent'
    } else {
        Write-Host '       - slimguard 已存在'
    }
}"

echo.
echo [6/6] 配置定时任务...
powershell -Command "& {
    $cronFile = '%OC_DIR%\cron\jobs.json'
    if (Test-Path $cronFile) {
        $cron = Get-Content $cronFile -Raw | ConvertFrom-Json
        $exists = $cron.jobs | Where-Object { $_.id -eq 'slimguard-daily-summary' }
        if (-not $exists) {
            $cron.jobs += @{
                id = 'slimguard-daily-summary'
                name = 'SlimGuard 每日总结'
                schedule = @{ kind = 'cron'; expr = '0 22 * * *'; tz = 'Asia/Shanghai' }
                sessionTarget = 'isolated'
                payload = @{ kind = 'agentTurn'; message = 'generate_daily_report' }
                delivery = @{ mode = 'announce'; channel = 'last' }
            }
            $cron | ConvertTo-Json -Depth 10 | Set-Content $cronFile -Encoding UTF8
            Write-Host '       ✓ 已添加 22:00 每日总结任务'
        } else {
            Write-Host '       - 定时任务已存在'
        }
    }
}"

echo.
echo ============================================
echo   安装完成！
echo ============================================
echo.
echo 下一步：
echo 1. 运行：openclaw gateway restart
echo 2. 在 Telegram/飞书中联系 SlimGuard Bot
echo 3. 说：\"早餐吃了 2 片面包\"
echo.
echo 每日 22:00 自动推送饮食总结
echo.
pause
