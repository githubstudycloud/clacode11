#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maven多模块项目生成器 - 教学版

功能：
1. 自动生成标准Maven多模块项目结构
2. 配置本地lib依赖管理
3. 生成Spring Boot示例代码
4. 创建完整的配置文件
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict


class ProjectGenerator:
    """项目生成器"""

    def __init__(self, project_name: str, base_dir: str = "."):
        """初始化生成器

        Args:
            project_name: 项目名称
            base_dir: 项目创建的基础目录
        """
        self.project_name = project_name
        self.base_dir = Path(base_dir).resolve()
        self.project_dir = self.base_dir / project_name
        self.group_id = "com.example"
        self.version = "1.0.0-SNAPSHOT"
        self.java_version = "1.8"
        self.spring_boot_version = "2.7.18"

    def create_project_structure(self):
        """创建项目目录结构"""
        print("\n=== 创建项目结构 ===")

        # 主目录
        self.project_dir.mkdir(parents=True, exist_ok=True)
        print(f"[OK] 创建项目目录: {self.project_dir}")

        # 子模块目录
        modules = [
            "common",
            "service-a",
            "module-group",
            "module-group/service-b",
            "tools",
            "docs"
        ]

        for module in modules:
            module_dir = self.project_dir / module
            module_dir.mkdir(parents=True, exist_ok=True)
            print(f"[OK] 创建模块目录: {module}")

        # lib目录
        lib_dirs = [
            "common/lib",
            "service-a/lib",
            "module-group/service-b/lib",
            "local-lib-manager/jars"
        ]

        for lib_dir in lib_dirs:
            lib_path = self.project_dir / lib_dir
            lib_path.mkdir(parents=True, exist_ok=True)
            print(f"[OK] 创建lib目录: {lib_dir}")

    def create_root_pom(self):
        """创建根POM文件"""
        print("\n=== 创建根POM ===")

        content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>{self.group_id}</groupId>
    <artifactId>{self.project_name}</artifactId>
    <version>{self.version}</version>
    <packaging>pom</packaging>

    <name>{self.project_name}</name>
    <description>Maven多模块项目 - 教学示例</description>

    <modules>
        <module>common</module>
        <module>service-a</module>
        <module>module-group</module>
    </modules>

    <properties>
        <java.version>{self.java_version}</java.version>
        <maven.compiler.source>{self.java_version}</maven.compiler.source>
        <maven.compiler.target>{self.java_version}</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <spring-boot.version>{self.spring_boot_version}</spring-boot.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${{spring-boot.version}}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                    <version>${{spring-boot.version}}</version>
                </plugin>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.8.1</version>
                    <configuration>
                        <source>${{java.version}}</source>
                        <target>${{java.version}}</target>
                    </configuration>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
