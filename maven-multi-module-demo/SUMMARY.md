# 项目总结文档

## 📋 项目概述

本项目演示了如何在Maven多模块项目中使用本地lib目录来绕过Jenkins流水线的jar版本检查（3年内发布要求），同时保持所有子项目能够正常访问这些依赖。

## 🎯 解决的核心问题

1. **流水线检查绕过**：公共项目需要使用不符合版本要求的jar包
2. **依赖传递**：其他子项目需要访问这些依赖
3. **嵌套项目支持**：支持多层级的子项目结构
4. **Jenkins兼容**：确保在CI/CD环境中正常工作

## 🏗️ 项目结构

```
maven-multi-module-demo/
├── pom.xml                                    # 根POM
├── README.md                                  # 主要说明文档
├── JENKINS_GUIDE.md                           # Jenkins详细配置指南
├── USAGE_EXAMPLE.md                           # 实际使用示例
├── SUMMARY.md                                 # 本文档
├── test-build.sh / .bat                       # 构建测试脚本
│
├── common/                                    # 🔑 核心公共模块
│   ├── pom.xml                                # 包含本地jar安装配置
│   ├── lib/                                   # 本地jar存放目录
│   │   ├── README.md                          # lib使用说明
│   │   ├── install-libs.sh / .bat            # 手动安装脚本
│   │   └── (你的jar文件放这里)
│   ├── pom-with-local-jar-example.xml        # 完整配置示例
│   └── src/main/java/com/example/common/
│       └── CommonUtil.java                    # 公共工具类
│
├── service-a/                                 # 子项目A（直接在根下）
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/example/servicea/
│       │   ├── ServiceAApplication.java       # Spring Boot应用
│       │   └── controller/TestController.java # 测试控制器
│       └── resources/application.yml          # 配置文件
│
└── module-group/                              # 📁 模块组（嵌套结构）
    ├── pom.xml                                # 中间层POM
    └── service-b/                             # 嵌套子项目B
        ├── pom.xml
        └── src/
            ├── main/java/com/example/serviceb/
            │   ├── ServiceBApplication.java   # Spring Boot应用
            │   └── controller/TestController.java
            └── resources/application.yml
```

## 💡 核心解决方案

### 方案：maven-install-plugin自动安装（推荐）

**原理流程：**

```
1. 将jar文件放入 common/lib/ 目录
         ↓
2. 在common/pom.xml配置maven-install-plugin
         ↓
3. Maven构建时在validate阶段自动执行
         ↓
4. 将lib/*.jar安装到本地Maven仓库
         ↓
5. 后续编译阶段可以正常使用这些依赖
         ↓
6. 其他子项目通过依赖common模块获得依赖
         ↓
7. 所有模块构建成功 ✓
```

**配置示例：**

