# Maven本地Jar依赖管理工具

这是一个用于自动化管理Maven多模块项目中本地jar依赖的Python工具。

## 功能特性

- ✅ 自动根据配置创建lib目录结构
- ✅ 批量复制jar文件到指定位置
- ✅ 自动生成maven-install-plugin配置
- ✅ 自动生成依赖声明配置
- ✅ 支持公共模块和子项目私有依赖
- ✅ 自动生成每个lib目录的README文档
- ✅ 使用YAML配置文件，易于维护

## 快速开始

### 1. 环境要求

- Python 3.6+
- PyYAML库

安装依赖：

```bash
pip install pyyaml
```

### 2. 准备jar文件

将你需要的jar文件放到 `jars` 目录：

```bash
# 创建jars目录
mkdir jars

# 复制jar文件
cp /path/to/your-lib-1.0.0.jar jars/
cp /path/to/another-lib-2.0.0.jar jars/
```

### 3. 配置依赖信息

编辑 `jars-config.yaml`，添加你的jar依赖配置：

```yaml
# 公共模块的本地jar依赖
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "Apache Commons Lang3 旧版本"

# 子项目的私有依赖
modules:
  - module_name: "service-a"
    lib_dir: "../service-a/lib"
    dependencies:
      - jar_file: "service-a-specific-lib.jar"
        group_id: "com.example"
        artifact_id: "service-a-lib"
        version: "1.0.0"
        description: "Service A专用库"
```

### 4. 运行工具

```bash
# 执行所有操作（推荐）
python lib_manager.py --all

# 或者分步执行
python lib_manager.py --setup      # 创建目录
python lib_manager.py --copy       # 复制jar
python lib_manager.py --generate   # 生成配置
python lib_manager.py --readme     # 生成README
```

### 5. 应用配置

工具会生成 `generated-pom-configs.xml` 文件，按照文件中的说明：

1. 复制对应模块的 `<plugin>` 配置到该模块 pom.xml 的 `<build><plugins>` 中
2. 复制对应模块的 `<dependency>` 配置到该模块 pom.xml 的 `<dependencies>` 中

### 6. 验证配置

```bash
# 返回项目根目录
cd ..

# 构建项目
mvn clean install

# 查看依赖树验证
cd service-a
mvn dependency:tree
```

## 目录结构

```
local-lib-manager/
├── README.md                    # 本文件
├── lib_manager.py              # 主程序脚本
├── jars-config.yaml            # jar依赖配置文件
├── jars/                       # jar文件源目录
│   ├── commons-lang3-3.8.1.jar
│   └── your-custom-lib.jar
└── generated-pom-configs.xml   # 生成的Maven配置（运行后）
```

## 配置文件说明

### jars-config.yaml 结构

```yaml
# 项目基础信息
project:
  name: "项目名称"
  version: "版本号"
  base_group: "基础GroupId"

# 公共模块配置
common:
  module_name: "common"           # 模块名称
  lib_dir: "../common/lib"        # lib目录路径（相对于本工具目录）
  dependencies:
    - jar_file: "jar文件名.jar"    # jar文件名
      group_id: "GroupId"          # Maven GroupId
      artifact_id: "ArtifactId"    # Maven ArtifactId
      version: "版本号"             # 版本
      description: "描述信息"       # 可选的描述

# 子项目配置（可配置多个）
modules:
  - module_name: "service-a"
    lib_dir: "../service-a/lib"
    dependencies:
      - jar_file: "xxx.jar"
        group_id: "com.example"
        artifact_id: "xxx"
        version: "1.0.0"
        description: "说明"

  # 支持嵌套模块
  - module_name: "module-group/service-b"
    lib_dir: "../module-group/service-b/lib"
    dependencies:
      - jar_file: "yyy.jar"
        group_id: "com.example"
        artifact_id: "yyy"
        version: "2.0.0"

# jar源目录配置
jar_sources:
  base_dir: "./jars"  # jar文件存放的源目录
```

## 命令行参数

```bash
python lib_manager.py [OPTIONS]

选项：
  --config PATH     配置文件路径（默认：jars-config.yaml）
  --all            执行所有操作
  --setup          只创建目录结构
  --copy           只复制jar文件
  --generate       只生成Maven配置
  --readme         只生成README文件
  --output PATH    指定配置输出文件路径
  -h, --help       显示帮助信息
```

## 使用场景示例

### 场景1：为公共模块添加本地jar

假设你有一个旧版本的 `commons-lang3-3.8.1.jar` 需要在common模块中使用：

