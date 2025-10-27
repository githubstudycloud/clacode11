#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maven多模块项目生成器 - 高级版

功能增强：
1. 支持自定义包名（groupId, packageName）
2. 支持指定父子项目路径
3. 支持自定义端口配置
4. 支持模板选择（基础版/完整版）
5. 生成配置文件以便复用
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import List, Dict, Optional


class AdvancedProjectGenerator:
    """高级项目生成器"""

    def __init__(self, config: Dict):
        """初始化生成器

        Args:
            config: 项目配置字典
        """
        self.config = config
        self.project_name = config.get('project_name', 'my-project')
        self.base_dir = Path(config.get('base_dir', '.')).resolve()
        self.project_dir = self.base_dir / self.project_name

        # 基础配置
        self.group_id = config.get('group_id', 'com.example')
        self.version = config.get('version', '1.0.0-SNAPSHOT')
        self.java_version = config.get('java_version', '1.8')
        self.spring_boot_version = config.get('spring_boot_version', '2.7.18')

        # 包名配置（从groupId自动推导或自定义）
        package_name = config.get('package_name')
        if package_name:
            self.package_name = package_name
        else:
            # 从group_id自动生成 com.example -> com/example
            self.package_name = self.group_id.replace('.', '/')

        # 模块配置
        self.modules = config.get('modules', [])
        if not self.modules:
            # 默认模块
            self.modules = [
                {'name': 'common', 'type': 'lib'},
                {'name': 'service-a', 'type': 'service', 'port': 8081},
            ]

        # 模板类型
        self.template = config.get('template', 'standard')  # standard, minimal, full

        # 是否包含示例代码
        self.include_examples = config.get('include_examples', True)

        # 是否创建本地lib支持
        self.include_local_lib = config.get('include_local_lib', True)

    def create_project_structure(self):
        """创建项目目录结构"""
        print("\n=== 创建项目结构 ===")

        # 主目录
        self.project_dir.mkdir(parents=True, exist_ok=True)
        print(f"[OK] 创建项目目录: {self.project_dir}")

        # 创建模块目录
        for module in self.modules:
            module_name = module['name']
            module_path = module.get('path', '')

            if module_path:
                # 支持嵌套路径，如 "module-group/service-b"
                module_dir = self.project_dir / module_path / module_name
            else:
                module_dir = self.project_dir / module_name

            module_dir.mkdir(parents=True, exist_ok=True)
            print(f"[OK] 创建模块目录: {module_name}")

            # 创建lib目录（如果需要）
            if self.include_local_lib and module['type'] in ['lib', 'service']:
                lib_dir = module_dir / 'lib'
                lib_dir.mkdir(exist_ok=True)
                print(f"[OK] 创建lib目录: {module_name}/lib")

        # 创建工具和文档目录
        if self.template == 'full':
            (self.project_dir / 'tools').mkdir(exist_ok=True)
            (self.project_dir / 'docs').mkdir(exist_ok=True)
            (self.project_dir / 'scripts').mkdir(exist_ok=True)
            print("[OK] 创建工具和文档目录")

    def create_root_pom(self):
        """创建根POM文件"""
        print("\n=== 创建根POM ===")

        # 收集所有顶层模块
        top_level_modules = []
        for module in self.modules:
            module_name = module['name']
            module_path = module.get('path', '')

            if not module_path:
                # 顶层模块
                top_level_modules.append(module_name)
            elif '/' not in module_path:
                # 一级嵌套的父模块
                if module_path not in top_level_modules:
                    top_level_modules.append(module_path)

        modules_xml = '\n'.join([f'        <module>{m}</module>' for m in top_level_modules])

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
    <description>Maven多模块项目 - 使用高级生成器创建</description>

    <modules>
{modules_xml}
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

    def create_module(self, module: Dict):
        """创建模块

        Args:
            module: 模块配置字典
        """
        module_name = module['name']
        module_type = module['type']
        module_path = module.get('path', '')

        print(f"\n=== 创建{module_name}模块 ({module_type}) ===")

        # 确定模块路径
        if module_path:
            module_dir = self.project_dir / module_path / module_name
            parent_artifact = module_path.split('/')[-1]
        else:
            module_dir = self.project_dir / module_name
            parent_artifact = self.project_name

        # 创建POM
        if module_type == 'lib':
            self._create_lib_module_pom(module_name, parent_artifact, module_dir)
        elif module_type == 'service':
            port = module.get('port', 8080)
            self._create_service_module_pom(module_name, parent_artifact, module_dir, port)
        elif module_type == 'aggregator':
            self._create_aggregator_pom(module_name, parent_artifact, module_dir, module)

        # 创建源代码（如果需要）
        if self.include_examples and module_type != 'aggregator':
            self._create_module_sources(module_name, module_type, module_dir, module)

    def _create_lib_module_pom(self, module_name: str, parent_artifact: str, module_dir: Path):
        """创建lib模块POM"""
        content = f'''<?xml version="1.0" encoding="UTF-8"?>
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
    <description>{module_name} - 公共模块</description>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
</project>
'''
        pom_file = module_dir / "pom.xml"
        pom_file.write_text(content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/pom.xml")

    def _create_service_module_pom(self, module_name: str, parent_artifact: str,
                                   module_dir: Path, port: int):
        """创建service模块POM"""
        # 查找common模块
        common_dependency = ""
        for m in self.modules:
            if m['type'] == 'lib':
                common_dependency = f'''        <dependency>
            <groupId>{self.group_id}</groupId>
            <artifactId>{m['name']}</artifactId>
            <version>${{project.version}}</version>
        </dependency>
'''
                break

        content = f'''<?xml version="1.0" encoding="UTF-8"?>
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
    <description>{module_name} - Spring Boot服务</description>

    <dependencies>
{common_dependency}
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

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
        pom_file = module_dir / "pom.xml"
        pom_file.write_text(content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/pom.xml")

    def _create_aggregator_pom(self, module_name: str, parent_artifact: str,
                               module_dir: Path, module: Dict):
        """创建聚合模块POM"""
        children = module.get('children', [])
        children_xml = '\n'.join([f'        <module>{c}</module>' for c in children])

        content = f'''<?xml version="1.0" encoding="UTF-8"?>
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
    <packaging>pom</packaging>

    <name>{module_name}</name>
    <description>{module_name} - 模块组</description>

    <modules>
{children_xml}
    </modules>
</project>
'''
        pom_file = module_dir / "pom.xml"
        pom_file.write_text(content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/pom.xml")

    def _create_module_sources(self, module_name: str, module_type: str,
                               module_dir: Path, module: Dict):
        """创建模块源代码"""
        if module_type == 'lib':
            self._create_lib_sources(module_name, module_dir)
        elif module_type == 'service':
            port = module.get('port', 8080)
            self._create_service_sources(module_name, module_dir, port)

    def _create_lib_sources(self, module_name: str, module_dir: Path):
        """创建lib模块源代码"""
        # 创建包目录
        src_dir = module_dir / "src" / "main" / "java" / self.package_name / module_name.replace('-', '')
        src_dir.mkdir(parents=True, exist_ok=True)

        # 创建工具类
        package_declaration = self.package_name.replace('/', '.')
        util_content = f'''package {package_declaration}.{module_name.replace('-', '')};

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 公共工具类 - {module_name}
 *
 * @author Maven Multi-Module Generator
 */
public class CommonUtil {{

    private static final DateTimeFormatter FORMATTER =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    /**
     * 获取当前时间字符串
     */
    public static String getCurrentTime() {{
        return LocalDateTime.now().format(FORMATTER);
    }}

    /**
     * 生成问候消息
     */
    public static String greet(String name) {{
        return String.format("Hello, %s! Time: %s",
            name, getCurrentTime());
    }}
}}
'''
        util_file = src_dir / "CommonUtil.java"
        util_file.write_text(util_content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/src/.../CommonUtil.java")

    def _create_service_sources(self, module_name: str, module_dir: Path, port: int):
        """创建service模块源代码"""
        package_name_no_slash = self.package_name.replace('/', '.')
        module_package = module_name.replace('-', '')

        # 创建包目录
        src_dir = module_dir / "src" / "main" / "java" / self.package_name / module_package
        src_dir.mkdir(parents=True, exist_ok=True)

        # Application主类
        class_name = ''.join(word.capitalize() for word in module_name.split('-')) + 'Application'
        app_content = f'''package {package_name_no_slash}.{module_package};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * {module_name} 启动类
 */
@SpringBootApplication(scanBasePackages = {{"{package_name_no_slash}"}})
public class {class_name} {{

    public static void main(String[] args) {{
        SpringApplication.run({class_name}.class, args);
    }}
}}
'''
        app_file = src_dir / f"{class_name}.java"
        app_file.write_text(app_content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/src/.../{class_name}.java")

        # Controller
        controller_dir = src_dir / "controller"
        controller_dir.mkdir(exist_ok=True)

        controller_content = f'''package {package_name_no_slash}.{module_package}.controller;

import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

/**
 * {module_name} API控制器
 */
@RestController
@RequestMapping("/api")
public class ApiController {{

    @GetMapping("/hello")
    public Map<String, Object> hello(@RequestParam(defaultValue = "World") String name) {{
        Map<String, Object> result = new HashMap<>();
        result.put("service", "{module_name}");
        result.put("message", "Hello, " + name + "!");
        result.put("timestamp", System.currentTimeMillis());
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
        controller_file = controller_dir / "ApiController.java"
        controller_file.write_text(controller_content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/src/.../controller/ApiController.java")

        # application.yml
        resources_dir = module_dir / "src" / "main" / "resources"
        resources_dir.mkdir(parents=True, exist_ok=True)

        yml_content = f'''server:
  port: {port}

spring:
  application:
    name: {module_name}

logging:
  level:
    {package_name_no_slash}: DEBUG
'''
        yml_file = resources_dir / "application.yml"
        yml_file.write_text(yml_content, encoding='utf-8')
        print(f"[OK] 创建文件: {module_name}/src/main/resources/application.yml")

    def create_build_scripts(self):
        """创建构建脚本"""
        print("\n=== 创建构建脚本 ===")

        # build.sh
        sh_content = '''#!/bin/bash
echo "==================================="
echo "  Maven Multi-Module Build Tool"
echo "==================================="
mvn clean install
'''
        sh_file = self.project_dir / "build.sh"
        sh_file.write_text(sh_content, encoding='utf-8')
        try:
            os.chmod(sh_file, 0o755)
        except:
            pass
        print("[OK] 创建文件: build.sh")

        # build.bat
        bat_content = '''@echo off
echo ===================================
echo   Maven Multi-Module Build Tool
echo ===================================
mvn clean install
'''
        bat_file = self.project_dir / "build.bat"
        bat_file.write_text(bat_content, encoding='utf-8')
        print("[OK] 创建文件: build.bat")

    def create_gitignore(self):
        """创建.gitignore"""
        print("\n=== 创建.gitignore ===")

        content = '''# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup

# IDE
.idea/
*.iml
.vscode/
.settings/
.project
.classpath

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# 保留lib目录中的jar文件
!lib/*.jar
!*/lib/*.jar
'''
        file_path = self.project_dir / ".gitignore"
        file_path.write_text(content, encoding='utf-8')
        print("[OK] 创建文件: .gitignore")

    def create_readme(self):
        """创建README"""
        print("\n=== 创建README ===")

        modules_list = '\n'.join([f"- {m['name']} ({m['type']})" for m in self.modules])

        content = f'''# {self.project_name}

Maven多模块项目 - 使用高级生成器创建

## 项目信息

- **Group ID**: {self.group_id}
- **Version**: {self.version}
- **Java Version**: {self.java_version}
- **Spring Boot**: {self.spring_boot_version}

## 模块列表

{modules_list}

## 快速开始

```bash
# 构建项目
mvn clean install

# 运行服务（如果有）
cd [service-module]
mvn spring-boot:run
```

## 配置

项目配置保存在 `project-config.yaml`

## 生成工具

使用 Maven Multi-Module Advanced Generator 生成
'''
        readme_file = self.project_dir / "README.md"
        readme_file.write_text(content, encoding='utf-8')
        print("[OK] 创建文件: README.md")

    def save_config(self):
        """保存项目配置以便复用"""
        config_file = self.project_dir / "project-config.yaml"
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
        print(f"\n[OK] 配置已保存: project-config.yaml")

    def generate(self):
        """执行完整的项目生成"""
        print("=" * 60)
        print(" Maven多模块项目生成器 - 高级版")
        print("=" * 60)

        try:
            self.create_project_structure()
            self.create_root_pom()

            # 创建所有模块
            for module in self.modules:
                self.create_module(module)

            self.create_build_scripts()
            self.create_gitignore()
            self.create_readme()
            self.save_config()

            print("\n" + "=" * 60)
            print(" 项目生成完成！")
            print("=" * 60)
            print(f"\n项目路径: {self.project_dir}")
            print("\n下一步:")
            print(f"  cd {self.project_name}")
            print("  mvn clean install")

            # 显示服务启动命令
            for module in self.modules:
                if module['type'] == 'service':
                    module_path = module.get('path', '')
                    full_path = f"{module_path}/{module['name']}" if module_path else module['name']
                    port = module.get('port', 8080)
                    print(f"\n  # 启动 {module['name']}")
                    print(f"  cd {full_path}")
                    print(f"  mvn spring-boot:run")
                    print(f"  # 访问: http://localhost:{port}/api/hello")
            print()

        except Exception as e:
            print(f"\n错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def load_config_from_file(config_file: str) -> Dict:
    """从YAML文件加载配置"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_default_config(project_name: str, **kwargs) -> Dict:
    """创建默认配置"""
    return {
        'project_name': project_name,
        'base_dir': kwargs.get('base_dir', '.'),
        'group_id': kwargs.get('group_id', 'com.example'),
        'version': kwargs.get('version', '1.0.0-SNAPSHOT'),
        'java_version': kwargs.get('java_version', '1.8'),
        'spring_boot_version': kwargs.get('spring_boot_version', '2.7.18'),
        'package_name': kwargs.get('package_name'),
        'template': kwargs.get('template', 'standard'),
        'include_examples': kwargs.get('include_examples', True),
        'include_local_lib': kwargs.get('include_local_lib', False),
        'modules': kwargs.get('modules', [
            {'name': 'common', 'type': 'lib'},
            {'name': 'service-a', 'type': 'service', 'port': 8081},
        ])
    }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Maven多模块项目生成器 - 高级版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:

1. 基础用法（使用默认配置）:
  %(prog)s my-project

2. 自定义groupId和包名:
  %(prog)s my-project --group-id com.mycompany --package-name com/mycompany/myapp

3. 使用配置文件:
  %(prog)s --config project-config.yaml

4. 完整配置:
  %(prog)s my-project \\
    --group-id com.mycompany \\
    --java-version 11 \\
    --spring-boot-version 2.7.18 \\
    --dir /path/to/workspace

配置文件示例 (project-config.yaml):
  project_name: my-project
  group_id: com.mycompany
  package_name: com/mycompany/app
  java_version: "11"
  spring_boot_version: "2.7.18"
  modules:
    - name: common
      type: lib
    - name: service-a
      type: service
      port: 8081
    - name: module-group
      type: aggregator
      children:
        - service-b
    - name: service-b
      type: service
      path: module-group
      port: 8082
        """
    )

    parser.add_argument(
        'project_name',
        nargs='?',
        help='项目名称（如果使用--config则可选）'
    )

    parser.add_argument(
        '--config',
        help='配置文件路径（YAML格式）'
    )

    parser.add_argument(
        '--dir',
        default='.',
        dest='base_dir',
        help='项目创建的基础目录（默认: 当前目录）'
    )

    parser.add_argument(
        '--group-id',
        default='com.example',
        dest='group_id',
        help='Maven groupId（默认: com.example）'
    )

    parser.add_argument(
        '--package-name',
        dest='package_name',
        help='Java包名（默认: 从group-id推导，如 com/example）'
    )

    parser.add_argument(
        '--java-version',
        default='1.8',
        dest='java_version',
        help='Java版本（默认: 1.8）'
    )

    parser.add_argument(
        '--spring-boot-version',
        default='2.7.18',
        dest='spring_boot_version',
        help='Spring Boot版本（默认: 2.7.18）'
    )

    parser.add_argument(
        '--template',
        choices=['minimal', 'standard', 'full'],
        default='standard',
        help='项目模板（minimal: 最简, standard: 标准, full: 完整）'
    )

    parser.add_argument(
        '--no-examples',
        action='store_true',
        help='不生成示例代码'
    )

    parser.add_argument(
        '--with-local-lib',
        action='store_true',
        help='包含本地lib支持'
    )

    args = parser.parse_args()

    # 加载或创建配置
    if args.config:
        # 从文件加载
        config = load_config_from_file(args.config)
        if args.project_name:
            config['project_name'] = args.project_name
    else:
        # 从命令行参数创建
        if not args.project_name:
            parser.error("需要提供project_name或--config参数")

        config = create_default_config(
            args.project_name,
            base_dir=args.base_dir,
            group_id=args.group_id,
            package_name=args.package_name,
            java_version=args.java_version,
            spring_boot_version=args.spring_boot_version,
            template=args.template,
            include_examples=not args.no_examples,
            include_local_lib=args.with_local_lib
        )

    # 生成项目
    generator = AdvancedProjectGenerator(config)
    generator.generate()


if __name__ == '__main__':
    main()
