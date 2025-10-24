# Maven多模块项目 - 本地Lib依赖解决方案

## 项目概述

这是一个演示如何在Maven多模块项目中使用本地lib目录来绕过流水线版本检查的完整示例。

### 适用场景

- 公共项目中有不符合流水线版本要求（3年内）的jar依赖
- 暂时无法立即替换这些依赖，但需要发布重要功能
- Jenkins流水线会检查整个根代码仓库
- 项目包含多层嵌套的子模块结构

## 项目结构

```
maven-multi-module-demo/
├── pom.xml                                    # 根POM，定义所有子模块
├── README.md                                  # 本文件
├── JENKINS_GUIDE.md                           # Jenkins配置详细指南
│
├── common/                                    # 公共模块（核心）
│   ├── pom.xml                                # 包含本地jar安装配置
│   ├── lib/                                   # 本地jar存放目录
│   │   ├── README.md                          # lib使用说明
│   │   ├── install-libs.sh                    # Linux/Mac安装脚本
│   │   └── install-libs.bat                   # Windows安装脚本
│   ├── pom-with-local-jar-example.xml        # 完整配置示例
│   └── src/main/java/com/example/common/
│       └── CommonUtil.java                    # 公共工具类
│
├── service-a/                                 # 子项目A
│   ├── pom.xml                                # 依赖common模块
│   └── src/main/java/com/example/servicea/
│       ├── ServiceAApplication.java           # Spring Boot主类
│       └── controller/TestController.java     # 测试控制器
│
└── module-group/                              # 模块组（嵌套结构）
    ├── pom.xml                                # 中间层POM
    └── service-b/                             # 嵌套子项目B
        ├── pom.xml                            # 也依赖common模块
        └── src/main/java/com/example/serviceb/
            ├── ServiceBApplication.java       # Spring Boot主类
            └── controller/TestController.java # 测试控制器
```

## 快速开始

### 1. 准备本地jar文件

将你需要的jar文件复制到 `common/lib/` 目录：

```bash
cp /path/to/your-old-dependency.jar common/lib/
```

### 2. 配置Maven依赖

编辑 `common/pom.xml`，参考 `common/pom-with-local-jar-example.xml` 添加配置：

```xml
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
                    <goals>
                        <goal>install-file</goal>
                    </goals>
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

### 3. 构建项目

```bash
cd maven-multi-module-demo

# 清理并构建整个项目
mvn clean install

# 或者只构建某个模块
cd service-a
mvn clean package
```

### 4. 运行测试

```bash
# 运行service-a
cd service-a
mvn spring-boot:run

# 在另一个终端运行service-b
cd module-group/service-b
mvn spring-boot:run
```

测试接口：
- Service-A: http://localhost:8081/api/hello
- Service-B: http://localhost:8082/api/hello

## 核心解决方案

### 方案：maven-install-plugin自动安装（推荐）

**原理**：
1. 将jar文件放在 `common/lib/` 目录
2. 在 `common/pom.xml` 配置maven-install-plugin
3. 构建时在validate阶段自动将jar安装到本地Maven仓库
4. 其他模块通过依赖common模块间接获得这些依赖

**优点**：
- ✅ 依赖可以正常传递到子模块
- ✅ 与Maven生态完全兼容
- ✅ Jenkins构建时自动处理，无需额外配置
- ✅ 支持多层嵌套的子项目结构
- ✅ 使用相对路径，在任何环境都能工作

**工作流程**：
```
Jenkins拉取代码
    ↓
执行 mvn clean install
    ↓
validate阶段：common/lib/*.jar → 本地Maven仓库
    ↓
compile阶段：使用已安装的依赖编译common模块
    ↓
其他子模块：通过依赖common获得所有依赖
    ↓
构建成功 ✓
```

## 子项目如何使用

子项目（service-a、service-b）不需要任何特殊配置，只需正常依赖common模块：

```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>common</artifactId>
    <version>${project.version}</version>
</dependency>
```

common模块中的所有依赖（包括lib中的jar）会自动传递。

## Jenkins配置

详细的Jenkins配置请参考 [JENKINS_GUIDE.md](JENKINS_GUIDE.md)

### 简单的Jenkinsfile

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven 3.8+'
        jdk 'JDK 8'
    }

    stages {
        stage('Build') {
            steps {
                sh 'mvn clean install'
            }
        }
    }
}
```

## 验证依赖

### 查看依赖树

```bash
# 查看service-a的完整依赖
cd service-a
mvn dependency:tree

# 查看service-b的完整依赖
cd module-group/service-b
mvn dependency:tree
```

### 验证jar是否正确加载

```bash
# 构建并查看打包的jar
mvn clean package
jar -tf service-a/target/service-a-1.0.0-SNAPSHOT.jar | grep "your-dependency"
```

## 技术栈

- Java 8
- Spring Boot 2.7.18
- Maven 3.6+

## 注意事项

1. **提交lib目录到Git**
   ```bash
   git add common/lib/*.jar
   git commit -m "Add local dependencies"
   ```

2. **路径使用**
   - 始终使用 `${project.basedir}` 而不是绝对路径
   - Maven会自动解析嵌套项目的相对路径

3. **版本管理**
   - 在lib/README.md中记录每个jar的信息
   - 定期审查和替换旧依赖

4. **依赖传递**
   - 使用maven-install-plugin确保依赖可以传递
   - 避免使用system scope

## 后续替换计划

1. 识别可以升级的依赖
2. 测试新版本的兼容性
3. 逐步替换lib中的jar为正常的Maven依赖
4. 移除maven-install-plugin配置
5. 删除lib目录中的旧jar

## 故障排查

### 问题1：构建时找不到jar
**解决**：检查jar文件是否在lib目录，路径是否使用 `${project.basedir}`

### 问题2：子项目找不到common的依赖
**解决**：确保使用maven-install-plugin而非system scope

### 问题3：Jenkins构建失败
**解决**：查看 [JENKINS_GUIDE.md](JENKINS_GUIDE.md) 的详细说明

## 联系和支持

有问题请参考：
- [JENKINS_GUIDE.md](JENKINS_GUIDE.md) - Jenkins详细配置
- [common/lib/README.md](common/lib/README.md) - Lib目录使用说明
- [common/pom-with-local-jar-example.xml](common/pom-with-local-jar-example.xml) - 完整配置示例

## License

MIT License
