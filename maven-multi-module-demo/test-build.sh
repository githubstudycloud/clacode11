#!/bin/bash

# Linux/Mac构建测试脚本

echo "========================================"
echo "Maven多模块项目构建测试"
echo "========================================"
echo

echo "[1/4] 清理项目..."
mvn clean
if [ $? -ne 0 ]; then
    echo "清理失败！"
    exit 1
fi
echo

echo "[2/4] 编译项目..."
mvn compile -DskipTests
if [ $? -ne 0 ]; then
    echo "编译失败！"
    exit 1
fi
echo

echo "[3/4] 打包项目..."
mvn package -DskipTests
if [ $? -ne 0 ]; then
    echo "打包失败！"
    exit 1
fi
echo

echo "[4/4] 安装到本地仓库..."
mvn install -DskipTests
if [ $? -ne 0 ]; then
    echo "安装失败！"
    exit 1
fi
echo

echo "========================================"
echo "构建成功！"
echo "========================================"
echo
echo "生成的文件："
ls -lh service-a/target/*.jar
ls -lh module-group/service-b/target/*.jar
echo

echo "查看service-a的依赖树："
cd service-a
mvn dependency:tree
cd ..
echo
