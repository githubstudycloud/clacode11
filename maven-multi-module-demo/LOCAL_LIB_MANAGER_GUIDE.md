# 本地Jar依赖管理工具使用指南

本文档介绍如何使用 `local-lib-manager` 工具自动化管理Maven多模块项目中的本地jar依赖。

## 工具概述

`local-lib-manager` 是一个Python脚本工具，用于：

- ✅ 自动创建lib目录结构
- ✅ 批量复制jar文件到指定位置
- ✅ 自动生成maven-install-plugin配置
- ✅ 自动生成依赖声明
- ✅ 支持公共模块和子项目的私有依赖
- ✅ 自动生成文档

## 为什么需要这个工具？

### 问题场景

在Maven多模块项目中使用本地jar依赖时，你可能面临：

1. **手动配置繁琐**: 每个jar都需要在pom.xml中配置maven-install-plugin和dependency
2. **容易出错**: 手动配置容易遗漏或配置错误
3. **维护困难**: jar文件分散，难以统一管理
4. **文档缺失**: 没有清晰的依赖说明文档

### 解决方案

使用 `local-lib-manager` 工具：

```
配置一次 → 自动生成所有配置 → 一键应用
```

## 快速开始

### 前提条件

- Python 3.6+
- Maven项目

### 5分钟上手

#### 1. 进入工具目录

```bash
cd local-lib-manager
```

#### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

或者

```bash
pip install pyyaml
```

#### 3. 准备jar文件

将你的jar文件复制到 `jars` 目录：

```bash
cp /path/to/your-lib.jar jars/
```

#### 4. 配置依赖信息

编辑 `jars-config.yaml`：

```yaml
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "your-lib.jar"
      group_id: "com.example"
      artifact_id: "your-lib"
      version: "1.0.0"
      description: "你的库说明"
```

#### 5. 运行工具

```bash
# Windows
run.bat

# Linux/Mac
./run.sh

# 或直接使用Python
python lib_manager.py --all
```

#### 6. 应用配置

打开生成的 `generated-pom-configs.xml`，按照说明复制配置到对应模块的 pom.xml。

#### 7. 验证

```bash
cd ..
mvn clean install
```

## 详细使用说明

### 目录结构

```
local-lib-manager/
├── README.md                    # 完整使用文档
├── QUICKSTART.md               # 快速开始指南
├── INDEX.md                    # 文档导航
├── lib_manager.py              # 核心Python脚本
├── run.bat                     # Windows启动脚本
├── run.sh                      # Linux/Mac启动脚本
├── requirements.txt            # Python依赖
├── jars-config.yaml            # jar依赖配置
├── jars-config.example.yaml    # 配置示例
├── jars/                       # jar文件源目录
│   └── .gitkeep
└── .gitignore
```

### 配置文件详解

#### 基础结构

```yaml
# 项目信息
project:
  name: "maven-multi-module-demo"
  version: "1.0.0-SNAPSHOT"
  base_group: "com.example"

# 公共模块配置
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies: [...]

# 子项目配置
modules:
  - module_name: "service-a"
    lib_dir: "../service-a/lib"
    dependencies: [...]

# jar源目录
jar_sources:
  base_dir: "./jars"
```

#### 依赖配置项

```yaml
dependencies:
  - jar_file: "commons-lang3-3.8.1.jar"    # jar文件名
    group_id: "org.apache.commons"         # Maven GroupId
    artifact_id: "commons-lang3"           # Maven ArtifactId
    version: "3.8.1"                       # 版本号
    description: "Apache Commons Lang3"    # 说明（可选）
```

### 使用场景

#### 场景1: 为公共模块添加jar依赖

**适用**: 所有子项目都需要使用的jar

**步骤**:

1. 将jar放到 `local-lib-manager/jars/` 目录
2. 在 `jars-config.yaml` 的 `common.dependencies` 添加配置
3. 运行工具: `./run.sh` 或 `run.bat`
4. 复制生成的配置到 `common/pom.xml`

**示例配置**:

```yaml
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "公共工具库"
```

#### 场景2: 为子项目添加私有依赖

**适用**: 只有特定子项目需要的jar

**步骤**:

1. 将jar放到 `local-lib-manager/jars/` 目录
2. 在 `jars-config.yaml` 的 `modules` 添加子项目配置
3. 运行工具
4. 复制生成的配置到子项目的 `pom.xml`

**示例配置**:

```yaml
modules:
  - module_name: "service-a"
    lib_dir: "../service-a/lib"
    dependencies:
      - jar_file: "service-a-lib.jar"
        group_id: "com.example"
        artifact_id: "service-a-lib"
        version: "1.0.0"
        description: "Service A专用库"
```

