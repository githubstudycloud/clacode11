# 本地Jar依赖管理工具 - 文档导航

## 快速导航

### 🚀 我是新手
- **立即开始**: [QUICKSTART.md](QUICKSTART.md) - 5分钟快速上手
- **完整文档**: [README.md](README.md) - 详细使用说明

### 📋 配置文件
- **当前配置**: [jars-config.yaml](jars-config.yaml) - 你的jar依赖配置
- **配置示例**: [jars-config.example.yaml](jars-config.example.yaml) - 完整配置示例

### 🛠️ 工具脚本
- **Python脚本**: [lib_manager.py](lib_manager.py) - 核心管理工具
- **Windows脚本**: [run.bat](run.bat) - Windows一键运行
- **Linux/Mac脚本**: [run.sh](run.sh) - Linux/Mac一键运行

### 📦 目录说明
- **jar源目录**: [jars/](jars/) - 存放需要导入的jar文件
- **生成的配置**: `generated-pom-configs.xml` - 运行工具后生成

## 目录结构

```
local-lib-manager/
├── README.md                    # 📖 完整使用文档
├── QUICKSTART.md               # 🚀 5分钟快速开始
├── INDEX.md                    # 📚 本文件
│
├── lib_manager.py              # 🐍 核心Python脚本
├── run.bat                     # 🪟 Windows启动脚本
├── run.sh                      # 🐧 Linux/Mac启动脚本
├── requirements.txt            # 📦 Python依赖
│
├── jars-config.yaml            # ⚙️ jar依赖配置文件
├── jars-config.example.yaml    # 📝 配置示例文件
│
├── jars/                       # 📦 jar文件源目录
│   └── .gitkeep                # （将jar文件放这里）
│
└── generated-pom-configs.xml   # 🎯 生成的Maven配置（运行后）
```

## 使用流程

```
┌─────────────────────┐
│  1. 准备jar文件      │
│  放到 jars/ 目录     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  2. 编辑配置文件     │
│  jars-config.yaml   │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  3. 运行工具         │
│  run.bat / run.sh   │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  4. 复制生成的配置   │
│  到 pom.xml         │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  5. 验证构建         │
│  mvn clean install  │
└─────────────────────┘
```

## 功能特性

| 功能 | 说明 |
|------|------|
| 🗂️ 目录管理 | 自动创建lib目录结构 |
| 📋 批量复制 | 批量复制jar到指定位置 |
| ⚙️ 配置生成 | 自动生成maven-install-plugin配置 |
| 📖 文档生成 | 自动生成README文档 |
| 🌳 多模块支持 | 支持公共和私有依赖 |
| 🔧 灵活配置 | YAML格式配置文件 |

## 常用命令

### 快速使用（推荐）

```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### 分步操作

```bash
# 只创建目录
python lib_manager.py --setup

# 只复制jar
python lib_manager.py --copy

# 只生成配置
python lib_manager.py --generate

# 只生成README
python lib_manager.py --readme

# 执行所有操作
python lib_manager.py --all
```

## 配置示例

### 最简配置

```yaml
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "your-lib.jar"
      group_id: "com.example"
      artifact_id: "your-lib"
      version: "1.0.0"

jar_sources:
  base_dir: "./jars"
```

### 完整配置

参考 [jars-config.example.yaml](jars-config.example.yaml)

## 场景示例

### 场景1: 为公共模块添加jar

1. 复制jar到 `jars/` 目录
2. 在配置文件的 `common.dependencies` 添加配置
3. 运行 `run.bat` 或 `run.sh`
4. 复制生成的配置到 `common/pom.xml`

### 场景2: 为子项目添加私有jar

1. 复制jar到 `jars/` 目录
2. 在配置文件的 `modules` 添加子项目配置
3. 运行工具
4. 复制生成的配置到子项目的 `pom.xml`

### 场景3: 批量添加多个jar

1. 将所有jar放到 `jars/` 目录
2. 在配置文件中逐个添加配置
3. 运行工具一次性处理所有jar

## 文档详情

### [README.md](README.md)
完整的使用文档，包括：
- 功能特性详解
- 完整使用流程
- 配置文件详细说明
- 命令行参数说明
- 使用场景示例
- 故障排查指南

**适合**: 需要深入了解工具的用户

### [QUICKSTART.md](QUICKSTART.md)
快速开始指南，包括：
- 6个步骤快速上手
- 每个步骤所需时间
- 常见问题快速解答

**适合**: 新手用户快速入门

### [jars-config.example.yaml](jars-config.example.yaml)
完整配置示例，包括：
- 所有配置选项说明
- 多个实际示例
- 配置字段说明
- 最佳实践建议

**适合**: 作为配置参考

## 依赖关系

```
lib_manager.py
     ├── 读取: jars-config.yaml
     ├── 读取: jars/*.jar
     │
     ├── 生成: ../common/lib/
     ├── 生成: ../service-a/lib/
     ├── 生成: ../module-group/service-b/lib/
     │
     ├── 生成: generated-pom-configs.xml
     └── 生成: 各模块lib/README.md
```

## 工作原理

1. **读取配置**: 解析 `jars-config.yaml`
2. **创建目录**: 创建各模块的 `lib` 目录
3. **复制文件**: 从 `jars/` 复制到各模块 `lib/`
4. **生成配置**: 生成 `maven-install-plugin` XML配置
5. **生成文档**: 为每个lib目录生成README

## 注意事项

⚠️ **重要**:
1. 配置文件使用YAML格式，注意缩进（使用空格）
2. jar文件必须先放到 `jars/` 目录
3. 生成的配置需要手动复制到 pom.xml
4. lib目录和jar文件应该提交到Git

✅ **建议**:
1. 为每个jar添加清晰的description
2. 定期审查是否可以用Maven中央仓库版本替换
3. 保持配置文件和README文档更新
4. 验证构建成功后再提交代码

## 相关链接

### 项目文档
- [项目主README](../README.md)
- [Jenkins配置指南](../JENKINS_GUIDE.md)
- [项目结构说明](../PROJECT_STRUCTURE.txt)
- [使用示例](../USAGE_EXAMPLE.md)

### 外部资源
- [Maven Install Plugin文档](https://maven.apache.org/plugins/maven-install-plugin/)
- [PyYAML文档](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Python官网](https://www.python.org/)

## 获取帮助

### 1. 查看文档
- 基础问题: [QUICKSTART.md](QUICKSTART.md)
- 详细说明: [README.md](README.md)
- 配置问题: [jars-config.example.yaml](jars-config.example.yaml)

### 2. 查看帮助信息
```bash
python lib_manager.py --help
```

### 3. 查看日志
运行工具时会显示详细的处理过程和错误信息

### 4. 常见问题
- Python环境: 确保安装Python 3.6+
- 依赖问题: 运行 `pip install -r requirements.txt`
- 配置错误: 检查YAML语法和缩进
- jar未找到: 确认jar文件在 `jars/` 目录

## 更新日志

- **v1.0** (2024-10-27): 初始版本
  - 基础功能实现
  - 支持公共和私有依赖
  - 自动生成配置和文档
  - Windows/Linux/Mac支持

## 许可证

MIT License

---

**返回**: [项目主页](../README.md) | **开始使用**: [QUICKSTART.md](QUICKSTART.md)
