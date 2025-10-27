#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maven多模块项目工具集 - 统一入口

集成所有工具的统一命令行界面
"""

import sys
import argparse
from pathlib import Path


def print_banner():
    """打印横幅"""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║          Maven Multi-Module Project Toolkit                   ║
║          Maven多模块项目工具集                                  ║
║                                                                ║
║          Version: 2.0                                          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def show_menu():
    """显示主菜单"""
    menu = """
📋 可用工具:

1️⃣  项目生成器 (基础版)
   - 快速创建标准Maven多模块项目
   - 命令: python project-generator.py <项目名>

2️⃣  项目生成器 (高级版) ⭐ 推荐
   - 支持自定义包名、路径、端口等
   - 支持配置文件
   - 命令: python project-generator-advanced.py <项目名>
   - 配置: python project-generator-advanced.py --config config.yaml

3️⃣  测试运行器
   - 自动化测试所有功能
   - 生成详细测试报告
   - 命令: python test-runner.py [--format html|markdown|json]

4️⃣  本地库管理器
   - 管理本地jar依赖
   - 自动生成Maven配置
   - 命令: cd ../local-lib-manager && python lib_manager.py --all

5️⃣  完整测试流程
   - 生成项目 → 测试 → 生成报告
   - 命令: python maven-tools.py test-flow

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 快速开始示例:

# 创建标准项目
python project-generator-advanced.py my-project

# 使用配置文件创建项目
python project-generator-advanced.py --config project-config-example.yaml

# 自定义包名和groupId
python project-generator-advanced.py my-project \\
  --group-id com.mycompany \\
  --package-name com/mycompany/myapp

# 测试项目并生成HTML报告
python test-runner.py --format html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 文档:
- 完整教学指南: ../docs/TEACHING_GUIDE.md
- 快速入门: ../QUICKSTART_CN.md
- 练习题集: ../docs/EXERCISES.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(menu)


def run_test_flow():
    """运行完整测试流程"""
    print("\n" + "="*60)
    print(" 完整测试流程")
    print("="*60)

    import subprocess
    import os

    steps = [
        {
            'name': '1. 生成测试项目',
            'cmd': [sys.executable, 'project-generator-advanced.py',
                   'test-demo-project',
                   '--group-id', 'com.test.demo']
        },
        {
            'name': '2. 构建测试项目',
            'cmd': ['mvn', 'clean', 'install', '-DskipTests'],
            'cwd': 'test-demo-project'
        },
        {
            'name': '3. 运行测试',
            'cmd': [sys.executable, 'test-runner.py',
                   '--project-dir', 'test-demo-project',
                   '--format', 'html']
        }
    ]

    for step in steps:
        print(f"\n{'='*60}")
        print(f" {step['name']}")
        print(f"{'='*60}\n")

        cwd = step.get('cwd', '.')
        try:
            result = subprocess.run(
                step['cmd'],
                cwd=cwd,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"❌ 失败: {step['name']}")
                print(result.stdout)
                print(result.stderr)
                return False
            else:
                print(f"✅ 成功: {step['name']}")

        except Exception as e:
            print(f"❌ 错误: {e}")
            return False

    print("\n" + "="*60)
    print(" ✅ 完整测试流程成功完成！")
    print("="*60)
    print("\n生成的文件:")
    print("  - 测试项目: test-demo-project/")
    print("  - 测试报告: test-demo-project/test-reports/")
    print()

    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Maven多模块项目工具集 - 统一入口',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'command',
        nargs='?',
        choices=['menu', 'test-flow', 'help'],
        default='menu',
        help='命令: menu(菜单), test-flow(完整测试), help(帮助)'
    )

    args = parser.parse_args()

    print_banner()

    if args.command == 'menu' or args.command == 'help':
        show_menu()
    elif args.command == 'test-flow':
        run_test_flow()


if __name__ == '__main__':
    main()
