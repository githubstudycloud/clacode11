#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maven本地Jar依赖管理工具

功能：
1. 根据配置文件自动生成lib目录结构
2. 复制jar文件到指定位置
3. 自动生成maven-install-plugin配置
4. 支持公共模块和子项目私有依赖
"""

import os
import sys
import shutil
import yaml
import argparse
from pathlib import Path
from typing import Dict, List
from xml.etree import ElementTree as ET
from xml.dom import minidom


class LibManager:
    """本地库管理器"""

    def __init__(self, config_file: str):
        """初始化管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = Path(config_file)
        self.base_dir = self.config_file.parent
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载配置文件"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        return config

    def _resolve_path(self, path: str) -> Path:
        """解析相对路径为绝对路径

        Args:
            path: 相对路径

        Returns:
            绝对路径
        """
        rel_path = Path(path)
        if rel_path.is_absolute():
            return rel_path
        return (self.base_dir / rel_path).resolve()

    def setup_directories(self):
        """创建必要的目录结构"""
        print("\n=== 创建目录结构 ===")

        # 创建jar源目录
        jar_base = self._resolve_path(self.config['jar_sources']['base_dir'])
        jar_base.mkdir(parents=True, exist_ok=True)
        print(f"[OK] 创建jar源目录: {jar_base}")

        # 创建公共模块lib目录
        if 'common' in self.config and self.config['common']:
            common_lib = self._resolve_path(self.config['common']['lib_dir'])
            common_lib.mkdir(parents=True, exist_ok=True)
            print(f"[OK] 创建公共模块lib目录: {common_lib}")

        # 创建子项目lib目录
        if 'modules' in self.config and self.config['modules']:
            for module in self.config['modules']:
                if not module:  # 跳过空配置
                    continue
                module_lib = self._resolve_path(module['lib_dir'])
                module_lib.mkdir(parents=True, exist_ok=True)
                print(f"[OK] 创建模块lib目录: {module_lib}")

        print("目录结构创建完成!\n")

    def copy_jars(self):
        """复制jar文件到各个模块的lib目录"""
        print("\n=== 复制JAR文件 ===")
        jar_base = self._resolve_path(self.config['jar_sources']['base_dir'])

        # 处理公共模块的jar
        if 'common' in self.config and self.config['common']:
            common_config = self.config['common']
            if 'dependencies' in common_config and common_config['dependencies']:
                self._copy_module_jars(jar_base, common_config, "公共模块")

        # 处理子项目的jar
        if 'modules' in self.config and self.config['modules']:
            for module in self.config['modules']:
                if not module:  # 跳过空配置
                    continue
                self._copy_module_jars(jar_base, module, f"模块 {module['module_name']}")

        print("JAR文件复制完成!\n")

    def _copy_module_jars(self, jar_base: Path, module_config: Dict, module_name: str):
        """复制单个模块的jar文件

        Args:
            jar_base: jar源目录
            module_config: 模块配置
            module_name: 模块名称（用于显示）
        """
        lib_dir = self._resolve_path(module_config['lib_dir'])
        dependencies = module_config.get('dependencies', [])

        if not dependencies:
            print(f"  [{module_name}] 无jar依赖配置")
            return

        for dep in dependencies:
            jar_file = dep['jar_file']
            src_file = jar_base / jar_file
            dst_file = lib_dir / jar_file

            if not src_file.exists():
                print(f"  [ERR] [{module_name}] 源文件不存在: {src_file}")
                continue

            shutil.copy2(src_file, dst_file)
            print(f"  [OK] [{module_name}] 复制: {jar_file}")

    def generate_pom_config(self, output_file: str = None):
        """生成Maven POM配置文件

        Args:
            output_file: 输出文件路径，默认为当前目录下的generated-pom-configs.xml
        """
        print("\n=== 生成Maven配置 ===")

        if output_file is None:
            output_file = self.base_dir / "generated-pom-configs.xml"
        else:
            output_file = Path(output_file)

        # 生成XML内容
        configs = []

        # 公共模块配置
        if 'common' in self.config and self.config['common']:
            common_config = self.config['common']
            if 'dependencies' in common_config and common_config['dependencies']:
                config = self._generate_module_pom_config(common_config, "公共模块 (common)")
                configs.append(config)

        # 子项目配置
        if 'modules' in self.config and self.config['modules']:
            for module in self.config['modules']:
                if not module:
                    continue
                config = self._generate_module_pom_config(module, f"模块 ({module['module_name']})")
                configs.append(config)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<!--\n')
            f.write('  自动生成的Maven POM配置片段\n')
            f.write('  \n')
            f.write('  使用方法：\n')
            f.write('  1. 复制对应模块的 <plugin> 配置到该模块的 pom.xml 的 <build><plugins> 中\n')
            f.write('  2. 复制对应模块的 <dependency> 配置到该模块的 pom.xml 的 <dependencies> 中\n')
            f.write('  3. 确保 lib 目录中有相应的 jar 文件\n')
            f.write('-->\n\n')
            f.write('<maven-configs>\n\n')

            for config in configs:
                f.write(config)
                f.write('\n\n')

            f.write('</maven-configs>\n')

        print(f"[OK] Maven配置已生成: {output_file}")
        print("\n请将生成的配置复制到对应模块的pom.xml中\n")

    def _generate_module_pom_config(self, module_config: Dict, title: str) -> str:
        """生成单个模块的POM配置

        Args:
            module_config: 模块配置
            title: 配置标题

        Returns:
            XML配置字符串
        """
        dependencies = module_config.get('dependencies', [])
        if not dependencies:
            return f"  <!-- {title}: 无jar依赖 -->"

        lines = []
        lines.append(f"  <!-- ========== {title} ========== -->")
        lines.append("")
        lines.append("  <!-- 第1步: 添加到 <build><plugins> 中 -->")
        lines.append("  <plugin>")
        lines.append("    <groupId>org.apache.maven.plugins</groupId>")
        lines.append("    <artifactId>maven-install-plugin</artifactId>")
        lines.append("    <version>2.5.2</version>")
        lines.append("    <executions>")

        for dep in dependencies:
            execution_id = f"install-{dep['artifact_id']}"
            lines.append(f"      <!-- {dep.get('description', dep['artifact_id'])} -->")
            lines.append("      <execution>")
            lines.append(f"        <id>{execution_id}</id>")
            lines.append("        <phase>validate</phase>")
            lines.append("        <goals>")
            lines.append("          <goal>install-file</goal>")
            lines.append("        </goals>")
            lines.append("        <configuration>")
            lines.append(f"          <file>${{project.basedir}}/lib/{dep['jar_file']}</file>")
            lines.append(f"          <groupId>{dep['group_id']}</groupId>")
            lines.append(f"          <artifactId>{dep['artifact_id']}</artifactId>")
            lines.append(f"          <version>{dep['version']}</version>")
            lines.append("          <packaging>jar</packaging>")
            lines.append("          <generatePom>true</generatePom>")
            lines.append("        </configuration>")
            lines.append("      </execution>")

        lines.append("    </executions>")
        lines.append("  </plugin>")
        lines.append("")
        lines.append("  <!-- 第2步: 添加到 <dependencies> 中 -->")

        for dep in dependencies:
            lines.append(f"  <!-- {dep.get('description', dep['artifact_id'])} -->")
            lines.append("  <dependency>")
            lines.append(f"    <groupId>{dep['group_id']}</groupId>")
            lines.append(f"    <artifactId>{dep['artifact_id']}</artifactId>")
            lines.append(f"    <version>{dep['version']}</version>")
            lines.append("  </dependency>")

        return '\n'.join(lines)

    def generate_readme(self):
        """在各个lib目录生成README文件"""
        print("\n=== 生成README文件 ===")

        # 公共模块README
        if 'common' in self.config and self.config['common']:
            common_config = self.config['common']
            if 'dependencies' in common_config and common_config['dependencies']:
                lib_dir = self._resolve_path(common_config['lib_dir'])
                self._generate_lib_readme(lib_dir, common_config, "公共模块")

        # 子项目README
        if 'modules' in self.config and self.config['modules']:
            for module in self.config['modules']:
                if not module:
                    continue
                lib_dir = self._resolve_path(module['lib_dir'])
                self._generate_lib_readme(lib_dir, module, module['module_name'])

        print("README文件生成完成!\n")

    def _generate_lib_readme(self, lib_dir: Path, module_config: Dict, module_name: str):
        """生成单个lib目录的README

        Args:
            lib_dir: lib目录路径
            module_config: 模块配置
            module_name: 模块名称
        """
        readme_file = lib_dir / "README.md"
        dependencies = module_config.get('dependencies', [])

        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# {module_name} - 本地Jar依赖说明\n\n")
            f.write("## 依赖清单\n\n")

            if not dependencies:
                f.write("暂无本地jar依赖\n")
            else:
                f.write("| Jar文件 | GroupId | ArtifactId | Version | 说明 |\n")
                f.write("|---------|---------|------------|---------|------|\n")

                for dep in dependencies:
                    jar = dep['jar_file']
                    group = dep['group_id']
                    artifact = dep['artifact_id']
                    version = dep['version']
                    desc = dep.get('description', '-')
                    f.write(f"| {jar} | {group} | {artifact} | {version} | {desc} |\n")

            f.write("\n## 使用说明\n\n")
            f.write("这些jar文件通过maven-install-plugin在构建时自动安装到本地Maven仓库。\n\n")
            f.write("### 构建时自动安装\n\n")
            f.write("```bash\n")
            f.write("mvn clean install\n")
            f.write("```\n\n")
            f.write("### 验证依赖\n\n")
            f.write("```bash\n")
            f.write("mvn dependency:tree\n")
            f.write("```\n\n")
            f.write("## 注意事项\n\n")
            f.write("1. 这些jar文件已提交到Git仓库\n")
            f.write("2. 构建时会自动处理，无需手动安装\n")
            f.write("3. Jenkins构建时也会自动处理\n\n")
            f.write("## 更新历史\n\n")
            f.write("- 由 lib_manager.py 自动生成\n")

        print(f"  [OK] 生成README: {readme_file}")

    def run_all(self):
        """执行所有操作"""
        print("=" * 60)
        print(" Maven本地Jar依赖管理工具")
        print("=" * 60)

        self.setup_directories()
        self.copy_jars()
        self.generate_pom_config()
        self.generate_readme()

        print("=" * 60)
        print(" 处理完成!")
        print("=" * 60)
        print("\n下一步操作:")
        print("1. 将生成的 generated-pom-configs.xml 中的配置复制到对应模块的 pom.xml")
        print("2. 运行 mvn clean install 验证配置")
        print("3. 提交lib目录和pom.xml到Git仓库")
        print()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Maven本地Jar依赖管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --config jars-config.yaml --all           # 执行所有操作
  %(prog)s --config jars-config.yaml --setup         # 只创建目录
  %(prog)s --config jars-config.yaml --copy          # 只复制jar文件
  %(prog)s --config jars-config.yaml --generate      # 只生成配置
  %(prog)s --config jars-config.yaml --readme        # 只生成README
        """
    )

    parser.add_argument(
        '--config',
        default='jars-config.yaml',
        help='配置文件路径 (默认: jars-config.yaml)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='执行所有操作（创建目录、复制jar、生成配置、生成README）'
    )

    parser.add_argument(
        '--setup',
        action='store_true',
        help='只创建目录结构'
    )

    parser.add_argument(
        '--copy',
        action='store_true',
        help='只复制jar文件'
    )

    parser.add_argument(
        '--generate',
        action='store_true',
        help='只生成Maven POM配置'
    )

    parser.add_argument(
        '--readme',
        action='store_true',
        help='只生成README文件'
    )

    parser.add_argument(
        '--output',
        help='生成的配置文件输出路径 (默认: generated-pom-configs.xml)'
    )

    args = parser.parse_args()

    # 如果没有指定任何操作，默认执行全部
    if not any([args.all, args.setup, args.copy, args.generate, args.readme]):
        args.all = True

    try:
        manager = LibManager(args.config)

        if args.all:
            manager.run_all()
        else:
            if args.setup:
                manager.setup_directories()
            if args.copy:
                manager.copy_jars()
            if args.generate:
                manager.generate_pom_config(args.output)
            if args.readme:
                manager.generate_readme()

    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