#### 场景3: 批量添加多个jar

**步骤**:

1. 将所有jar放到 `jars/` 目录
2. 在配置文件中为每个jar添加配置
3. 运行工具一次性处理

**示例配置**:

```yaml
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "lib1.jar"
      group_id: "com.example"
      artifact_id: "lib1"
      version: "1.0.0"

    - jar_file: "lib2.jar"
      group_id: "com.example"
      artifact_id: "lib2"
      version: "2.0.0"

    - jar_file: "lib3.jar"
      group_id: "com.example"
      artifact_id: "lib3"
      version: "3.0.0"
```

### 工具命令

#### 一键运行（推荐）

```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

#### 分步执行

```bash
# 只创建目录
python lib_manager.py --setup

# 只复制jar文件
python lib_manager.py --copy

# 只生成Maven配置
python lib_manager.py --generate

# 只生成README文档
python lib_manager.py --readme

# 执行所有操作
python lib_manager.py --all
```

#### 自定义配置文件

```bash
python lib_manager.py --config my-config.yaml --all
```

#### 自定义输出路径

```bash
python lib_manager.py --generate --output my-pom-configs.xml
```

### 生成的文件

#### 1. generated-pom-configs.xml

包含所有模块的Maven配置，格式如下：

```xml
<!-- ========== 公共模块 (common) ========== -->

<!-- 第1步: 添加到 <build><plugins> 中 -->
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-install-plugin</artifactId>
  <version>2.5.2</version>
  <executions>
    <execution>
      <id>install-your-lib</id>
      <phase>validate</phase>
      <goals>
        <goal>install-file</goal>
      </goals>
      <configuration>
        <file>${project.basedir}/lib/your-lib.jar</file>
        <groupId>com.example</groupId>
        <artifactId>your-lib</artifactId>
        <version>1.0.0</version>
        <packaging>jar</packaging>
        <generatePom>true</generatePom>
      </configuration>
    </execution>
  </executions>
</plugin>

<!-- 第2步: 添加到 <dependencies> 中 -->
<dependency>
  <groupId>com.example</groupId>
  <artifactId>your-lib</artifactId>
  <version>1.0.0</version>
</dependency>
```

#### 2. 各lib目录的README.md

工具会在每个lib目录生成README.md，包含：

- 依赖清单表格
- 使用说明
- 验证方法

### 应用配置到pom.xml

#### 步骤1: 打开生成的配置文件

```bash
cat generated-pom-configs.xml
# 或在编辑器中打开
```

#### 步骤2: 找到对应模块的配置

文件中会按模块分组，找到你需要的模块配置。

#### 步骤3: 复制plugin配置

复制 `<plugin>...</plugin>` 部分到模块 pom.xml 的 `<build><plugins>` 中：

```xml
<build>
  <plugins>
    <!-- 其他插件... -->

    <!-- 从generated-pom-configs.xml复制的plugin配置 -->
    <plugin>
      <groupId>org.apache.maven.plugins</groupId>
      <artifactId>maven-install-plugin</artifactId>
      ...
    </plugin>
  </plugins>
</build>
```

#### 步骤4: 复制dependency配置

复制 `<dependency>...</dependency>` 部分到模块 pom.xml 的 `<dependencies>` 中：

```xml
<dependencies>
  <!-- 其他依赖... -->

  <!-- 从generated-pom-configs.xml复制的dependency配置 -->
  <dependency>
    <groupId>com.example</groupId>
    <artifactId>your-lib</artifactId>
    <version>1.0.0</version>
  </dependency>
</dependencies>
```

### 验证配置

#### 1. 构建项目

```bash
cd ..  # 返回项目根目录
mvn clean install
```

#### 2. 检查依赖树

```bash
cd common
mvn dependency:tree

