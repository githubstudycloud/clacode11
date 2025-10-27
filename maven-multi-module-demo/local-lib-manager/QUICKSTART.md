# 快速开始指南

5分钟快速配置本地jar依赖！

## 步骤1: 安装Python依赖（1分钟）

```bash
pip install pyyaml
```

## 步骤2: 准备jar文件（1分钟）

将你的jar文件复制到 `jars` 目录：

```bash
# 示例
cp /path/to/commons-lang3-3.8.1.jar jars/
```

## 步骤3: 配置依赖（2分钟）

编辑 `jars-config.yaml`：

```yaml
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "旧版本依赖"
```

## 步骤4: 运行工具（30秒）

```bash
python lib_manager.py --all
```

工具会自动：
- ✅ 创建lib目录
- ✅ 复制jar文件
- ✅ 生成Maven配置
- ✅ 生成README文档

## 步骤5: 应用配置（1分钟）

打开 `generated-pom-configs.xml`，复制对应模块的配置到 `pom.xml`：

1. 复制 `<plugin>` 部分到 `<build><plugins>` 中
2. 复制 `<dependency>` 部分到 `<dependencies>` 中

## 步骤6: 验证（30秒）

```bash
cd ..
mvn clean install
```

构建成功！🎉

## 常见问题

### Q: Python环境问题？

```bash
# 检查Python版本（需要3.6+）
python --version

# 或使用python3
python3 lib_manager.py --all
```

### Q: 配置文件报错？

- 检查YAML缩进（使用空格，不要用Tab）
- 确保jar文件名正确
- 参考 `jars-config.example.yaml` 示例

### Q: Maven构建失败？

- 检查pom.xml配置是否正确复制
- 确保lib目录中有对应的jar文件
- 运行 `mvn -X clean install` 查看详细日志

## 下一步

- 查看完整文档: [README.md](README.md)
- 查看配置示例: [jars-config.example.yaml](jars-config.example.yaml)
- 了解项目集成: [../README.md](../README.md)

## 帮助

运行以下命令查看所有选项：

```bash
python lib_manager.py --help
```
