# 实际使用示例

## 场景说明

假设你的公共项目（common）需要使用一个旧版本的jar包：`commons-lang3-3.8.1.jar`（假设这是不符合3年内版本要求的）

## 完整操作步骤

### 步骤1：准备jar文件

将jar文件复制到common/lib目录：

```bash
# 假设你的jar文件在 /downloads/commons-lang3-3.8.1.jar
cp /downloads/commons-lang3-3.8.1.jar common/lib/

# Windows下
copy C:\downloads\commons-lang3-3.8.1.jar common\lib\
```

### 步骤2：配置common/pom.xml

编辑 `common/pom.xml`，在 `<build><plugins>` 部分添加：

```xml
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
```

然后在 `<dependencies>` 部分添加：

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>3.8.1</version>
</dependency>
```

### 步骤3：在CommonUtil中使用依赖

编辑 `common/src/main/java/com/example/common/CommonUtil.java`：

```java
package com.example.common;

import org.apache.commons.lang3.StringUtils;

public class CommonUtil {

    public static String formatMessage(String message) {
        // 现在可以使用commons-lang3的功能了
        return StringUtils.capitalize(message);
    }

    public static boolean isEmpty(String str) {
        return StringUtils.isEmpty(str);
    }
}
```

### 步骤4：构建项目

```bash
# 方法1：使用提供的测试脚本
./test-build.sh        # Linux/Mac
test-build.bat         # Windows

# 方法2：手动构建
mvn clean install
```

### 步骤5：验证依赖

```bash
# 查看service-a的依赖树，确认commons-lang3已包含
cd service-a
mvn dependency:tree | grep commons-lang3

# 应该看到类似输出：
# [INFO] |  \- com.example:common:jar:1.0.0-SNAPSHOT:compile
# [INFO] |     \- org.apache.commons:commons-lang3:jar:3.8.1:compile
```

### 步骤6：在子项目中使用

`service-a/src/main/java/com/example/servicea/controller/TestController.java`：

```java
package com.example.servicea.controller;

import com.example.common.CommonUtil;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class TestController {

    @GetMapping("/format")
    public String format(@RequestParam String message) {
        // 通过common模块使用commons-lang3
        return CommonUtil.formatMessage(message);
    }

    @GetMapping("/check-empty")
    public boolean checkEmpty(@RequestParam String text) {
        return CommonUtil.isEmpty(text);
    }
}
```

## 多个jar文件的情况

如果你有多个jar需要添加到lib目录：

### 1. 复制所有jar到lib目录

```bash
common/lib/
├── commons-lang3-3.8.1.jar
├── guava-20.0.jar
└── jackson-core-2.9.0.jar
```

### 2. 在pom.xml中添加多个execution

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-install-plugin</artifactId>
    <version>2.5.2</version>
    <executions>
        <!-- commons-lang3 -->
        <execution>
            <id>install-commons-lang3</id>
            <phase>validate</phase>
            <goals><goal>install-file</goal></goals>
            <configuration>
                <file>${project.basedir}/lib/commons-lang3-3.8.1.jar</file>
                <groupId>org.apache.commons</groupId>
                <artifactId>commons-lang3</artifactId>
                <version>3.8.1</version>
                <packaging>jar</packaging>
                <generatePom>true</generatePom>
            </configuration>
        </execution>

        <!-- guava -->
        <execution>
            <id>install-guava</id>
            <phase>validate</phase>
            <goals><goal>install-file</goal></goals>
            <configuration>
                <file>${project.basedir}/lib/guava-20.0.jar</file>
                <groupId>com.google.guava</groupId>
                <artifactId>guava</artifactId>
                <version>20.0</version>
                <packaging>jar</packaging>
                <generatePom>true</generatePom>
            </configuration>
        </execution>

        <!-- jackson-core -->
        <execution>
            <id>install-jackson-core</id>
            <phase>validate</phase>
            <goals><goal>install-file</goal></goals>
            <configuration>
                <file>${project.basedir}/lib/jackson-core-2.9.0.jar</file>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-core</artifactId>
                <version>2.9.0</version>
                <packaging>jar</packaging>
                <generatePom>true</generatePom>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### 3. 添加对应的依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.8.1</version>
    </dependency>

    <dependency>
        <groupId>com.google.guava</groupId>
        <artifactId>guava</artifactId>
        <version>20.0</version>
    </dependency>

    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-core</artifactId>
        <version>2.9.0</version>
    </dependency>
</dependencies>
```

