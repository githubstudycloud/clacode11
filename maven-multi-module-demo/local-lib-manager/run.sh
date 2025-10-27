#!/bin/bash
# Maven本地Jar依赖管理工具 - Linux/Mac启动脚本
#
# 使用方法：
#   ./run.sh              - 执行所有操作
#   ./run.sh setup        - 只创建目录
#   ./run.sh copy         - 只复制jar
#   ./run.sh generate     - 只生成配置
#   ./run.sh readme       - 只生成README

set -e

echo "================================================"
echo " Maven本地Jar依赖管理工具"
echo "================================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python 3.6+"
    echo ""
    echo "安装方法:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "  macOS:         brew install python3"
    exit 1
fi

# 显示Python版本
echo "[信息] 检测到Python版本:"
python3 --version
echo ""

# 检查依赖
echo "[信息] 检查Python依赖..."
if ! python3 -c "import yaml" &> /dev/null; then
    echo "[警告] 未安装pyyaml库，正在安装..."
    pip3 install pyyaml
    echo "[成功] pyyaml安装完成"
    echo ""
fi

# 检查配置文件
if [ ! -f "jars-config.yaml" ]; then
    echo "[警告] 未找到配置文件 jars-config.yaml"
    echo "[信息] 正在从示例文件创建..."
    cp jars-config.example.yaml jars-config.yaml
    echo "[成功] 已创建配置文件，请编辑 jars-config.yaml 后再次运行"
    echo ""
    exit 0
fi

# 执行Python脚本
case "$1" in
    "setup")
        echo "[信息] 创建目录结构..."
        python3 lib_manager.py --setup
        ;;
    "copy")
        echo "[信息] 复制jar文件..."
        python3 lib_manager.py --copy
        ;;
    "generate")
        echo "[信息] 生成Maven配置..."
        python3 lib_manager.py --generate
        ;;
    "readme")
        echo "[信息] 生成README文件..."
        python3 lib_manager.py --readme
        ;;
    "")
        echo "[信息] 执行所有操作..."
        python3 lib_manager.py --all
        ;;
    *)
        echo "[错误] 未知参数: $1"
        echo ""
        echo "支持的参数:"
        echo "  setup     - 创建目录结构"
        echo "  copy      - 复制jar文件"
        echo "  generate  - 生成Maven配置"
        echo "  readme    - 生成README文件"
        echo "  (空)      - 执行所有操作"
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo " 处理完成！"
    echo "================================================"
    echo ""
    echo "下一步操作:"
    echo "1. 查看生成的 generated-pom-configs.xml"
    echo "2. 将配置复制到对应模块的 pom.xml"
    echo "3. 运行 mvn clean install 验证"
    echo ""
else
    echo ""
    echo "[错误] 处理失败，请查看错误信息"
    echo ""
    exit 1
fi
