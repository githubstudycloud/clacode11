# Jenkins流水线配置指南

## 项目结构说明

```
maven-multi-module-demo/
├── pom.xml                    # 根POM
├── common/                    # 公共模块
│   ├── pom.xml
│   ├── lib/                   # 本地jar存放目录（关键）
│   │   └── README.md
│   └── src/
├── service-a/                 # 子项目A（直接依赖common）
│   ├── pom.xml
│   └── src/
└── module-group/              # 模块组
    ├── pom.xml
    └── service-b/             # 嵌套子项目B（也依赖common）
        ├── pom.xml
        └── src/
```

## 核心解决方案

### 问题
- 公共项目（common）中的某些jar版本不符合流水线3年内版本要求
- 暂时无法立即替换这些依赖
- 需要绕过流水线检查，但不影响其他子项目的正常构建

### 解决方案：三种方法

#### 方法1：使用 system scope（最简单，但有局限性）

在 `common/pom.xml` 中：

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.8.1</version>
        <scope>system</scope>
        <!-- 关键：使用相对路径，确保Jenkins能找到 -->
        <systemPath>${project.basedir}/lib/commons-lang3-3.8.1.jar</systemPath>
    </dependency>
</dependencies>
```

**优点**：
- 简单直接
- 不需要额外配置

**缺点**：
- system scope的依赖不会传递到其他模块
- 打包时可能需要额外处理
- Maven 3.9+ 可能会有警告

#### 方法2：使用 maven-install-plugin 自动安装（推荐）

在 `common/pom.xml` 中：

```xml
<build>
    <plugins>
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
                        <!-- 可选：安装到自定义本地仓库 -->
                        <!-- <localRepositoryPath>${project.basedir}/../.m2/repository</localRepositoryPath> -->
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>

<dependencies>
    <!-- 然后正常引用依赖 -->
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.8.1</version>
    </dependency>
</dependencies>
```

**优点**：
- 依赖可以正常传递到其他模块
- 与Maven生态完全兼容
- Jenkins构建时会在validate阶段自动安装jar到本地仓库

**工作流程**：
1. Jenkins从Git拉取代码（包含common/lib目录）
2. 执行 `mvn clean install`
3. validate阶段：自动将lib/*.jar安装到Jenkins的本地Maven仓库
4. 后续构建：其他模块可以正常引用这些依赖

#### 方法3：使用项目内本地仓库（适合多个jar）

在根 `pom.xml` 中添加：

```xml
<repositories>
    <repository>
        <id>project-local-repo</id>
        <url>file://${project.basedir}/common/lib-repo</url>
    </repository>
</repositories>
```

创建目录结构：
```
common/lib-repo/
└── org/
    └── apache/
        └── commons/
            └── commons-lang3/
                └── 3.8.1/
                    ├── commons-lang3-3.8.1.jar
                    └── commons-lang3-3.8.1.pom
```

使用Maven命令安装jar到项目仓库：
```bash
mvn install:install-file \
  -Dfile=commons-lang3-3.8.1.jar \
  -DgroupId=org.apache.commons \
  -DartifactId=commons-lang3 \
  -Dversion=3.8.1 \
  -Dpackaging=jar \
  -DlocalRepositoryPath=./common/lib-repo
```

## Jenkins Jenkinsfile 示例

### 标准构建流水线

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven 3.8.6'
        jdk 'JDK 8'
    }

    stages {
        stage('Checkout') {
            steps {
                // 拉取整个代码仓库
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    // 使用方法2时，validate阶段会自动安装lib中的jar
                    sh 'mvn clean install -DskipTests'
                }
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Package') {
            steps {
                sh 'mvn package'
            }
        }
    }

    post {
        success {
            echo '构建成功！'
            archiveArtifacts artifacts: '**/target/*.jar', fingerprint: true
        }
        failure {
            echo '构建失败！'
        }
    }
}
```

### 处理嵌套模块的构建

