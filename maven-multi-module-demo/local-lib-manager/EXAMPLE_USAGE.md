# 使用示例 - 实战演练

这个文档通过实际示例演示如何使用本工具管理本地jar依赖。

## 示例1: 为公共模块添加一个jar

### 场景说明
common模块需要使用 `commons-lang3-3.8.1.jar`（旧版本）

### 操作步骤

#### 1. 准备jar文件
```bash
# 将jar文件复制到jars目录
cp /path/to/commons-lang3-3.8.1.jar jars/

# 验证文件存在
ls -lh jars/
# 输出: -rw-r--r-- 1 user 501K commons-lang3-3.8.1.jar
```

#### 2. 编辑配置文件
编辑 `jars-config.yaml`:

```yaml
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "Apache Commons Lang3 旧版本，用于兼容旧系统"
```

#### 3. 运行工具
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

#### 4. 查看生成结果
```bash
# 检查lib目录
ls -lh ../common/lib/
# 输出:
# -rw-r--r-- 1 user 501K commons-lang3-3.8.1.jar
# -rw-r--r-- 1 user 1.5K README.md

# 查看生成的配置
cat generated-pom-configs.xml
```

#### 5. 应用配置到pom.xml
复制 `generated-pom-configs.xml` 中的配置到 `common/pom.xml`:

```xml
<!-- 在 <build><plugins> 中添加 -->
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

<!-- 在 <dependencies> 中添加 -->
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-lang3</artifactId>
  <version>3.8.1</version>
</dependency>
```

#### 6. 验证构建
```bash
cd ..
mvn clean install

# 查看依赖树
cd common
mvn dependency:tree | grep commons-lang3
# 输出: [INFO] +- org.apache.commons:commons-lang3:jar:3.8.1:compile
```

### 完成！✓

---

## 示例2: 为子项目添加私有依赖

### 场景说明
service-a 需要使用 Oracle JDBC 驱动

### 操作步骤

#### 1. 准备jar文件
```bash
cp /path/to/ojdbc6-11.2.0.4.jar jars/
```

#### 2. 编辑配置文件
在 `jars-config.yaml` 中添加:

```yaml
modules:
  - module_name: "service-a"
    lib_dir: "../service-a/lib"
    dependencies:
      - jar_file: "ojdbc6-11.2.0.4.jar"
        group_id: "com.oracle.database.jdbc"
        artifact_id: "ojdbc6"
        version: "11.2.0.4"
        description: "Oracle JDBC驱动，用于连接Oracle 11g数据库"
```

#### 3. 运行工具
```bash
python lib_manager.py --all
```

#### 4. 应用配置
复制生成的配置到 `service-a/pom.xml`

#### 5. 验证
```bash
cd ../service-a
mvn dependency:tree | grep ojdbc
```

---

## 示例3: 批量添加多个jar

### 场景说明
需要同时添加3个jar到common模块

### 准备文件
```bash
# 复制多个jar文件
cp /libs/commons-lang3-3.8.1.jar jars/
cp /libs/guava-28.0-jre.jar jars/
cp /libs/fastjson-1.2.75.jar jars/
```

### 配置文件
```yaml
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "Apache Commons Lang3"

    - jar_file: "guava-28.0-jre.jar"
      group_id: "com.google.guava"
      artifact_id: "guava"
      version: "28.0-jre"
      description: "Google Guava库"

    - jar_file: "fastjson-1.2.75.jar"
      group_id: "com.alibaba"
      artifact_id: "fastjson"
      version: "1.2.75"
      description: "Alibaba FastJson"
```

### 一键处理
```bash
./run.sh
```

工具会：
- ✓ 创建 common/lib/ 目录
- ✓ 复制3个jar文件
- ✓ 生成3个jar的Maven配置
- ✓ 生成README文档

---

## 示例4: 嵌套模块的私有依赖

### 场景说明
module-group/service-b 需要使用 JasperReports

### 配置
```yaml
modules:
  - module_name: "module-group/service-b"
    lib_dir: "../module-group/service-b/lib"
    dependencies:
      - jar_file: "jasperreports-5.6.0.jar"
        group_id: "net.sf.jasperreports"
        artifact_id: "jasperreports"
        version: "5.6.0"
        description: "JasperReports报表库"
```

### 特点
- 支持多层嵌套路径
- 自动处理相对路径
- 生成正确的目录结构

---

## 示例5: 混合配置（公共+私有）

### 完整场景
- common: 2个公共jar
- service-a: 1个私有jar
- service-b: 1个私有jar

