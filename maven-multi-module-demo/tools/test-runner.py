#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maven多模块项目测试工具

功能：
1. 自动化测试所有模块
2. 测试API接口
3. 生成测试报告
4. 验证依赖关系
"""

import os
import sys
import subprocess
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class TestRunner:
    """测试运行器"""

    def __init__(self, project_dir: str = "."):
        """初始化测试运行器

        Args:
            project_dir: 项目根目录
        """
        self.project_dir = Path(project_dir).resolve()
        self.report_dir = self.project_dir / "test-reports"
        self.report_dir.mkdir(exist_ok=True)
        self.test_results = []

    def run_maven_test(self, module: str = None) -> Tuple[bool, str]:
        """运行Maven测试

        Args:
            module: 模块名称，None表示测试所有模块

        Returns:
            (是否成功, 输出信息)
        """
        cmd = ["mvn", "clean", "test"]
        cwd = self.project_dir / module if module else self.project_dir

        print(f"\n{'='*60}")
        print(f" 运行Maven测试: {module or '所有模块'}")
        print(f"{'='*60}")

        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            success = result.returncode == 0
            output = result.stdout + result.stderr

            return success, output

        except Exception as e:
            return False, str(e)

    def run_maven_build(self) -> Tuple[bool, str]:
        """运行完整构建

        Returns:
            (是否成功, 输出信息)
        """
        print(f"\n{'='*60}")
        print(" 运行完整构建: mvn clean install")
        print(f"{'='*60}")

        try:
            result = subprocess.run(
                ["mvn", "clean", "install"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            success = result.returncode == 0
            output = result.stdout + result.stderr

            return success, output

        except Exception as e:
            return False, str(e)

    def check_dependency_tree(self, module: str) -> Tuple[bool, str]:
        """检查依赖树

        Args:
            module: 模块名称

        Returns:
            (是否成功, 依赖树信息)
        """
        print(f"\n检查 {module} 的依赖树...")

        try:
            result = subprocess.run(
                ["mvn", "dependency:tree"],
                cwd=self.project_dir / module,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            success = result.returncode == 0
            output = result.stdout

            return success, output

        except Exception as e:
            return False, str(e)

    def test_api_endpoint(self, url: str, expected_keys: List[str] = None) -> Tuple[bool, Dict]:
        """测试API接口

        Args:
            url: API地址
            expected_keys: 期望的响应键

        Returns:
            (是否成功, 响应数据)
        """
        try:
            import urllib.request
            import urllib.error

            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))

                if expected_keys:
                    for key in expected_keys:
                        if key not in data:
                            return False, {"error": f"Missing key: {key}"}

                return True, data

        except Exception as e:
            return False, {"error": str(e)}

    def run_full_test(self) -> Dict:
        """运行完整测试套件

        Returns:
            测试结果字典
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }

        # 1. 测试构建
        print("\n" + "="*60)
        print(" 第1步: 测试Maven构建")
        print("="*60)

        build_success, build_output = self.run_maven_build()
        results["tests"].append({
            "name": "Maven构建",
            "passed": build_success,
            "output": build_output[:1000] if len(build_output) > 1000 else build_output
        })

        if not build_success:
            print("❌ 构建失败，停止后续测试")
            results["summary"] = {
                "total": 1,
                "passed": 0,
                "failed": 1,
                "success_rate": "0%"
            }
            return results

        print("✅ 构建成功")

        # 2. 检查依赖
        print("\n" + "="*60)
        print(" 第2步: 检查模块依赖")
        print("="*60)

        modules = ["service-a", "module-group/service-b"]
        for module in modules:
            dep_success, dep_output = self.check_dependency_tree(module)
            results["tests"].append({
                "name": f"{module}依赖检查",
                "passed": dep_success,
                "output": dep_output[:1000] if len(dep_output) > 1000 else dep_output
            })

            if dep_success:
                # 检查是否包含common模块
                has_common = "com.example:common" in dep_output
                results["tests"].append({
                    "name": f"{module}包含common依赖",
                    "passed": has_common,
                    "output": "找到common模块依赖" if has_common else "未找到common模块依赖"
                })
                print(f"  {'✅' if has_common else '❌'} {module} 依赖common模块")
            else:
                print(f"  ❌ {module} 依赖检查失败")

        # 3. 单元测试
        print("\n" + "="*60)
        print(" 第3步: 运行单元测试")
        print("="*60)

        test_modules = ["common", "service-a", "module-group/service-b"]
        for module in test_modules:
            test_success, test_output = self.run_maven_test(module)
            results["tests"].append({
                "name": f"{module}单元测试",
                "passed": test_success,
                "output": test_output[:1000] if len(test_output) > 1000 else test_output
            })

            print(f"  {'✅' if test_success else '❌'} {module} 测试")

        # 统计结果
        total_tests = len(results["tests"])
        passed_tests = sum(1 for t in results["tests"] if t["passed"])
        failed_tests = total_tests - passed_tests
        success_rate = f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%"

        results["summary"] = {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": success_rate
        }

        return results

    def generate_report(self, results: Dict, format: str = "markdown") -> str:
        """生成测试报告

        Args:
            results: 测试结果
            format: 报告格式 (markdown, html, json)

        Returns:
            报告文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "json":
            report_file = self.report_dir / f"test_report_{timestamp}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

        elif format == "html":
            report_file = self.report_dir / f"test_report_{timestamp}.html"
            html_content = self._generate_html_report(results)
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

        else:  # markdown
            report_file = self.report_dir / f"test_report_{timestamp}.md"
            md_content = self._generate_markdown_report(results)
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(md_content)

        return str(report_file)

    def _generate_markdown_report(self, results: Dict) -> str:
        """生成Markdown格式报告"""
        lines = []
        lines.append("# Maven多模块项目测试报告\n")
        lines.append(f"**测试时间**: {results['timestamp']}\n")
        lines.append("## 测试总结\n")

        summary = results['summary']
        lines.append(f"- **总测试数**: {summary['total']}")
        lines.append(f"- **通过数**: {summary['passed']} ✅")
        lines.append(f"- **失败数**: {summary['failed']} ❌")
        lines.append(f"- **成功率**: {summary['success_rate']}\n")

        lines.append("## 详细结果\n")
        lines.append("| 测试项 | 状态 | 说明 |")
        lines.append("|--------|------|------|")

        for test in results['tests']:
            status = "✅ 通过" if test['passed'] else "❌ 失败"
            name = test['name']
            output = test['output'][:50] + "..." if len(test['output']) > 50 else test['output']
            lines.append(f"| {name} | {status} | {output} |")

        lines.append("\n## 建议\n")

        if summary['failed'] == 0:
            lines.append("🎉 所有测试通过！项目配置正确。\n")
        else:
            lines.append("⚠️ 存在失败的测试，请检查以下内容：\n")
            lines.append("1. Maven依赖配置是否正确")
            lines.append("2. 本地lib目录中的jar文件是否存在")
            lines.append("3. maven-install-plugin配置是否正确")
            lines.append("4. 模块间依赖关系是否正确\n")

        return '\n'.join(lines)

    def _generate_html_report(self, results: Dict) -> str:
        """生成HTML格式报告"""
        summary = results['summary']

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maven多模块项目测试报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #666;
        }}
        .summary-card .value {{
            font-size: 32px;
            font-weight: bold;
        }}
        .passed {{ color: #27ae60; }}
        .failed {{ color: #e74c3c; }}
        table {{
            width: 100%;
            background: white;
            border-collapse: collapse;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #34495e;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Maven多模块项目测试报告</h1>
        <p>测试时间: {results['timestamp']}</p>
    </div>

    <div class="summary">
        <div class="summary-card">
            <h3>总测试数</h3>
            <div class="value">{summary['total']}</div>
        </div>
        <div class="summary-card">
            <h3>通过</h3>
            <div class="value passed">{summary['passed']}</div>
        </div>
        <div class="summary-card">
            <h3>失败</h3>
            <div class="value failed">{summary['failed']}</div>
        </div>
        <div class="summary-card">
            <h3>成功率</h3>
            <div class="value">{summary['success_rate']}</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>测试项</th>
                <th>状态</th>
                <th>说明</th>
            </tr>
        </thead>
        <tbody>
'''

        for test in results['tests']:
            status = '<span class="passed">✅ 通过</span>' if test['passed'] else '<span class="failed">❌ 失败</span>'
            output = test['output'][:100] + "..." if len(test['output']) > 100 else test['output']
            html += f'''
            <tr>
                <td>{test['name']}</td>
                <td>{status}</td>
                <td>{output}</td>
            </tr>
'''

        html += '''
        </tbody>
    </table>
</body>
</html>
'''

        return html


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Maven多模块项目测试工具',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--project-dir',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )

    parser.add_argument(
        '--format',
        choices=['markdown', 'html', 'json'],
        default='markdown',
        help='报告格式 (默认: markdown)'
    )

    parser.add_argument(
        '--build-only',
        action='store_true',
        help='只运行构建测试'
    )

    args = parser.parse_args()

    print("=" * 60)
    print(" Maven多模块项目测试工具")
    print("=" * 60)

    runner = TestRunner(args.project_dir)

    if args.build_only:
        success, output = runner.run_maven_build()
        print("\n构建结果:", "✅ 成功" if success else "❌ 失败")
    else:
        results = runner.run_full_test()

        # 生成报告
        print("\n" + "=" * 60)
        print(" 生成测试报告")
        print("=" * 60)

        report_file = runner.generate_report(results, args.format)
        print(f"✅ 报告已生成: {report_file}")

        # 显示摘要
        print("\n" + "=" * 60)
        print(" 测试摘要")
        print("=" * 60)
        summary = results['summary']
        print(f"总测试数: {summary['total']}")
        print(f"通过: {summary['passed']} ✅")
        print(f"失败: {summary['failed']} ❌")
        print(f"成功率: {summary['success_rate']}")

        if summary['failed'] > 0:
            print("\n⚠️  存在失败的测试，请查看报告了解详情")
            sys.exit(1)
        else:
            print("\n🎉 所有测试通过！")


if __name__ == '__main__':
    main()