'''

        pom_file = self.project_dir / "pom.xml"
        pom_file.write_text(content, encoding='utf-8')
        print(f"[OK] 创建文件: pom.xml")

    def create_common_module(self):
        """创建common模块"""
        print("\n=== 创建Common模块 ===")

        # POM文件
        pom_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>{self.group_id}</groupId>
        <artifactId>{self.project_name}</artifactId>
        <version>{self.version}</version>
    </parent>

    <artifactId>common</artifactId>
    <packaging>jar</packaging>

    <name>Common Module</name>
    <description>公共模块 - 包含通用工具类和本地lib依赖</description>

    <dependencies>
        <!-- Spring Boot Starter -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- 将lib目录复制到target -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.2.0</version>
                <executions>
                    <execution>
                        <id>copy-lib</id>
                        <phase>validate</phase>
                        <goals>
                            <goal>copy-resources</goal>
                        </goals>
                        <configuration>
                            <outputDirectory>${{project.build.directory}}/lib</outputDirectory>
                            <resources>
                                <resource>
                                    <directory>${{project.basedir}}/lib</directory>
                                    <filtering>false</filtering>
                                </resource>
                            </resources>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
'''

        pom_file = self.project_dir / "common" / "pom.xml"
        pom_file.write_text(pom_content, encoding='utf-8')
        print(f"[OK] 创建文件: common/pom.xml")

        # 创建Java源代码目录
        src_dir = self.project_dir / "common" / "src" / "main" / "java" / "com" / "example" / "common"
        src_dir.mkdir(parents=True, exist_ok=True)

        # 创建CommonUtil.java
        util_content = '''package com.example.common;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 公共工具类
 *
 * @author Maven Multi-Module Demo
 */
public class CommonUtil {

    private static final DateTimeFormatter FORMATTER =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    /**
     * 获取当前时间字符串
     *
     * @return 格式化的时间字符串
     */
    public static String getCurrentTime() {
        return LocalDateTime.now().format(FORMATTER);
    }

    /**
     * 生成问候消息
     *
     * @param name 名称
     * @return 问候消息
     */
    public static String greet(String name) {
        return String.format("Hello, %s! Current time: %s",
            name, getCurrentTime());
    }

    /**
     * 检查字符串是否为空
     *
     * @param str 待检查的字符串
     * @return 是否为空
     */
    public static boolean isEmpty(String str) {
        return str == null || str.trim().isEmpty();
    }
}
'''

        util_file = src_dir / "CommonUtil.java"
        util_file.write_text(util_content, encoding='utf-8')
        print(f"[OK] 创建文件: common/src/main/java/com/example/common/CommonUtil.java")

        # 创建lib目录README
        lib_readme = '''# Common模块 - 本地Jar依赖说明

## 目录用途

本目录用于存放Common模块的本地jar依赖文件。

## 使用方法

### 1. 添加jar文件

将需要的jar文件复制到本目录。

### 2. 配置POM

使用 `local-lib-manager/lib_manager.py` 工具自动生成Maven配置。

### 3. 构建项目

```bash
mvn clean install
```

## 当前依赖

目前没有本地jar依赖。如需添加，请使用lib_manager工具。

## 注意事项

1. jar文件应该提交到Git仓库
2. 使用maven-install-plugin自动安装
3. 避免使用system scope
'''

        lib_readme_file = self.project_dir / "common" / "lib" / "README.md"
        lib_readme_file.write_text(lib_readme, encoding='utf-8')
        print(f"[OK] 创建文件: common/lib/README.md")

    def create_service_module(self, module_name: str, port: int, parent_path: str = ""):
        """创建服务模块

        Args:
            module_name: 模块名称（如service-a）
            port: 服务端口
            parent_path: 父路径（用于嵌套模块）
        """
        print(f"\n=== 创建{module_name}模块 ===")

        module_path = self.project_dir / parent_path / module_name if parent_path else self.project_dir / module_name

        # POM文件
        parent_artifact = "module-group" if parent_path else self.project_name
        pom_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>{self.group_id}</groupId>
        <artifactId>{parent_artifact}</artifactId>
        <version>{self.version}</version>
    </parent>

    <artifactId>{module_name}</artifactId>
    <packaging>jar</packaging>

    <name>{module_name}</name>
    <description>{module_name} - Spring Boot微服务</description>

    <dependencies>
        <!-- 依赖公共模块 -->
        <dependency>
            <groupId>{self.group_id}</groupId>
            <artifactId>common</artifactId>
            <version>${{project.version}}</version>
        </dependency>

        <!-- Spring Boot Web -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Spring Boot Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
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
</project>
'''

        pom_file = module_path / "pom.xml"
        pom_file.write_text(pom_content, encoding='utf-8')
        print(f"[OK] 创建文件: {parent_path}/{module_name}/pom.xml" if parent_path else f"[OK] 创建文件: {module_name}/pom.xml")

        # 创建Java源代码
        package_name = module_name.replace("-", "")
        src_dir = module_path / "src" / "main" / "java" / "com" / "example" / package_name
        src_dir.mkdir(parents=True, exist_ok=True)

        # Application主类
        app_class = f"{package_name[0].upper()}{package_name[1:]}Application"
        app_content = f'''package com.example.{package_name};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * {module_name} 启动类
 */
@SpringBootApplication(scanBasePackages = {{"com.example"}})
public class {app_class} {{

