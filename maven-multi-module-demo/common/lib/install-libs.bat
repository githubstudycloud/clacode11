@echo off
REM Windows批处理脚本 - 用于手动安装lib目录中的jar到Maven本地仓库

SET LIB_DIR=%~dp0

echo 开始安装本地lib到Maven仓库...
echo Lib目录: %LIB_DIR%

REM 示例：安装commons-lang3-3.8.1.jar
REM 将下面的示例替换为你实际的jar文件
REM
REM if exist "%LIB_DIR%commons-lang3-3.8.1.jar" (
REM     echo 安装 commons-lang3-3.8.1.jar...
REM     call mvn install:install-file ^
REM         -Dfile="%LIB_DIR%commons-lang3-3.8.1.jar" ^
REM         -DgroupId=org.apache.commons ^
REM         -DartifactId=commons-lang3 ^
REM         -Dversion=3.8.1 ^
REM         -Dpackaging=jar
REM ) else (
REM     echo 警告: commons-lang3-3.8.1.jar 不存在
REM )

REM 添加更多jar的安装命令
REM if exist "%LIB_DIR%another-lib-1.0.0.jar" (
REM     call mvn install:install-file ^
REM         -Dfile="%LIB_DIR%another-lib-1.0.0.jar" ^
REM         -DgroupId=com.example ^
REM         -DartifactId=another-lib ^
REM         -Dversion=1.0.0 ^
REM         -Dpackaging=jar
REM )

echo 安装完成！
pause
