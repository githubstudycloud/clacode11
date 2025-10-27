# Maven多模块项目 - 完整教学指南

## 📚 课程概述

本教程将系统讲解Maven多模块项目的构建、管理和本地依赖解决方案，适合作为企业级Java开发的标准教学案例。

### 教学目标

学完本课程，学生将能够：

1. ✅ 理解Maven多模块项目的结构和设计原则
2. ✅ 掌握模块间依赖关系的配置
3. ✅ 解决本地jar依赖的集成问题
4. ✅ 配置Jenkins CI/CD流水线
5. ✅ 使用自动化工具管理项目
6. ✅ 应用最佳实践到实际项目中

### 课时安排

- **第1课时**: Maven基础和多模块概念 (45分钟)
- **第2课时**: 项目结构和POM配置 (45分钟)
- **第3课时**: 模块依赖和本地lib管理 (60分钟)
- **第4课时**: 自动化工具和CI/CD (45分钟)
- **第5课时**: 实战演练和问题排查 (60分钟)

---

## 第1课时: Maven基础和多模块概念

### 1.1 Maven核心概念

#### 什么是Maven？

Maven是一个项目管理和构建自动化工具，它使用POM（Project Object Model）来描述项目。

**核心特性**：
- 标准化的项目结构
- 依赖管理
- 构建生命周期
- 插件机制

#### Maven坐标系统

每个Maven项目都通过三个坐标唯一标识：

```xml
<groupId>com.example</groupId>        <!-- 组织/公司 -->
<artifactId>my-project</artifactId>   <!-- 项目名称 -->
<version>1.0.0-SNAPSHOT</version>     <!-- 版本号 -->
```

**版本说明**：
- `SNAPSHOT`: 开发版本，会自动更新
- `RELEASE`: 正式发布版本，不可变

### 1.2 为什么需要多模块？

#### 单模块项目的问题

```
my-monolith/
├── src/
│   ├── main/java/
│   │   ├── common/      ← 通用代码
│   │   ├── service1/    ← 服务1
│   │   └── service2/    ← 服务2
│   └── resources/
└── pom.xml
```

**缺点**：
- ❌ 所有代码耦合在一起
- ❌ 构建时间长（即使只改了一行）
- ❌ 无法独立部署
- ❌ 依赖关系不清晰

#### 多模块项目的优势

```
my-project/
├── common/          ← 公共模块
├── service-a/       ← 服务A
├── service-b/       ← 服务B
└── pom.xml         ← 父POM
```

**优点**：
- ✅ 职责分离，模块化
- ✅ 可以独立构建
- ✅ 依赖关系清晰
- ✅ 便于团队协作
- ✅ 支持微服务架构

### 1.3 多模块项目结构

#### 标准结构

```
maven-multi-module-demo/
├── pom.xml                    # 父POM（聚合器）
│
├── common/                    # 公共模块
│   ├── pom.xml               # 继承父POM
│   └── src/
│
├── service-a/                 # 服务模块A
│   ├── pom.xml               # 继承父POM，依赖common
│   └── src/
│
└── module-group/              # 模块组（嵌套结构）
    ├── pom.xml               # 聚合器POM
    └── service-b/            # 服务模块B
        ├── pom.xml
        └── src/
```

#### POM类型说明

| POM类型 | packaging | 作用 | 示例 |
|---------|-----------|------|------|
| 父POM | pom | 聚合多个模块，统一配置 | 根pom.xml |
| 模块POM | jar/war | 实际项目代码 | common/pom.xml |
| 聚合POM | pom | 组织多个子模块 | module-group/pom.xml |

### 1.4 实践：创建第一个多模块项目

#### 使用项目生成器

```bash
# 1. 进入tools目录
cd maven-multi-module-demo/tools

# 2. 运行生成器
python project-generator.py my-first-project

# 3. 查看生成的结构
cd my-first-project
tree  # Linux/Mac
# 或
dir /s  # Windows
```