## Jenkins流水线实际配置

### Jenkinsfile示例

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven 3.8.6'
        jdk 'JDK 8'
    }

    environment {
        // 定义Maven选项
        MAVEN_OPTS = '-Xmx1024m'
    }

    stages {
        stage('环境检查') {
            steps {
                echo '检查环境信息...'
                sh 'java -version'
                sh 'mvn -version'
                sh 'pwd'
                sh 'ls -la common/lib/'
            }
        }

        stage('构建Common模块') {
            steps {
                echo '构建公共模块（会自动安装lib中的jar）...'
                sh 'mvn clean install -pl common -am -DskipTests'
            }
        }

        stage('构建所有子项目') {
            steps {
                echo '构建所有模块...'
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('运行测试') {
            steps {
                echo '运行测试...'
                sh 'mvn test'
            }
        }

        stage('归档产物') {
            steps {
                echo '归档构建产物...'
                archiveArtifacts artifacts: '**/target/*.jar',
                                fingerprint: true,
                                allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            echo '✅ 构建成功！'
        }
        failure {
            echo '❌ 构建失败！'
        }
        always {
            echo '清理工作区...'
            cleanWs()
        }
    }
}
```

### 针对嵌套项目的并行构建

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven 3.8.6'
        jdk 'JDK 8'
    }

    stages {
        stage('构建Common') {
            steps {
                sh 'mvn clean install -pl common -am'
            }
        }

        stage('并行构建子项目') {
            parallel {
                stage('构建Service-A') {
                    steps {
                        sh 'mvn clean package -pl service-a -am'
                    }
                }

                stage('构建Service-B') {
                    steps {
                        sh 'mvn clean package -pl module-group/service-b -am'
                    }
                }
            }
        }
    }
}
```

## 常见问题解答

### Q: 构建时报错找不到jar文件
**A**:
1. 检查jar文件是否在lib目录：`ls common/lib/*.jar`
2. 检查pom.xml中的路径是否正确使用了 `${project.basedir}`
3. 确保lib目录已提交到Git

### Q: 子项目找不到common中lib的依赖
**A**:
1. 确保使用了maven-install-plugin（不是system scope）
2. 先单独构建common：`mvn clean install -pl common`
3. 查看Maven本地仓库是否有该jar：`ls ~/.m2/repository/org/apache/commons/commons-lang3/3.8.1/`

### Q: Jenkins构建时validate阶段失败
**A**:
1. 检查Jenkins工作空间的权限
2. 确保Maven本地仓库目录存在且可写
3. 查看详细日志：`mvn clean install -X`

### Q: 如何确认依赖已正确传递到子项目
**A**:
```bash
cd service-a
mvn dependency:tree

# 应该看到：
# [INFO] com.example:service-a:jar:1.0.0-SNAPSHOT
# [INFO] \- com.example:common:jar:1.0.0-SNAPSHOT:compile
# [INFO]    \- org.apache.commons:commons-lang3:jar:3.8.1:compile
```

## 后续优化建议

### 1. 版本统一管理

在根pom.xml的properties中定义版本：

```xml
<properties>
    <commons-lang3.version>3.8.1</commons-lang3.version>
    <guava.version>20.0</guava.version>
</properties>
```

然后在common/pom.xml中引用：

```xml
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>${commons-lang3.version}</version>
</dependency>
```

### 2. 创建lib管理脚本

创建 `common/lib/manage-libs.sh`：

```bash
#!/bin/bash

# 自动安装所有lib中的jar到本地仓库

LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for jar in "${LIB_DIR}"/*.jar; do
    if [ -f "$jar" ]; then
        filename=$(basename "$jar")
        echo "发现jar: $filename"
        # 这里可以添加自动解析jar信息并安装的逻辑
    fi
done
```

### 3. 添加验证测试

创建一个测试类验证依赖是否可用：

```java
@Test
public void testLibDependencies() {
    // 验证commons-lang3可用
    String result = CommonUtil.formatMessage("test");
    assertNotNull(result);
    assertEquals("Test", result);
}
```

## 总结

这个方案的优势：
1. ✅ 完全绕过流水线的版本检查
2. ✅ 依赖可以正常传递到所有子项目
3. ✅ Jenkins构建自动化处理
4. ✅ 支持任意层级的嵌套子项目
5. ✅ 后续可以逐步替换为标准Maven依赖

记住：这是一个临时解决方案，应该在代码中添加TODO注释，提醒后续升级依赖版本。
