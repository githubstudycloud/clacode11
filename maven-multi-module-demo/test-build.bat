@echo off
REM Windows构建测试脚本

echo ========================================
echo Maven多模块项目构建测试
echo ========================================
echo.

echo [1/4] 清理项目...
call mvn clean
if %ERRORLEVEL% NEQ 0 (
    echo 清理失败！
    pause
    exit /b 1
)
echo.

echo [2/4] 编译项目...
call mvn compile -DskipTests
if %ERRORLEVEL% NEQ 0 (
    echo 编译失败！
    pause
    exit /b 1
)
echo.

echo [3/4] 打包项目...
call mvn package -DskipTests
if %ERRORLEVEL% NEQ 0 (
    echo 打包失败！
    pause
    exit /b 1
)
echo.

echo [4/4] 安装到本地仓库...
call mvn install -DskipTests
if %ERRORLEVEL% NEQ 0 (
    echo 安装失败！
    pause
    exit /b 1
)
echo.

echo ========================================
echo 构建成功！
echo ========================================
echo.
echo 生成的文件：
dir /b service-a\target\*.jar
dir /b module-group\service-b\target\*.jar
echo.

echo 查看service-a的依赖树：
cd service-a
call mvn dependency:tree
cd ..
echo.

pause
