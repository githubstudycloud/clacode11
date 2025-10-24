#!/bin/bash

# 本地lib安装脚本
# 用于手动安装lib目录中的jar到Maven本地仓库

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="${SCRIPT_DIR}"

echo "开始安装本地lib到Maven仓库..."
echo "Lib目录: ${LIB_DIR}"

# 示例：安装commons-lang3-3.8.1.jar
# 将下面的示例替换为你实际的jar文件
#
# if [ -f "${LIB_DIR}/commons-lang3-3.8.1.jar" ]; then
#     echo "安装 commons-lang3-3.8.1.jar..."
#     mvn install:install-file \
#         -Dfile="${LIB_DIR}/commons-lang3-3.8.1.jar" \
#         -DgroupId=org.apache.commons \
#         -DartifactId=commons-lang3 \
#         -Dversion=3.8.1 \
#         -Dpackaging=jar
# else
#     echo "警告: commons-lang3-3.8.1.jar 不存在"
# fi

# 添加更多jar的安装命令
# if [ -f "${LIB_DIR}/another-lib-1.0.0.jar" ]; then
#     mvn install:install-file \
#         -Dfile="${LIB_DIR}/another-lib-1.0.0.jar" \
#         -DgroupId=com.example \
#         -DartifactId=another-lib \
#         -Dversion=1.0.0 \
#         -Dpackaging=jar
# fi

echo "安装完成！"