1. 将jar文件放到 `jars/` 目录
2. 在 `jars-config.yaml` 的 `common.dependencies` 中添加配置
3. 运行 `python lib_manager.py --all`
4. 将生成的配置复制到 `common/pom.xml`

### 场景2：为子项目添加私有依赖

假设 service-a 需要一个专用的库：

1. 将jar文件放到 `jars/` 目录
2. 在 `jars-config.yaml` 的 `modules` 中添加 service-a 的配置
3. 运行 `python lib_manager.py --all`
4. 将生成的配置复制到 `service-a/pom.xml`

### 场景3：批量添加多个jar

1. 将所有jar文件放到 `jars/` 目录
2. 在配置文件中为每个jar添加配置项
3. 运行 `python lib_manager.py --all`
4. 按模块将生成的配置复制到对应的 pom.xml

### 场景4：只更新配置不复制文件

如果jar文件已经在lib目录中，只需要重新生成配置：

```bash
python lib_manager.py --generate
```

## 生成的文件说明

运行工具后会生成以下文件：

### 1. generated-pom-configs.xml

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
      <id>install-commons-lang3</id>
      <phase>validate</phase>
      <goals>
        <goal>install-file</goal>
      </goals>
      <configuration>
        <file>${project.basedir}/lib/commons-lang3-3.8.1.jar</file>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.8.1</version>
        <packaging>jar</packaging>
        <generatePom>true</generatePom>
      </configuration>
    </execution>
  </executions>
</plugin>

<!-- 第2步: 添加到 <dependencies> 中 -->
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-lang3</artifactId>
  <version>3.8.1</version>
</dependency>
```

### 2. 各模块lib目录的README.md

每个lib目录会生成一个README.md，包含：
- 依赖清单表格
- 使用说明
- 验证方法
- 注意事项

## 工作流程

```
1. 准备jar文件
   ↓
2. 编辑jars-config.yaml
   ↓
3. 运行 lib_manager.py
   ↓
4. 自动创建lib目录
   ↓
5. 自动复制jar文件
   ↓
6. 生成Maven配置
   ↓
7. 生成README文档
   ↓
8. 手动复制配置到pom.xml
   ↓
9. 运行 mvn clean install
   ↓
10. 验证构建成功
```

## 优势特点

1. **自动化**: 一键完成所有配置生成
2. **标准化**: 统一的配置格式和目录结构
3. **可维护**: YAML配置易于理解和修改
4. **可追溯**: 自动生成的README记录所有依赖
5. **灵活**: 支持公共依赖和私有依赖
6. **兼容**: 完全兼容Maven生态和Jenkins CI

## 注意事项

1. **提交jar到Git**: 生成的lib目录和jar文件需要提交到Git仓库
2. **配置文件管理**: jars-config.yaml 也应该提交到仓库
3. **版本号**: 确保配置的版本号与jar文件实际版本一致
4. **路径使用**: 配置中使用相对路径，确保在不同环境都能工作
5. **依赖冲突**: 注意本地jar与Maven中央仓库的版本冲突
6. **定期审查**: 定期检查是否可以用标准Maven依赖替换本地jar

## 故障排查

### 问题1: ModuleNotFoundError: No module named 'yaml'

**解决方案**：
```bash
pip install pyyaml
```

### 问题2: 找不到jar文件

**检查**：
- jar文件是否在 `jars/` 目录
- 配置文件中的 jar_file 名称是否正确

### 问题3: Maven构建找不到依赖

**检查**：
- 是否将生成的配置正确复制到了 pom.xml
- lib目录中是否有对应的jar文件
- 路径是否使用 `${project.basedir}/lib/xxx.jar`

### 问题4: 子项目找不到common的依赖

**解决方案**：
使用maven-install-plugin（本工具生成的方式）而不是system scope，
这样依赖会自动传递。

## 完整示例

查看 [jars-config.example.yaml](jars-config.example.yaml) 获取完整配置示例。

## 后续改进计划

- [ ] 支持从远程仓库下载jar
- [ ] 支持从本地Maven仓库导出jar
- [ ] 自动检测jar的GroupId/ArtifactId
- [ ] 生成安装脚本（.sh/.bat）
- [ ] 支持配置模板生成

## 许可证

MIT License

## 相关文档

- [项目主README](../README.md)
- [Jenkins配置指南](../JENKINS_GUIDE.md)
- [使用示例](../USAGE_EXAMPLE.md)