#### 手动创建（理解原理）

**步骤1: 创建父项目**

```bash
mkdir my-project
cd my-project
```

创建 `pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-project</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>  <!-- 注意：是pom -->

    <modules>
        <module>common</module>
    </modules>
</project>
```

**步骤2: 创建子模块**

```bash
mkdir -p common/src/main/java/com/example/common
```

创建 `common/pom.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>  <!-- 继承父POM -->
        <groupId>com.example</groupId>
        <artifactId>my-project</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>

    <artifactId>common</artifactId>
    <packaging>jar</packaging>  <!-- 注意：是jar -->
</project>
```

**步骤3: 验证**

```bash
mvn clean install
```

### 1.5 课后练习

**练习1**: 创建项目
使用项目生成器创建一个名为 `student-project` 的多模块项目。

**练习2**: 理解POM
回答以下问题：
1. 父POM的packaging是什么？为什么？
2. `<modules>` 标签的作用是什么？
3. 子模块如何继承父POM的配置？

**练习3**: 修改配置
将Java版本从1.8改为11，观察需要修改哪些地方。

---

## 第2课时: 项目结构和POM配置

### 2.1 父POM详解

#### dependencyManagement vs dependencies

**dependencyManagement**: 只声明，不引入

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>2.7.18</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**作用**：
- 统一管理版本号
- 子模块不需要写版本号
- 避免版本冲突

**dependencies**: 声明并引入

```xml
<dependencies>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.12</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**作用**：
- 所有子模块自动继承
- 适合通用依赖（如日志）

#### pluginManagement vs plugins

同理：

```xml
<build>
    <pluginManagement>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.8.1</version>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                </configuration>
            </plugin>
        </plugins>
    </pluginManagement>
</build>
```

### 2.2 模块依赖关系

#### 声明模块依赖

在 `service-a/pom.xml` 中依赖 `common`:

```xml
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>common</artifactId>
        <version>${project.version}</version>
    </dependency>
</dependencies>
```

**关键点**：
- `${project.version}` 自动引用父POM版本
- Maven会自动处理构建顺序

#### 依赖传递

```
service-a
  └── common
       └── spring-boot-starter
            └── spring-core
```

**依赖范围（scope）**：

| Scope | 编译 | 测试 | 运行 | 传递 | 示例 |
|-------|------|------|------|------|------|
| compile | ✅ | ✅ | ✅ | ✅ | Spring |
| provided | ✅ | ✅ | ❌ | ❌ | Servlet API |
| runtime | ❌ | ✅ | ✅ | ✅ | MySQL驱动 |
| test | ❌ | ✅ | ❌ | ❌ | JUnit |
| system | ✅ | ✅ | ✅ | ❌ | 本地jar（不推荐） |

### 2.3 Spring Boot集成

#### 父POM配置

```xml
<properties>
    <spring-boot.version>2.7.18</spring-boot.version>
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

#### 服务模块配置

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <!-- 不需要写version，从父POM继承 -->
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>
```

### 2.4 实践：配置依赖关系

#### 练习：添加新模块

创建 `service-c` 模块，要求：
1. 依赖 `common` 模块
2. 使用 Spring Boot Web
3. 端口号 8083

**步骤**：

1. 修改根 `pom.xml`，添加模块：
```xml
<modules>
    <module>common</module>
    <module>service-a</module>
    <module>service-c</module>  <!-- 新增 -->
</modules>
```

2. 创建目录结构
3. 编写 `service-c/pom.xml`
4. 创建启动类和Controller
5. 配置 `application.yml`
6. 测试运行

### 2.5 依赖分析工具

#### 查看依赖树

```bash
# 查看所有依赖
mvn dependency:tree

# 查看特定模块
cd service-a
mvn dependency:tree

# 查看冲突
mvn dependency:tree -Dverbose
```

#### 分析依赖

```bash
# 分析未使用的依赖
mvn dependency:analyze