```xml
<!-- common/pom.xml -->
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-install-plugin</artifactId>
            <version>2.5.2</version>
            <executions>
                <execution>
                    <id>install-your-jar</id>
                    <phase>validate</phase>
                    <goals><goal>install-file</goal></goals>
                    <configuration>
                        <file>${project.basedir}/lib/your-jar.jar</file>
                        <groupId>com.example</groupId>
                        <artifactId>your-jar</artifactId>
                        <version>1.0.0</version>
                        <packaging>jar</packaging>
                        <generatePom>true</generatePom>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>

<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>your-jar</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

## ✅ 方案优势

1. **自动化处理**
   - Jenkins构建时自动安装jar到本地仓库
   - 无需手动操作或额外脚本

2. **依赖传递**
   - 子项目只需依赖common模块
   - lib中的依赖自动传递到所有子项目

3. **环境兼容**
   - 使用相对路径（`${project.basedir}`）
   - 在本地、Jenkins、Docker等任何环境都能工作

4. **嵌套支持**
   - 支持任意层级的子项目嵌套
   - Maven自动解析相对路径

5. **易于维护**
   - 所有jar集中在common/lib目录
   - 配置清晰，易于理解和修改

## 📝 使用步骤（快速开始）

### 1. 准备jar文件
```bash
cp /path/to/your-old-dependency.jar common/lib/
```

### 2. 配置common/pom.xml
参考 `common/pom-with-local-jar-example.xml` 添加配置

### 3. 构建测试
```bash
mvn clean install
```

### 4. 验证依赖
```bash
cd service-a
mvn dependency:tree | grep your-dependency
```

## 🚀 Jenkins集成

### 标准Jenkinsfile

```groovy
pipeline {
    agent any
    tools {
        maven 'Maven 3.8.6'
        jdk 'JDK 8'
    }
    stages {
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
    }
}
```

**工作原理：**
1. Jenkins从Git拉取代码（包含common/lib目录）
2. 执行 `mvn clean install`
3. validate阶段自动将lib/*.jar安装到Jenkins的本地仓库
4. 所有模块正常编译、测试、打包

## 📊 技术栈

- **Java**: 1.8
- **Spring Boot**: 2.7.18
- **Maven**: 3.6+
- **构建工具**: Maven (不需要Gradle)

## 🔍 关键文件说明

| 文件 | 用途 |
|------|------|
| `README.md` | 项目主要说明和快速入门 |
| `JENKINS_GUIDE.md` | Jenkins详细配置指南，包含三种方案对比 |
| `USAGE_EXAMPLE.md` | 实际使用示例，包含完整代码 |
| `common/lib/README.md` | lib目录使用说明和注意事项 |
| `common/pom-with-local-jar-example.xml` | 完整的配置示例 |
| `test-build.sh/.bat` | 自动化测试脚本 |

## ⚠️ 重要注意事项

### 1. Git提交
**必须**将lib目录下的jar文件提交到Git：
```bash
git add common/lib/*.jar
git commit -m "Add local lib dependencies"
```

### 2. 路径使用
**始终**使用 `${project.basedir}` 相对路径：
```xml
<file>${project.basedir}/lib/your-jar.jar</file>
```

### 3. 依赖传递
**避免**使用 `<scope>system</scope>`，使用推荐的maven-install-plugin方案

### 4. 子项目配置
子项目**只需**依赖common模块：
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>common</artifactId>
    <version>${project.version}</version>
</dependency>
```

## 🎓 学习资源

### 项目内文档
1. 先读：`README.md` - 了解项目整体
2. 详细配置：`JENKINS_GUIDE.md` - Jenkins完整配置
3. 实战示例：`USAGE_EXAMPLE.md` - 实际操作步骤
4. Lib说明：`common/lib/README.md` - lib目录使用方法

### 验证命令
```bash
# 查看依赖树
mvn dependency:tree

# 查看有效POM
mvn help:effective-pom

# 清理并重新构建
mvn clean install -X  # -X 显示详细日志
```

## 🔧 常见问题快速索引

| 问题 | 解决方案 | 参考文档 |
|------|----------|----------|
| Jenkins找不到jar | 检查Git提交和路径配置 | JENKINS_GUIDE.md |
| 子项目找不到依赖 | 使用maven-install-plugin | JENKINS_GUIDE.md |
| 嵌套项目构建失败 | 检查相对路径配置 | USAGE_EXAMPLE.md |
| 依赖没有传递 | 避免system scope | README.md |

## 📈 后续优化建议

### 短期（临时方案）
1. ✅ 使用本地lib绕过流水线检查
2. ✅ 在代码中添加TODO注释
3. ✅ 记录在lib/README.md中

### 中期（逐步替换）
1. 🔄 识别可升级的依赖
2. 🔄 测试新版本兼容性
3. 🔄 逐个替换为标准Maven依赖

### 长期（规范化）
1. 🎯 所有依赖使用符合要求的版本
2. 🎯 移除lib目录和特殊配置
3. 🎯 恢复标准Maven项目结构

## 📞 支持和反馈

如果遇到问题：
1. 查看对应的文档章节
2. 检查常见问题解答
3. 查看Maven详细日志（`mvn -X`）
4. 参考项目中的示例配置

## 📄 许可证

MIT License

---

**项目创建日期**: 2025-10-24
**最后更新**: 2025-10-24
**Spring Boot版本**: 2.7.18
**Java版本**: 1.8
