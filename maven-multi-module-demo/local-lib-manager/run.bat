@echo off
REM Maven本地Jar依赖管理工具 - Windows启动脚本
REM
REM 使用方法：
REM   run.bat              - 执行所有操作
REM   run.bat setup        - 只创建目录
REM   run.bat copy         - 只复制jar
REM   run.bat generate     - 只生成配置
REM   run.bat readme       - 只生成README

setlocal enabledelayedexpansion

echo ================================================
echo  Maven本地Jar依赖管理工具
echo ================================================
echo.

REM 检查Python是否安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.6+
    echo.
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 显示Python版本
echo [信息] 检测到Python版本:
python --version
echo.

REM 检查依赖
echo [信息] 检查Python依赖...
python -c "import yaml" >nul 2>nul
if %errorlevel% neq 0 (
    echo [警告] 未安装pyyaml库，正在安装...
    pip install pyyaml
    if %errorlevel% neq 0 (
        echo [错误] 安装pyyaml失败
        pause
        exit /b 1
    )
    echo [成功] pyyaml安装完成
    echo.
)

REM 检查配置文件
if not exist "jars-config.yaml" (
    echo [警告] 未找到配置文件 jars-config.yaml
    echo [信息] 正在从示例文件创建...
    copy jars-config.example.yaml jars-config.yaml >nul
    echo [成功] 已创建配置文件，请编辑 jars-config.yaml 后再次运行
    echo.
    pause
    exit /b 0
)

REM 执行Python脚本
if "%1"=="" (
    echo [信息] 执行所有操作...
    python lib_manager.py --all
) else if "%1"=="setup" (
    echo [信息] 创建目录结构...
    python lib_manager.py --setup
) else if "%1"=="copy" (
    echo [信息] 复制jar文件...
    python lib_manager.py --copy
) else if "%1"=="generate" (
    echo [信息] 生成Maven配置...
    python lib_manager.py --generate
) else if "%1"=="readme" (
    echo [信息] 生成README文件...
    python lib_manager.py --readme
) else (
    echo [错误] 未知参数: %1
    echo.
    echo 支持的参数:
    echo   setup     - 创建目录结构
    echo   copy      - 复制jar文件
    echo   generate  - 生成Maven配置
    echo   readme    - 生成README文件
    echo   (空)      - 执行所有操作
    pause
    exit /b 1
)

if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo  处理完成！
    echo ================================================
    echo.
    echo 下一步操作:
    echo 1. 查看生成的 generated-pom-configs.xml
    echo 2. 将配置复制到对应模块的 pom.xml
    echo 3. 运行 mvn clean install 验证
    echo.
) else (
    echo.
    echo [错误] 处理失败，请查看错误信息
    echo.
)

pause
