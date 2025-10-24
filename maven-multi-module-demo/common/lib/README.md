# 本地Lib目录说明

## 用途
这个目录用于存放不符合流水线版本要求的第三方jar包，作为临时解决方案。

## 使用方法

### 方法1：使用system scope（简单但有限制）
在pom.xml中添加：
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>your-lib</artifactId>
    <version>1.0.0</version>
    <scope>system</scope>
    <systemPath>${project.basedir}/lib/your-lib-1.0.0.jar</systemPath>
</dependency>
```

**注意**：使用相对路径 `${project.basedir}/lib/` 来确保在Jenkins等CI环境中也能找到jar包。

### 方法2：使用Maven安装插件（推荐）
在根pom.xml或common的pom.xml中配置maven-install-plugin，在validate阶段自动将jar安装到本地仓库：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-install-plugin</artifactId>
    <executions>
        <execution>
            <id>install-your-jar</id>
            <phase>validate</phase>
            <goals>
                <goal>install-file</goal>
            </goals>
            <configuration>
                <file>${project.basedir}/lib/your-lib-1.0.0.jar</file>
                <groupId>com.example</groupId>
                <artifactId>your-lib</artifactId>
                <version>1.0.0</version>
                <packaging>jar</packaging>
            </configuration>
        </execution>
    </executions>
</plugin>
```

然后正常引用依赖：
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>your-lib</artifactId>
    <version>1.0.0</version>
</dependency>
```

## 示例文件
将你的jar文件放在这里，例如：
- commons-lang3-3.8.1.jar
- old-dependency-1.0.0.jar

## Jenkins构建注意事项
1. 确保lib目录被提交到Git仓库
2. 使用 `${project.basedir}` 而不是绝对路径
3. 在父子项目中，子项目引用common的lib时，路径会自动解析

## 子项目如何引用
子项目只需要依赖common模块即可：
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>common</artifactId>
    <version>${project.version}</version>
</dependency>
```

common模块中的lib依赖会自动传递（如果使用compile scope）。