cd ../service-a
mvn dependency:tree
```

#### 3. 查看安装的jar

```bash
ls -la ~/.m2/repository/com/example/your-lib/
```

## 最佳实践

### 1. 命名规范

**GroupId**:
- 使用反向域名格式: `com.example`, `org.apache`
- 保持与项目GroupId一致或相关

**ArtifactId**:
- 使用小写字母和连字符: `custom-lib`, `vendor-sdk`
- 与jar文件名相关

**Version**:
- 使用语义化版本: `1.0.0`, `2.1.3-SNAPSHOT`
- 与jar实际版本保持一致

### 2. 依赖管理

**公共vs私有**:
- 多个模块使用 → 配置在 `common`
- 单个模块使用 → 配置在 `modules`

**文档记录**:
- 为每个jar添加清晰的 `description`
- 记录jar的来源和用途
- 定期审查和更新

### 3. 版本控制

**提交到Git**:
```bash
git add local-lib-manager/
git add common/lib/
git add service-a/lib/
git commit -m "Add local jar dependencies"
```

**忽略生成的文件**:
- `generated-pom-configs.xml` 不需要提交（已在.gitignore中）
- 配置文件和jar文件需要提交

### 4. 后续替换计划

1. 定期检查jar是否有Maven中央仓库版本
2. 测试新版本的兼容性
3. 逐步替换为标准Maven依赖
4. 从配置文件移除已替换的jar

## 故障排查

### 问题1: ModuleNotFoundError: No module named 'yaml'

**原因**: 未安装PyYAML库

**解决**:
```bash
pip install pyyaml
```

### 问题2: 找不到jar文件

**检查**:
- jar文件是否在 `jars/` 目录
- 配置中的 `jar_file` 名称是否正确
- 路径是否正确

**解决**:
```bash
ls -la jars/
# 确认jar文件存在
```

### 问题3: Maven构建找不到依赖

**检查**:
- pom.xml是否正确复制了配置
- lib目录是否有jar文件
- 路径是否使用 `${project.basedir}/lib/`

**解决**:
```bash
# 查看详细日志
mvn -X clean install

# 检查lib目录
ls -la common/lib/
```

### 问题4: YAML语法错误

**常见错误**:
- 使用Tab而不是空格
- 缩进不一致
- 冒号后没有空格

**解决**:
```bash
# 使用YAML验证工具
python -c "import yaml; yaml.safe_load(open('jars-config.yaml'))"
```

### 问题5: 子项目找不到common的依赖

**原因**: 可能使用了system scope

**解决**:
- 使用maven-install-plugin（本工具默认方式）
- 确保common模块正确构建
- 子项目正确依赖common模块

## 工作流程

```
┌─────────────────────────────────────────┐
│ 1. 准备jar文件                          │
│    cp *.jar local-lib-manager/jars/    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│ 2. 配置依赖信息                         │
│    编辑 jars-config.yaml               │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│ 3. 运行工具                            │
│    ./run.sh 或 run.bat                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│ 4. 自动处理                            │
│    ✓ 创建lib目录                       │
│    ✓ 复制jar文件                       │
│    ✓ 生成Maven配置                     │
│    ✓ 生成README文档                    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│ 5. 应用配置                            │
│    复制配置到pom.xml                   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│ 6. 验证构建                            │
│    mvn clean install                   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│ 7. 提交代码                            │
│    git add . && git commit             │
└─────────────────────────────────────────┘
```

## 与Jenkins集成

### Jenkins中使用

在Jenkins流水线中，工具生成的配置会在 `mvn clean install` 时自动生效：

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                // 构建时会自动安装lib中的jar
                sh 'mvn clean install'
            }
        }
    }
}
```

### 优势

- ✅ 无需在Jenkins中额外配置
- ✅ jar文件随代码一起管理
- ✅ 构建过程完全自动化
- ✅ 支持多环境部署

详细的Jenkins配置请参考: [JENKINS_GUIDE.md](JENKINS_GUIDE.md)

## 相关文档

### 工具文档
- [完整使用文档](local-lib-manager/README.md)
- [快速开始指南](local-lib-manager/QUICKSTART.md)
- [文档导航](local-lib-manager/INDEX.md)
- [配置示例](local-lib-manager/jars-config.example.yaml)

### 项目文档
- [项目主README](README.md)
- [Jenkins配置指南](JENKINS_GUIDE.md)
- [项目结构说明](PROJECT_STRUCTURE.txt)
- [使用示例](USAGE_EXAMPLE.md)

## 总结

`local-lib-manager` 工具提供了一个标准化、自动化的方式来管理Maven多模块项目中的本地jar依赖。

**优势**:
- 🚀 快速配置，5分钟上手
- ⚙️ 自动化处理，减少人工错误
- 📋 统一管理，易于维护
- 📖 自动生成文档，清晰明了
- 🔄 支持批量操作
- 🌳 支持多模块结构

**适用场景**:
- 需要使用不符合版本要求的旧jar
- 使用供应商提供的私有jar
- 暂时无法从Maven中央仓库获取的jar
- 需要快速集成本地jar到项目

立即开始使用: [QUICKSTART.md](local-lib-manager/QUICKSTART.md)

## License

MIT License