# 复制依赖到target/dependency
mvn dependency:copy-dependencies
```

### 2.6 课后练习

**练习1**: 依赖配置
为 `service-a` 添加以下依赖：
- MySQL驱动（runtime）
- Lombok（provided）
- JUnit（test）

**练习2**: 依赖传递
回答：如果 `common` 依赖 `guava`，`service-a` 是否可以直接使用 `guava` 的类？

**练习3**: 版本冲突
创建一个依赖冲突场景并解决它。

---

## 第3课时: 模块依赖和本地lib管理

### 3.1 本地jar依赖的挑战

#### 问题场景

企业开发中经常遇到：

1. **旧版本依赖**
   - 项目依赖 commons-lang3 3.8.1（5年前的版本）
   - CI/CD要求依赖不超过3年

2. **私有jar包**
   - 公司内部开发的jar
   - 无法发布到Maven中央仓库

3. **商业jar包**
   - 需要授权的第三方库
   - 不能放到公共仓库

#### 错误的解决方案

**❌ 方案1: system scope**

```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>my-jar</artifactId>
    <version>1.0</version>
    <scope>system</scope>
    <systemPath>${project.basedir}/lib/my-jar.jar</systemPath>
</dependency>
```

**问题**：
- 依赖不会传递
- 打包时不会包含
- IDE支持差

**❌ 方案2: 手动install**

```bash
mvn install:install-file \
  -Dfile=lib/my-jar.jar \
  -DgroupId=com.example \
  -DartifactId=my-jar \
  -Dversion=1.0 \
  -Dpackaging=jar
```

**问题**：
- 每个开发者都要手动执行
- Jenkins构建时需要额外配置
- 容易遗漏

### 3.2 正确的解决方案

#### maven-install-plugin 自动安装

**原理**：
在Maven构建的 `validate` 阶段自动将jar安装到本地仓库。

**配置示例**：

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-install-plugin</artifactId>
            <version>2.5.2</version>
            <executions>
                <execution>
                    <id>install-my-jar</id>
                    <phase>validate</phase>
                    <goals>
                        <goal>install-file</goal>
                    </goals>
                    <configuration>
                        <file>${project.basedir}/lib/my-jar.jar</file>
                        <groupId>com.example</groupId>
                        <artifactId>my-jar</artifactId>
                        <version>1.0.0</version>
                        <packaging>jar</packaging>
                        <generatePom>true</generatePom>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

**然后正常声明依赖**：

```xml
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>my-jar</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

### 3.3 工作流程

```
1. mvn clean install
   ↓
2. validate阶段
   ↓
3. maven-install-plugin执行
   ↓
4. lib/my-jar.jar → ~/.m2/repository/...
   ↓
5. compile阶段
   ↓
6. Maven从本地仓库找到依赖
   ↓
7. 编译成功！
```

### 3.4 使用 lib_manager 工具

#### 配置文件格式

`local-lib-manager/jars-config.yaml`:

```yaml
# jar文件源目录
jar_sources:
  base_dir: "./jars"

# 公共模块配置
common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "Apache Commons Lang3 工具库"

# 子模块配置
modules:
  - module_name: "service-a"
    lib_dir: "../service-a/lib"
    dependencies:
      - jar_file: "fastjson-1.2.75.jar"
        group_id: "com.alibaba"
        artifact_id: "fastjson"
        version: "1.2.75"
        description: "Alibaba FastJson"
```

#### 使用工具

```bash
cd local-lib-manager

# 1. 准备jar文件
# 将jar文件放到 jars/ 目录

# 2. 编辑配置文件
vim jars-config.yaml

# 3. 运行工具
python lib_manager.py --all

# 4. 工具会自动：
#    - 创建lib目录
#    - 复制jar文件
#    - 生成Maven配置
#    - 生成README文档
```

#### 应用生成的配置