    public static void main(String[] args) {{
        SpringApplication.run({app_class}.class, args);
    }}
}}
'''

        app_file = src_dir / f"{app_class}.java"
        app_file.write_text(app_content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/src/.../{ app_class}.java")

        # Controller
        controller_dir = src_dir / "controller"
        controller_dir.mkdir(parents=True, exist_ok=True)

        controller_content = f'''package com.example.{package_name}.controller;

import com.example.common.CommonUtil;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * {module_name} 测试控制器
 */
@RestController
@RequestMapping("/api")
public class TestController {{

    @GetMapping("/hello")
    public Map<String, Object> hello(@RequestParam(defaultValue = "Student") String name) {{
        Map<String, Object> result = new HashMap<>();
        result.put("service", "{module_name}");
        result.put("message", CommonUtil.greet(name));
        result.put("timestamp", CommonUtil.getCurrentTime());
        return result;
    }}

    @GetMapping("/health")
    public Map<String, String> health() {{
        Map<String, String> result = new HashMap<>();
        result.put("status", "UP");
        result.put("service", "{module_name}");
        return result;
    }}
}}
'''

        controller_file = controller_dir / "TestController.java"
        controller_file.write_text(controller_content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/src/.../controller/TestController.java")

        # application.yml
        resources_dir = module_path / "src" / "main" / "resources"
        resources_dir.mkdir(parents=True, exist_ok=True)

        yml_content = f'''server:
  port: {port}

spring:
  application:
    name: {module_name}

logging:
  level:
    com.example: DEBUG