```groovy
pipeline {
    agent any

    stages {
        stage('Build Common') {
            steps {
                dir('common') {
                    sh 'mvn clean install'
                }
            }
        }

        stage('Build Services') {
            parallel {
                stage('Build Service-A') {
                    steps {
                        dir('service-a') {
                            sh 'mvn clean package'
                        }
                    }
                }
                stage('Build Service-B') {
                    steps {
                        dir('module-group/service-b') {
                            sh 'mvn clean package'
                        }
                    }
                }
            }
        }
    }
}
```

## 关键注意事项

### 1. Git配置
确保 `common/lib/` 目录下的jar文件被提交到Git：

```bash
# 检查.gitignore，确保不排除lib目录
# 如果有这行，需要添加例外：
# !common/lib/*.jar

# 提交lib目录
git add common/lib/*.jar
git commit -m "Add local lib dependencies"
git push
```

### 2. 路径使用
- 始终使用 `${project.basedir}` 而不是绝对路径
- 对于嵌套项目，Maven会自动解析正确的相对路径
- Jenkins在不同节点上工作目录可能不同，相对路径确保兼容性

### 3. 依赖传递
- 使用 **方法2（maven-install-plugin）** 时，依赖会正常传递
- 子项目只需依赖common模块即可：
  ```xml
  <dependency>
      <groupId>com.example</groupId>
      <artifactId>common</artifactId>
      <version>${project.version}</version>
  </dependency>
  ```

### 4. 多环境构建
如果Jenkins有多个构建节点，方法2会在每个节点的本地仓库安装依赖，互不影响。

### 5. 清理策略
后续替换依赖时：
1. 更新common/pom.xml中的依赖版本（使用正常的Maven依赖）
2. 移除maven-install-plugin配置
3. 删除lib目录中的旧jar
4. 提交更改并重新构建

## 验证方法

### 本地验证
```bash
cd maven-multi-module-demo
mvn clean install
```

### 模拟Jenkins环境
```bash
# 清除本地仓库缓存
rm -rf ~/.m2/repository/com/example

# 重新构建
mvn clean install

# 检查是否成功
ls -la service-a/target/*.jar
ls -la module-group/service-b/target/*.jar
```

### 检查依赖树
```bash
# 查看service-a的依赖
cd service-a
mvn dependency:tree

# 查看service-b的依赖
cd ../module-group/service-b
mvn dependency:tree
```

## 常见问题

### Q1: Jenkins构建时找不到lib中的jar
**A**: 确保lib目录已提交到Git，并且使用 `${project.basedir}` 相对路径。

### Q2: 子项目无法使用common中lib的依赖
**A**: 使用方法2（maven-install-plugin），避免使用system scope。

### Q3: 多个子项目都需要相同的lib依赖
**A**: 只需在common模块配置一次，所有依赖common的子项目都会自动获得。

### Q4: 如何批量安装多个jar
**A**: 在maven-install-plugin中配置多个execution：

```xml
<executions>
    <execution>
        <id>install-jar-1</id>
        <phase>validate</phase>
        <goals><goal>install-file</goal></goals>
        <configuration>
            <file>${project.basedir}/lib/jar1.jar</file>
            <!-- ... -->
        </configuration>
    </execution>
    <execution>
        <id>install-jar-2</id>
        <phase>validate</phase>
        <goals><goal>install-file</goal></goals>
        <configuration>
            <file>${project.basedir}/lib/jar2.jar</file>
            <!-- ... -->
        </configuration>
    </execution>
</executions>
```

## 最佳实践建议

1. **使用方法2（推荐）**：maven-install-plugin自动安装到本地仓库
2. **文档记录**：在lib/README.md中记录每个jar的来源、版本、替换计划
3. **版本管理**：在根pom.xml的properties中统一管理版本号
4. **定期审查**：设置定期任务检查和替换旧依赖
5. **隔离影响**：只在common模块使用此方案，其他模块保持标准Maven依赖