```bash
# 查看生成的配置
cat generated-pom-configs.xml

# 复制到对应模块的pom.xml
# 按照注释说明添加到 <build><plugins> 和 <dependencies> 中
```

### 3.5 实践：集成本地jar

#### 练习：添加本地jar到common模块

**任务**：
为 `common` 模块添加 `guava-28.0-jre.jar`

**步骤**：

1. 下载jar文件
```bash
# 或者从Maven中央仓库下载
wget https://repo1.maven.org/maven2/com/google/guava/guava/28.0-jre/guava-28.0-jre.jar
```

2. 放到项目目录
```bash
cp guava-28.0-jre.jar local-lib-manager/jars/
```

3. 更新配置文件
```yaml
common:
  dependencies:
    - jar_file: "guava-28.0-jre.jar"
      group_id: "com.google.guava"
      artifact_id: "guava"
      version: "28.0-jre"
      description: "Google Guava工具库"
```

4. 运行工具
```bash
python lib_manager.py --all
```

5. 更新 `common/pom.xml`
   - 复制 plugin 配置
   - 复制 dependency 配置

6. 测试
```bash
mvn clean install
```

7. 在代码中使用
```java
import com.google.common.collect.Lists;

public class CommonUtil {
    public static void testGuava() {
        List<String> list = Lists.newArrayList("a", "b", "c");
        System.out.println(list);
    }
}
```

### 3.6 最佳实践

#### 1. 文档化

在 `lib/README.md` 中记录：
- jar文件来源
- 版本信息
- 使用原因
- 替换计划

示例：

```markdown
# Common模块本地依赖

## guava-28.0-jre.jar

- **来源**: Maven Central
- **版本**: 28.0-jre
- **使用原因**: 项目需要使用Guava的ImmutableList，但流水线不允许29.0以上版本
- **计划**: 2024年Q2升级到最新版本
- **风险**: 已知安全漏洞 CVE-xxx（低危）
```

#### 2. 版本控制

```bash
# 提交jar文件到Git
git add common/lib/*.jar
git commit -m "Add guava 28.0-jre to common lib"

# 不要忽略lib目录
# 在 .gitignore 中添加例外
!lib/*.jar
```

#### 3. 定期审查

```bash
# 每季度检查
1. 是否有新版本可用？
2. 是否有安全漏洞？
3. 是否可以移除？
```

### 3.7 课后练习

**练习1**: 完整流程
为 `service-a` 添加 `fastjson-1.2.75.jar`，完成整个流程。

**练习2**: 依赖传递验证
在 `service-a` 中验证是否可以使用 `common` 模块的 `guava`。

**练习3**: 问题排查
故意制造一个错误（如jar文件路径错误），观察错误信息并解决。

---

## 第4课时: 自动化工具和CI/CD

### 4.1 项目生成器

#### 工具说明

`tools/project-generator.py` 可以快速创建标准化的多模块项目。

#### 使用示例

```bash
# 创建新项目
python project-generator.py my-new-project

# 指定创建位置
python project-generator.py my-project --dir /path/to/workspace
```

#### 生成的内容

- ✅ 完整的Maven多模块结构
- ✅ Spring Boot集成
- ✅ 示例代码和Controller
- ✅ 配置文件
- ✅ 构建脚本
- ✅ .gitignore

### 4.2 自动化测试

#### 测试工具

`tools/test-runner.py` 提供全面的自动化测试。

#### 运行测试

```bash
cd maven-multi-module-demo

# 运行完整测试
python tools/test-runner.py

# 生成HTML报告
python tools/test-runner.py --format html

# 只测试构建
python tools/test-runner.py --build-only
```

#### 测试内容

1. ✅ Maven构建测试
2. ✅ 依赖关系验证
3. ✅ 单元测试执行
4. ✅ 依赖树分析
5. ✅ 生成详细报告

### 4.3 Jenkins集成