'''

        yml_file = resources_dir / "application.yml"
        yml_file.write_text(yml_content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/src/main/resources/application.yml")

    def create_module_group(self):
        """创建module-group聚合模块"""
        print("\n=== 创建module-group ===")

        pom_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>{self.group_id}</groupId>
        <artifactId>{self.project_name}</artifactId>
        <version>{self.version}</version>
    </parent>

    <artifactId>module-group</artifactId>
    <packaging>pom</packaging>

    <name>Module Group</name>
    <description>模块组 - 包含多个嵌套子模块</description>

    <modules>
        <module>service-b</module>
        <!-- 可以继续添加更多子模块 -->
    </modules>
</project>
'''

        pom_file = self.project_dir / "module-group" / "pom.xml"
        pom_file.write_text(pom_content, encoding='utf-8')
        print(f"[OK] 创建文件: module-group/pom.xml")

    def create_build_scripts(self):
        """创建构建脚本"""
        print("\n=== 创建构建脚本 ===")

        # Windows批处理脚本
        bat_content = '''@echo off
chcp 65001 >nul
echo ====================================
echo   Maven 多模块项目构建工具
echo ====================================
echo.

:menu
echo 请选择操作:
echo 1. 完整构建 (clean install)
echo 2. 快速构建 (install)
echo 3. 只编译 (compile)
echo 4. 运行测试 (test)
echo 5. 清理 (clean)
echo 6. 查看依赖树
echo 7. 退出
echo.

set /p choice=请输入选项 (1-7):

if "%choice%"=="1" goto full_build
if "%choice%"=="2" goto quick_build
if "%choice%"=="3" goto compile
if "%choice%"=="4" goto test
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto dependency
if "%choice%"=="7" goto end

echo 无效选项，请重新选择
echo.
goto menu

:full_build
echo.
echo [执行] mvn clean install
call mvn clean install
goto result

:quick_build
echo.
echo [执行] mvn install
call mvn install
goto result

:compile
echo.
echo [执行] mvn compile
call mvn compile
goto result

:test
echo.
echo [执行] mvn test
call mvn test
goto result

:clean
echo.
echo [执行] mvn clean
call mvn clean
goto result

:dependency
echo.
echo [执行] mvn dependency:tree
call mvn dependency:tree
goto result

:result
echo.
if %ERRORLEVEL% EQU 0 (
    echo ====================================
    echo   构建成功！
    echo ====================================
) else (
    echo ====================================
    echo   构建失败！错误代码: %ERRORLEVEL%
    echo ====================================
)
echo.
pause
goto menu

:end
echo.
echo 再见！
'''

        bat_file = self.project_dir / "build.bat"
        bat_file.write_text(bat_content, encoding='utf-8')
        print(f"[OK] 创建文件: build.bat")

        # Linux/Mac Shell脚本
        sh_content = '''#!/bin/bash

echo "===================================="
echo "  Maven 多模块项目构建工具"
echo "===================================="
echo ""

show_menu() {
    echo "请选择操作:"
    echo "1. 完整构建 (clean install)"
    echo "2. 快速构建 (install)"
    echo "3. 只编译 (compile)"
    echo "4. 运行测试 (test)"
    echo "5. 清理 (clean)"
    echo "6. 查看依赖树"
    echo "7. 退出"
    echo ""
}

while true; do
    show_menu
    read -p "请输入选项 (1-7): " choice

    case $choice in
        1)
            echo ""
            echo "[执行] mvn clean install"
            mvn clean install
            ;;
        2)
            echo ""
            echo "[执行] mvn install"
            mvn install
            ;;
        3)
            echo ""
            echo "[执行] mvn compile"
            mvn compile
            ;;
        4)
            echo ""
            echo "[执行] mvn test"
            mvn test
            ;;
        5)
            echo ""
            echo "[执行] mvn clean"
            mvn clean
            ;;
        6)
            echo ""
            echo "[执行] mvn dependency:tree"
            mvn dependency:tree
            ;;
        7)
            echo ""
            echo "再见！"
            exit 0
            ;;
        *)
            echo "无效选项，请重新选择"
            echo ""
            continue
            ;;
    esac

    if [ $? -eq 0 ]; then
        echo ""
        echo "===================================="
        echo "  构建成功！"
        echo "===================================="
    else
        echo ""
        echo "===================================="
        echo "  构建失败！错误代码: $?"
        echo "===================================="
    fi
    echo ""
    read -p "按回车键继续..."
done
'''

        sh_file = self.project_dir / "build.sh"
        sh_file.write_text(sh_content, encoding='utf-8')

        # 设置可执行权限
        try:
            os.chmod(sh_file, 0o755)
        except:
            pass

        print(f"[OK] 创建文件: build.sh")

    def create_gitignore(self):
        """创建.gitignore文件"""
        print("\n=== 创建.gitignore ===")

        content = '''# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# IDE
.idea/
*.iml
*.iws
*.ipr
.vscode/
.settings/
.project
.classpath

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# 保留lib目录中的jar文件
!lib/*.jar
!*/lib/*.jar
!**/lib/*.jar
'''

        file_path = self.project_dir / ".gitignore"
        file_path.write_text(content, encoding='utf-8')
        print(f"[OK] 创建文件: .gitignore")

    def generate(self):
        """执行完整的项目生成"""
        print("=" * 60)
        print(" Maven多模块项目生成器 - 教学版")
        print("=" * 60)

        try:
            self.create_project_structure()
            self.create_root_pom()
            self.create_common_module()
            self.create_service_module("service-a", 8081)
            self.create_module_group()
            self.create_service_module("service-b", 8082, "module-group")
            self.create_build_scripts()
            self.create_gitignore()

            print("\n" + "=" * 60)
            print(" 项目生成完成！")
            print("=" * 60)
            print(f"\n项目路径: {self.project_dir}")
            print("\n下一步操作:")
            print(f"  cd {self.project_name}")
            print("  mvn clean install")
            print("  cd service-a && mvn spring-boot:run")
            print("\n访问测试:")
            print("  http://localhost:8081/api/hello")
            print("  http://localhost:8082/api/hello")
            print()

        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Maven多模块项目生成器 - 教学版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s my-project                    # 在当前目录创建my-project
  %(prog)s my-project --dir /path/to/    # 在指定目录创建项目
        """
    )

    parser.add_argument(
        'project_name',
        help='项目名称'
    )

    parser.add_argument(
        '--dir',
        default='.',
        help='项目创建的基础目录 (默认: 当前目录)'
    )

    args = parser.parse_args()

    generator = ProjectGenerator(args.project_name, args.dir)
    generator.generate()


if __name__ == '__main__':
    main()