### 完整配置
```yaml
project:
  name: "maven-multi-module-demo"
  version: "1.0.0-SNAPSHOT"
  base_group: "com.example"

# 公共依赖
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "Apache Commons Lang3"

    - jar_file: "guava-28.0-jre.jar"
      group_id: "com.google.guava"
      artifact_id: "guava"
      version: "28.0-jre"
      description: "Google Guava"

# 私有依赖
modules:
  - module_name: "service-a"
    lib_dir: "../service-a/lib"
    dependencies:
      - jar_file: "ojdbc6-11.2.0.4.jar"
        group_id: "com.oracle.database.jdbc"
        artifact_id: "ojdbc6"
        version: "11.2.0.4"
        description: "Oracle JDBC驱动"

  - module_name: "module-group/service-b"
    lib_dir: "../module-group/service-b/lib"
    dependencies:
      - jar_file: "jasperreports-5.6.0.jar"
        group_id: "net.sf.jasperreports"
        artifact_id: "jasperreports"
        version: "5.6.0"
        description: "JasperReports报表"

jar_sources:
  base_dir: "./jars"
```

### 运行结果
```
=== 创建目录结构 ===
✓ 创建jar源目录: .../jars
✓ 创建公共模块lib目录: .../common/lib
✓ 创建模块lib目录: .../service-a/lib
✓ 创建模块lib目录: .../module-group/service-b/lib

=== 复制JAR文件 ===
✓ [公共模块] 复制: commons-lang3-3.8.1.jar
✓ [公共模块] 复制: guava-28.0-jre.jar
✓ [模块 service-a] 复制: ojdbc6-11.2.0.4.jar
✓ [模块 module-group/service-b] 复制: jasperreports-5.6.0.jar

=== 生成Maven配置 ===
✓ Maven配置已生成: generated-pom-configs.xml

=== 生成README文件 ===
✓ 生成README: .../common/lib/README.md
✓ 生成README: .../service-a/lib/README.md
✓ 生成README: .../module-group/service-b/lib/README.md
```

---

## 示例6: 只更新配置不复制文件

### 场景
jar文件已经在lib目录，只需要重新生成配置

### 命令
```bash
python lib_manager.py --generate
```

### 结果
只生成 `generated-pom-configs.xml`，不复制文件

---

## 示例7: 分步操作

### 场景
需要逐步完成每个操作

### 命令序列
```bash
# 1. 只创建目录
python lib_manager.py --setup

# 2. 只复制jar
python lib_manager.py --copy

# 3. 只生成配置
python lib_manager.py --generate

# 4. 只生成README
python lib_manager.py --readme
```

---

## 常见错误示例

### 错误1: jar文件不存在

**配置**:
```yaml
dependencies:
  - jar_file: "non-existent.jar"
```

**输出**:
```
✗ [公共模块] 源文件不存在: .../jars/non-existent.jar
```

**解决**: 确保jar文件在jars目录

### 错误2: YAML语法错误

**错误配置**:
```yaml
dependencies:
	- jar_file: "test.jar"  # 使用了Tab
```

**输出**:
```
错误: while scanning for the next token
found character '\t' that cannot start any token
```

**解决**: 使用空格而不是Tab

### 错误3: 缺少必需字段

**错误配置**:
```yaml
dependencies:
  - jar_file: "test.jar"
    # 缺少group_id
```

**输出**:
```
KeyError: 'group_id'
```

**解决**: 添加所有必需字段

---

## 完整工作流示例

### 从头到尾的完整操作

```bash
# 1. 进入工具目录
cd local-lib-manager

# 2. 安装依赖
pip install -r requirements.txt

# 3. 准备jar文件
mkdir -p jars
cp /path/to/*.jar jars/

# 4. 编辑配置
vim jars-config.yaml

# 5. 运行工具
./run.sh

# 6. 查看生成结果
cat generated-pom-configs.xml
ls -la ../common/lib/

# 7. 应用配置
# 复制配置到 common/pom.xml

# 8. 验证构建
cd ..
mvn clean install

# 9. 查看依赖
cd common
mvn dependency:tree

# 10. 提交代码
git add local-lib-manager/ common/lib/ common/pom.xml
git commit -m "Add local jar dependencies"
git push
```

---

## 故障排查示例

### 问题: Python模块未找到

```bash
$ python lib_manager.py
Traceback: ModuleNotFoundError: No module named 'yaml'

# 解决
$ pip install pyyaml
```

### 问题: 配置文件不存在

```bash
$ python lib_manager.py --all
FileNotFoundError: jars-config.yaml

# 解决
$ cp jars-config.example.yaml jars-config.yaml
$ vim jars-config.yaml
```

### 问题: Maven找不到依赖

```bash
$ mvn clean install
[ERROR] Failed to execute goal ... could not resolve dependencies

# 检查
$ ls common/lib/
$ grep -A5 "maven-install-plugin" common/pom.xml

# 确认配置正确复制到pom.xml
```

---

## 总结

本文档展示了7个实际使用场景和3个故障排查示例，涵盖：

- ✅ 单个jar添加
- ✅ 批量jar添加
- ✅ 公共依赖配置
- ✅ 私有依赖配置
- ✅ 混合依赖配置
- ✅ 嵌套模块处理
- ✅ 分步操作
- ✅ 错误处理

通过这些示例，你应该能够轻松使用本工具管理你的本地jar依赖。

**下一步**: 参考 [README.md](README.md) 了解更多详细信息。