#### Jenkinsfile示例

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven 3.8+'
        jdk 'JDK 8'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean install -DskipTests'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Quality Check') {
            steps {
                sh 'mvn dependency:analyze'
            }
        }

        stage('Package') {
            steps {
                sh 'mvn package -DskipTests'
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: '**/target/*.jar'
                junit '**/target/surefire-reports/*.xml'
            }
        }
    }

    post {
        success {
            echo '构建成功！'
        }
        failure {
            echo '构建失败！'
        }
    }
}
```

#### 关键点说明

**1. 本地lib自动处理**

Maven构建时会自动执行 `validate` 阶段，无需额外配置。

**2. 依赖缓存**

Jenkins会缓存 `~/.m2/repository`，加速构建。

**3. 并行构建**

```groovy
stage('Test') {
    parallel {
        stage('Unit Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Integration Test') {
            steps {
                sh 'mvn verify -P integration-test'
            }
        }
    }
}
```

### 4.4 实践：配置Jenkins

#### 练习：创建Jenkins Job

**步骤**：

1. 新建Pipeline项目
2. 配置Git仓库
3. 添加Jenkinsfile
4. 配置Maven和JDK
5. 运行构建
6. 查看构建日志
7. 分析测试报告

### 4.5 课后练习

**练习1**: 自动化工具
使用项目生成器创建一个新项目，然后用测试工具验证。

**练习2**: Jenkins配置
在本地Jenkins环境中配置一个完整的CI流程。

**练习3**: 构建优化
研究如何减少构建时间（如依赖缓存、并行构建）。

---

## 第5课时: 实战演练和问题排查

### 5.1 完整项目实战

#### 任务：开发电商系统

**需求**：
- `common`: 通用工具类
- `user-service`: 用户服务 (8081)
- `product-service`: 商品服务 (8082)
- `order-service`: 订单服务 (8083)

**要求**：
1. 使用多模块结构
2. 集成Spring Boot
3. 使用本地jar（如 fastjson）
4. 配置Jenkins流水线
5. 编写测试用例

#### 实施步骤

参考完整示例代码：[练习答案](EXERCISES_ANSWERS.md)

### 5.2 常见问题排查

#### 问题1: 找不到common模块

**错误信息**：
```
[ERROR] Failed to execute goal on project service-a:
Could not resolve dependencies for project com.example:service-a:jar:1.0.0-SNAPSHOT:
Could not find artifact com.example:common:jar:1.0.0-SNAPSHOT
```

**原因**：
- common模块没有先构建
- 版本号不匹配

**解决**：
```bash
# 方案1: 从根目录构建
cd maven-multi-module-demo
mvn clean install

# 方案2: 先构建common
cd common
mvn clean install
cd ../service-a
mvn clean package
```

#### 问题2: 本地jar找不到

**错误信息**：
```
[ERROR] Failed to execute goal on project common:
Could not resolve dependencies:
Could not find artifact com.google.guava:guava:jar:28.0-jre
```

**检查清单**：
1. ✅ jar文件是否在 `lib/` 目录？
2. ✅ 路径是否使用 `${project.basedir}`？
3. ✅ maven-install-plugin 配置是否正确？
4. ✅ 是否执行了 `mvn clean`？

**解决**：
```bash
# 检查文件
ls -l common/lib/

# 手动验证安装
mvn install:install-file \
  -Dfile=common/lib/guava-28.0-jre.jar \
  -DgroupId=com.google.guava \
  -DartifactId=guava \
  -Dversion=28.0-jre \
  -Dpackaging=jar

# 重新构建
mvn clean install
```

#### 问题3: Jenkins构建失败

**错误信息**：
```
[ERROR] No compiler is provided in this environment
```

**原因**：
Jenkins使用JRE而不是JDK

**解决**：
```groovy
pipeline {
    tools {
        jdk 'JDK 8'  // 配置JDK而不是JRE
    }
}
```

#### 问题4: 依赖冲突

**错误信息**：
```
[WARNING] 'dependencies.dependency.version' for com.google.guava:guava:jar
is managed from 27.0-jre but was overridden to 28.0-jre
```

**解决**：
```xml
<!-- 在父POM的 dependencyManagement 中统一版本 -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>28.0-jre</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 5.3 性能优化

