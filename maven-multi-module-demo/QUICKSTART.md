# 快速开始指南 ⚡

> 5分钟快速上手 - 让你的项目使用本地lib绕过流水线检查

## 前提条件

- ✅ Java 8+
- ✅ Maven 3.6+
- ✅ 你有需要使用的jar文件

## 步骤1️⃣ - 复制jar文件 (30秒)

将你的jar文件复制到 `common/lib/` 目录：

```bash
# Linux/Mac
cp /path/to/your-old-dependency.jar common/lib/

# Windows
copy C:\path\to\your-old-dependency.jar common\lib\
```

## 步骤2️⃣ - 配置pom.xml (2分钟)

打开 `common/pom.xml`，找到 `<build><plugins>` 部分，添加：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-install-plugin</artifactId>
    <version>2.5.2</version>
    <executions>
        <execution>
            <id>install-my-jar</id>
            <phase>validate</phase>
            <goals><goal>install-file</goal></goals>
            <configuration>
                <!-- 修改这里：jar文件名 -->
                <file>${project.basedir}/lib/your-jar-name.jar</file>
                <!-- 修改这里：groupId -->
                <groupId>com.example</groupId>
                <!-- 修改这里：artifactId -->
                <artifactId>your-artifact-id</artifactId>
                <!-- 修改这里：版本号 -->
                <version>1.0.0</version>
                <packaging>jar</packaging>
                <generatePom>true</generatePom>
            </configuration>
        </execution>
    </executions>
</plugin>
```

然后在同一个文件的 `<dependencies>` 部分添加：

```xml
<dependency>
    <!-- 与上面的配置保持一致 -->
    <groupId>com.example</groupId>
    <artifactId>your-artifact-id</artifactId>
    <version>1.0.0</version>
</dependency>
```

**💡 提示**：如果不知道jar的groupId和artifactId，可以自己定义，例如：
- groupId: `com.local`
- artifactId: jar文件名（去掉版本号和.jar）
- version: jar的版本号

## 步骤3️⃣ - 构建测试 (1分钟)

在项目根目录执行：

```bash
# Windows
test-build.bat

# Linux/Mac
chmod +x test-build.sh
./test-build.sh

# 或者直接用Maven
mvn clean install
```

如果看到 `BUILD SUCCESS`，恭喜你成功了！🎉

## 步骤4️⃣ - 使用依赖 (1分钟)

在 `common/src/main/java/com/example/common/CommonUtil.java` 中使用你的jar：

```java
package com.example.common;

// 导入你jar中的类
import your.package.YourClass;

public class CommonUtil {

    public static void useYourJar() {
        // 使用jar中的功能
        YourClass.doSomething();
    }
}
```

子项目（service-a、service-b）会自动获得这个依赖，可以直接使用CommonUtil！

## 完成！✨

现在你的项目可以：
- ✅ 使用本地lib中的jar
- ✅ 在Jenkins上正常构建
- ✅ 所有子项目自动获得依赖
- ✅ 绕过流水线的版本检查

## 验证依赖是否正确

```bash
cd service-a
mvn dependency:tree | grep your-artifact-id

# 应该看到类似输出：
# [INFO] |  \- com.example:common:jar:1.0.0-SNAPSHOT:compile
# [INFO] |     \- com.example:your-artifact-id:jar:1.0.0:compile
```

## 遇到问题？

### 问题1：找不到jar文件
**检查**：jar文件是否在 `common/lib/` 目录？
```bash
ls common/lib/
```

### 问题2：构建失败，提示找不到依赖
**检查**：pom.xml中的groupId、artifactId、version是否与配置一致？

### 问题3：子项目无法使用依赖
**检查**：是否使用了maven-install-plugin（不是system scope）？

## 下一步

- 📖 阅读 [README.md](README.md) 了解完整功能
- 🔧 查看 [JENKINS_GUIDE.md](JENKINS_GUIDE.md) 配置Jenkins
- 💡 参考 [USAGE_EXAMPLE.md](USAGE_EXAMPLE.md) 学习更多用法

## 常用命令

```bash
# 清理并重新构建
mvn clean install

# 只编译不测试
mvn clean compile -DskipTests

# 查看依赖树
cd service-a && mvn dependency:tree

# 运行service-a
cd service-a && mvn spring-boot:run

# 运行service-b
cd module-group/service-b && mvn spring-boot:run
```

## Git提交

记得提交lib目录到Git：

```bash
git add common/lib/*.jar
git add common/pom.xml
git commit -m "Add local lib dependencies"
git push
```

---

**需要帮助？** 查看完整文档：
- [README.md](README.md) - 项目概述
- [JENKINS_GUIDE.md](JENKINS_GUIDE.md) - Jenkins配置
- [USAGE_EXAMPLE.md](USAGE_EXAMPLE.md) - 详细示例
- [SUMMARY.md](SUMMARY.md) - 项目总结
