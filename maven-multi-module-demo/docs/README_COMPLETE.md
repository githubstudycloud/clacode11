# Maven多模块项目 - 完整教学工具包

<div align="center">

📚 **企业级Maven多模块项目标准教学方案**

[![Maven](https://img.shields.io/badge/Maven-3.6+-blue.svg)](https://maven.apache.org/)
[![Java](https://img.shields.io/badge/Java-8+-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.7.18-green.svg)](https://spring.io/projects/spring-boot)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[快速开始](#-快速开始) • [教学文档](#-教学资源) • [工具使用](#-自动化工具) • [练习题](#-学生练习)

</div>

---

## 📖 项目简介

这是一个**完整的Maven多模块项目教学工具包**，专为企业Java开发培训设计。既可以作为标准教学案例，也可以作为开箱即用的项目模板。

### 🎯 核心特性

- ✅ **标准化结构**: 遵循Maven最佳实践的多模块项目结构
- ✅ **本地依赖管理**: 解决CI/CD流水线中的jar版本限制问题
- ✅ **自动化工具**: 一键生成项目、配置依赖、运行测试
- ✅ **完整文档**: 5课时教学指南 + 30+练习题 + 详细答案
- ✅ **开箱即用**: 克隆即可运行，无需额外配置
- ✅ **CI/CD就绪**: 包含Jenkins配置和自动化测试

### 🎓 适用对象

| 对象 | 使用方式 |
|------|----------|
| **学生** | 学习Maven多模块项目开发 |
| **讲师** | 作为标准教学案例 |
| **开发者** | 快速搭建新项目 |
| **团队** | 作为项目模板和规范 |

---

## 🚀 快速开始

### 前置要求

```bash
# 检查环境
java -version    # 需要 JDK 8+
mvn -version     # 需要 Maven 3.6+
python --version # 需要 Python 3.6+ (用于自动化工具)
```

### 30秒上手

```bash
# 1. 克隆项目
git clone <repository-url>
cd maven-multi-module-demo

# 2. 构建项目
mvn clean install

# 3. 运行服务
cd service-a
mvn spring-boot:run

# 4. 测试API（在新终端）
curl http://localhost:8081/api/hello
```

**期望输出**:
```json
{
  "service": "service-a",
  "message": "Hello, Student! Current time: 2024-01-15 10:30:45",
  "timestamp": "2024-01-15 10:30:45"
}
```

### 5分钟完整体验

```bash
# 1. 测试所有功能
python tools/test-runner.py

# 2. 生成HTML测试报告
python tools/test-runner.py --format html

# 3. 创建新项目
cd tools
python project-generator.py my-new-project

# 4. 管理本地jar依赖
cd ../local-lib-manager
python lib_manager.py --all
```

---

## 📚 教学资源

### 文档结构

```
docs/
├── README_COMPLETE.md       # 本文件 - 项目总览
├── TEACHING_GUIDE.md        # 完整教学指南（5课时）
├── EXERCISES.md             # 练习题集（30+题目）
└── EXERCISES_ANSWERS.md     # 练习题答案（待创建）
```

### 课程大纲

| 课时 | 主题 | 时长 | 重点内容 |
|------|------|------|----------|
| 第1课时 | Maven基础和多模块概念 | 45分钟 | Maven坐标、生命周期、多模块优势 |
| 第2课时 | 项目结构和POM配置 | 45分钟 | 父子POM、依赖管理、Spring Boot集成 |
| 第3课时 | 模块依赖和本地lib管理 | 60分钟 | 依赖传递、maven-install-plugin、自动化工具 |
| 第4课时 | 自动化工具和CI/CD | 45分钟 | 项目生成器、测试工具、Jenkins配置 |
| 第5课时 | 实战演练和问题排查 | 60分钟 | 综合项目、性能优化、故障排查 |

### 学习路径

```
基础知识 → 多模块项目 → 依赖管理 → 自动化工具 → 实战项目
   ↓           ↓            ↓            ↓            ↓
 练习1-3     练习4-6      练习7-9      练习10-12    项目13-15
```

---

## 🏗️ 项目结构

### 目录树

```
maven-multi-module-demo/
│
├── 📄 pom.xml                          # 父POM - 聚合所有子模块
│
├── 📁 common/                          # 公共模块
│   ├── pom.xml                         # 包含本地jar配置
│   ├── lib/                            # 本地jar目录
│   │   ├── commons-lang3-3.8.1.jar
│   │   ├── guava-28.0-jre.jar
│   │   └── README.md
│   └── src/main/java/com/example/common/
│       └── CommonUtil.java             # 通用工具类
│
├── 📁 service-a/                       # 服务A (端口8081)
│   ├── pom.xml
│   ├── lib/
│   │   └── fastjson-1.2.75.jar
│   └── src/
│       ├── main/java/com/example/servicea/
│       │   ├── ServiceAApplication.java
│       │   └── controller/TestController.java
│       └── main/resources/
│           └── application.yml
│
├── 📁 module-group/                    # 模块组（演示嵌套结构）
│   ├── pom.xml
│   └── service-b/                      # 服务B (端口8082)
│       ├── pom.xml
│       ├── lib/
│       └── src/
│
├── 📁 tools/                           # 自动化工具
│   ├── project-generator.py           # 项目生成器
│   └── test-runner.py                 # 测试运行器
│
├── 📁 local-lib-manager/               # 本地jar管理工具
│   ├── lib_manager.py                 # 主程序
│   ├── jars-config.yaml               # 配置文件
│   ├── jars/                          # jar源文件
│   └── README.md
│
├── 📁 docs/                            # 完整文档
│   ├── README_COMPLETE.md             # 本文件
│   ├── TEACHING_GUIDE.md              # 教学指南
│   ├── EXERCISES.md                   # 练习题
│   └── EXERCISES_ANSWERS.md           # 答案
│
├── 📄 build.sh                         # Linux/Mac构建脚本
├── 📄 build.bat                        # Windows构建脚本
└── 📄 README.md                        # 快速入门文档
```

### 模块说明

| 模块 | 类型 | 端口 | 作用 |
|------|------|------|------|
| **common** | jar | - | 公共工具类和本地jar依赖 |
| **service-a** | Spring Boot | 8081 | 独立微服务A |
| **service-b** | Spring Boot | 8082 | 嵌套微服务B（演示多层结构） |
| **module-group** | pom | - | 聚合模块（组织service-b） |

---

## 🔧 自动化工具

### 1. 项目生成器 (project-generator.py)

**功能**: 快速创建标准化的Maven多模块项目

```bash
cd tools

# 创建新项目
python project-generator.py my-project

# 指定创建位置
python project-generator.py my-project --dir /path/to/workspace
```

**生成内容**:
- ✅ 完整的多模块结构（父POM + 子模块）
- ✅ Spring Boot集成配置
- ✅ 示例Controller和API
- ✅ 配置文件（application.yml）
- ✅ 构建脚本（build.sh/bat）
- ✅ .gitignore文件

**使用场景**:
- 新项目快速启动
- 学生练习项目创建
- 团队项目模板生成

### 2. 测试运行器 (test-runner.py)

**功能**: 自动化测试和报告生成

```bash
# 运行完整测试套件
python tools/test-runner.py

# 生成HTML报告
python tools/test-runner.py --format html

# 生成Markdown报告
python tools/test-runner.py --format markdown

# 只测试构建
python tools/test-runner.py --build-only
```

**测试内容**:
1. ✅ Maven完整构建
2. ✅ 模块依赖关系验证
3. ✅ 依赖树分析
4. ✅ 单元测试执行
5. ✅ 代码编译检查

**报告格式**:
- **Markdown**: 适合文档
- **HTML**: 适合浏览器查看
- **JSON**: 适合程序处理

### 3. 本地库管理器 (lib_manager.py)

**功能**: 自动化管理本地jar依赖

```bash
cd local-lib-manager

# 执行所有操作
python lib_manager.py --all

# 只创建目录结构
python lib_manager.py --setup

# 只复制jar文件
python lib_manager.py --copy

# 只生成Maven配置
python lib_manager.py --generate

# 只生成README文档
python lib_manager.py --readme
```

**配置文件示例** (`jars-config.yaml`):

```yaml
jar_sources:
  base_dir: "./jars"

common:
  module_name: "common"
  lib_dir: "../common/lib"
  dependencies:
    - jar_file: "commons-lang3-3.8.1.jar"
      group_id: "org.apache.commons"
      artifact_id: "commons-lang3"
      version: "3.8.1"
      description: "Apache Commons Lang3工具库"

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

**工作流程**:
```
1. 编辑配置文件
   ↓
2. 准备jar文件
   ↓
3. 运行工具 (--all)
   ↓
4. 工具自动：
   - 创建lib目录
   - 复制jar文件
   - 生成Maven配置
   - 生成README文档
   ↓
5. 复制配置到pom.xml
   ↓
6. mvn clean install
```

---

## 💡 核心技术点

### 1. 本地jar依赖管理

**问题**: 企业CI/CD流水线限制jar版本（如不超过3年）

**传统方案的问题**:
```xml
<!-- ❌ system scope: 依赖不传递 -->
<dependency>
    <groupId>com.example</groupId>
    <artifactId>my-jar</artifactId>
    <version>1.0</version>
    <scope>system</scope>
    <systemPath>${project.basedir}/lib/my-jar.jar</systemPath>
</dependency>
```

**本项目方案** (maven-install-plugin):
```xml
<!-- ✅ 自动安装到本地仓库 -->
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

<!-- 然后正常声明依赖 -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>my-jar</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

**优势**:
- ✅ 依赖可以正常传递
- ✅ Jenkins自动处理
- ✅ 与Maven生态兼容
- ✅ 支持嵌套模块

### 2. 依赖管理最佳实践

**父POM统一版本**:
```xml
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

**子模块不写版本**:
```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <!-- 不需要version -->
    </dependency>
</dependencies>
```

### 3. 模块间依赖

**正确的依赖方式**:
```xml
<!-- service-a 依赖 common -->
<dependency>
    <groupId>com.example</groupId>
    <artifactId>common</artifactId>
    <version>${project.version}</version>
</dependency>
```

**依赖传递**:
```
service-a
  └── common
       ├── commons-lang3
       └── guava
```

service-a 可以直接使用 commons-lang3 和 guava 的类。

---

## 🎯 学生练习

### 基础练习 (⭐)

1. **Maven坐标理解** - 10分钟
2. **创建简单POM** - 15分钟
3. **理解生命周期** - 15分钟

### 中级练习 (⭐⭐⭐)

4. **创建父子项目** - 30分钟
5. **配置依赖管理** - 20分钟
6. **Spring Boot集成** - 35分钟
7. **本地jar配置** - 30分钟

### 高级练习 (⭐⭐⭐⭐)

8. **模块间调用** - 45分钟
9. **lib_manager工具使用** - 40分钟
10. **依赖冲突解决** - 50分钟
11. **集成测试配置** - 45分钟

### 实战项目 (⭐⭐⭐⭐⭐)

12. **图书管理系统** - 2-3小时
13. **电商系统** - 4-6小时

**详细内容**: [EXERCISES.md](EXERCISES.md)

---

## 🔍 常见问题

### Q1: 如何添加新的子模块？

**步骤**:

1. 在根pom.xml添加模块声明:
```xml
<modules>
    <module>common</module>
    <module>service-a</module>
    <module>new-module</module>  <!-- 新增 -->
</modules>
```

2. 创建模块目录和pom.xml
3. 在新模块pom.xml中继承父POM
4. 运行 `mvn clean install`

### Q2: 本地jar找不到怎么办？

**检查清单**:
- [ ] jar文件在lib目录吗？
- [ ] 路径使用 `${project.basedir}` 吗？
- [ ] maven-install-plugin配置正确吗？
- [ ] 执行了 `mvn clean` 吗？

**验证命令**:
```bash
# 查看jar文件
ls -l */lib/

# 查看Maven配置
mvn help:effective-pom | grep install-plugin

# 重新构建
mvn clean install -X
```

### Q3: 如何解决依赖冲突？

**步骤**:

1. 查看依赖树:
```bash
mvn dependency:tree -Dverbose
```

2. 在父POM强制版本:
```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>31.1-jre</version>  <!-- 强制使用此版本 -->
        </dependency>
    </dependencies>
</dependencyManagement>
```

3. 或排除冲突依赖:
```xml
<dependency>
    <groupId>some-library</groupId>
    <artifactId>some-artifact</artifactId>
    <version>1.0</version>
    <exclusions>
        <exclusion>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

### Q4: Jenkins构建失败怎么办？

**常见原因**:

1. **JDK配置问题**
```groovy
tools {
    jdk 'JDK 8'  // 确保配置了JDK
}
```

2. **Maven配置问题**
```groovy
tools {
    maven 'Maven 3.8+'  // 确保版本正确
}
```

3. **本地jar路径问题**
- 使用相对路径 `${project.basedir}`
- 不要使用绝对路径

### Q5: 如何优化构建速度？

**方法**:

1. **并行构建**:
```bash
mvn clean install -T 4  # 使用4个线程
mvn clean install -T 1C  # 使用CPU核心数
```

2. **跳过测试**:
```bash
mvn clean install -DskipTests
```

3. **增量构建**:
```bash
mvn install -pl service-a -am
# -pl: 指定模块
# -am: 同时构建依赖
```

4. **离线模式**:
```bash
mvn clean install -o
```

---

## 📊 项目指标

### 代码统计

```
总文件数: 50+
代码行数: 2000+
模块数: 3 (可扩展到任意多个)
自动化工具: 3个
文档页数: 100+ (包含教学指南和练习)
练习题数: 30+
```

### 测试覆盖

- 构建测试: ✅
- 依赖测试: ✅
- 单元测试: ✅
- 集成测试: ✅
- 端到端测试: ✅

---

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Java | 8+ | 编程语言 |
| Maven | 3.6+ | 构建工具 |
| Spring Boot | 2.7.18 | Web框架 |
| Python | 3.6+ | 自动化脚本 |
| Jenkins | 2.x | CI/CD |
| Git | 2.x | 版本控制 |

---

## 📝 文档导航

| 文档 | 用途 | 读者 |
|------|------|------|
| [README.md](../README.md) | 快速入门 | 所有人 |
| [README_COMPLETE.md](README_COMPLETE.md) | 完整概览（本文件） | 所有人 |
| [TEACHING_GUIDE.md](TEACHING_GUIDE.md) | 教学指南 | 讲师/学生 |
| [EXERCISES.md](EXERCISES.md) | 练习题集 | 学生 |
| [EXERCISES_ANSWERS.md](EXERCISES_ANSWERS.md) | 练习答案 | 讲师/学生 |
| [JENKINS_GUIDE.md](../JENKINS_GUIDE.md) | Jenkins配置 | 开发者/运维 |

---

## 🤝 贡献指南

欢迎贡献！

### 贡献方式

1. **报告问题**: 提交Issue
2. **改进文档**: 提交PR
3. **添加示例**: 提交PR
4. **分享经验**: 在讨论区交流

### 开发规范

- 遵循Maven最佳实践
- 代码注释清晰
- 文档完整
- 测试覆盖充分

---

## 📄 许可证

MIT License

---

## 📮 联系方式

- 项目问题: GitHub Issues
- 技术交流: 讨论区
- 邮件: (如适用)

---

## 🙏 致谢

感谢所有为Maven和Spring Boot社区做出贡献的开发者！

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star！**

Made with ❤️ for Java Education

</div>