#### 1. 并行构建

```bash
# 使用多线程构建
mvn clean install -T 4

# 或使用CPU核心数
mvn clean install -T 1C
```

#### 2. 跳过测试

```bash
# 开发时跳过测试
mvn clean install -DskipTests

# 完全跳过测试编译
mvn clean install -Dmaven.test.skip=true
```

#### 3. 增量编译

```bash
# 只构建变化的模块
mvn install -pl service-a -am
# -pl: 指定模块
# -am: 同时构建依赖的模块
```

#### 4. 离线模式

```bash
# 使用本地仓库，不下载依赖
mvn clean install -o
```

### 5.4 最佳实践总结

#### 目录结构

```
✅ 好的结构：
maven-multi-module-demo/
├── common/                 # 公共模块在前
├── service-a/
├── service-b/
└── pom.xml

❌ 不好的结构：
my-project/
├── pom.xml
├── src/                   # 父POM不应该有src
└── modules/
    ├── common/
    └── service-a/
```

#### POM配置

```xml
✅ 使用properties
<properties>
    <guava.version>28.0-jre</guava.version>
</properties>

<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>${guava.version}</version>
</dependency>

❌ 硬编码版本号
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>28.0-jre</version>
</dependency>
```

#### 依赖管理

```
✅ 在父POM用 dependencyManagement
✅ 子模块不写version
✅ 公共依赖放在父POM的 dependencies

❌ 每个模块都声明版本
❌ 重复的依赖配置
```

### 5.5 综合练习

#### 期末项目：构建微服务系统

**要求**：

1. **架构设计** (30分)
   - 设计合理的模块结构
   - 明确模块职责
   - 绘制依赖关系图

2. **代码实现** (40分)
   - 使用项目生成器创建项目
   - 实现基本功能
   - 添加本地jar依赖
   - 编写单元测试

3. **CI/CD配置** (20分)
   - 编写Jenkinsfile
   - 配置自动化测试
   - 生成测试报告

4. **文档编写** (10分)
   - README说明
   - API文档
   - 部署文档

**提交内容**：
- 完整源代码
- Git仓库
- 测试报告
- 项目文档

---

## 附录

### A. Maven命令速查

| 命令 | 说明 |
|------|------|
| `mvn clean` | 清理target目录 |
| `mvn compile` | 编译代码 |
| `mvn test` | 运行测试 |
| `mvn package` | 打包 |
| `mvn install` | 安装到本地仓库 |
| `mvn deploy` | 发布到远程仓库 |
| `mvn dependency:tree` | 查看依赖树 |
| `mvn dependency:analyze` | 分析依赖 |
| `mvn help:effective-pom` | 查看有效POM |

### B. 常用插件

| 插件 | 用途 |
|------|------|
| maven-compiler-plugin | 编译代码 |
| maven-surefire-plugin | 运行测试 |
| maven-jar-plugin | 打包jar |
| maven-install-plugin | 安装jar |
| spring-boot-maven-plugin | Spring Boot打包 |

### C. 参考资料

- [Maven官方文档](https://maven.apache.org/)
- [Spring Boot文档](https://spring.io/projects/spring-boot)
- [项目GitHub仓库](链接)

---

## 总结

通过本课程，你已经学会了：

1. ✅ Maven多模块项目的设计和实现
2. ✅ 模块依赖关系的配置
3. ✅ 本地jar依赖的管理
4. ✅ 自动化工具的使用
5. ✅ CI/CD流水线的配置
6. ✅ 问题排查和性能优化

**下一步学习**：
- Docker容器化
- Kubernetes部署
- 微服务架构
- 分布式系统

**联系方式**：
- 项目问题：提交Issue
- 技术交流：加入讨论组
