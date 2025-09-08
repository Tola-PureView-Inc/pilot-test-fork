#!/usr/bin/env python3
"""
Coding Agent - A simple code review tool

This script analyzes code files and provides basic review feedback including:
- Code quality checks
- Security vulnerability detection
- Style and formatting suggestions
- Documentation completeness
"""

import os
import sys
import argparse
import yaml
import re
from pathlib import Path
from typing import List, Dict, Any


class CodeReview:
    """Represents a code review with findings and suggestions"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.findings = []
        self.suggestions = []
        self.severity_counts = {"high": 0, "medium": 0, "low": 0}
    
    def add_finding(self, line_num: int, severity: str, category: str, message: str):
        """Add a review finding"""
        finding = {
            "line": line_num,
            "severity": severity,
            "category": category,
            "message": message
        }
        self.findings.append(finding)
        self.severity_counts[severity] += 1
    
    def add_suggestion(self, suggestion: str):
        """Add a general suggestion"""
        self.suggestions.append(suggestion)


class CodingAgent:
    """Main coding agent class for performing code reviews"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        self.supported_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs'}
    
    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        default_config = {
            "max_line_length": 100,
            "check_security": True,
            "check_style": True,
            "check_documentation": True,
            "ignore_patterns": ["*.min.js", "node_modules/*", "__pycache__/*"]
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                default_config.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config file {config_path}: {e}")
        
        return default_config
    
    def should_ignore_file(self, file_path: str) -> bool:
        """Check if file should be ignored based on patterns"""
        for pattern in self.config.get("ignore_patterns", []):
            if re.match(pattern.replace("*", ".*"), file_path):
                return True
        return False
    
    def check_python_file(self, file_path: str, content: str) -> CodeReview:
        """Perform Python-specific code review"""
        review = CodeReview(file_path)
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > self.config["max_line_length"]:
                review.add_finding(
                    i, "medium", "style",
                    f"Line too long ({len(line)} > {self.config['max_line_length']} chars)"
                )
            
            # Security checks
            if self.config["check_security"]:
                if "eval(" in line or "exec(" in line:
                    review.add_finding(
                        i, "high", "security",
                        "Potential security risk: use of eval() or exec()"
                    )
                
                if "subprocess.call" in line and "shell=True" in line:
                    review.add_finding(
                        i, "high", "security",
                        "Security risk: subprocess with shell=True"
                    )
            
            # Style checks
            if self.config["check_style"]:
                if line.strip().endswith(";;"):
                    review.add_finding(
                        i, "low", "style",
                        "Double semicolon not needed in Python"
                    )
                
                if re.search(r'\s+$', line):
                    review.add_finding(
                        i, "low", "style",
                        "Trailing whitespace"
                    )
        
        # Check for documentation
        if self.config["check_documentation"]:
            if not any("def " in line and '"""' in content[content.find(line):content.find(line)+200] 
                      for line in lines if "def " in line):
                review.add_suggestion("Consider adding docstrings to functions")
            
            if "class " in content and '"""' not in content:
                review.add_suggestion("Consider adding class documentation")
        
        return review
    
    def check_javascript_file(self, file_path: str, content: str) -> CodeReview:
        """Perform JavaScript-specific code review"""
        review = CodeReview(file_path)
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > self.config["max_line_length"]:
                review.add_finding(
                    i, "medium", "style",
                    f"Line too long ({len(line)} > {self.config['max_line_length']} chars)"
                )
            
            # Security checks
            if self.config["check_security"]:
                if "eval(" in line:
                    review.add_finding(
                        i, "high", "security",
                        "Security risk: use of eval()"
                    )
                
                if "innerHTML" in line and "+" in line:
                    review.add_finding(
                        i, "medium", "security",
                        "Potential XSS vulnerability with innerHTML"
                    )
            
            # Style checks
            if self.config["check_style"]:
                if "==" in line and "===" not in line:
                    review.add_finding(
                        i, "medium", "style",
                        "Consider using === instead of =="
                    )
                
                if "var " in line:
                    review.add_finding(
                        i, "low", "style",
                        "Consider using let or const instead of var"
                    )
        
        return review
    
    def review_file(self, file_path: str) -> CodeReview:
        """Review a single file"""
        if self.should_ignore_file(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.py':
            return self.check_python_file(file_path, content)
        elif file_ext in ['.js', '.ts']:
            return self.check_javascript_file(file_path, content)
        else:
            # Generic checks for other file types
            review = CodeReview(file_path)
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                if len(line) > self.config["max_line_length"]:
                    review.add_finding(
                        i, "medium", "style",
                        f"Line too long ({len(line)} > {self.config['max_line_length']} chars)"
                    )
                
                if re.search(r'\s+$', line):
                    review.add_finding(
                        i, "low", "style",
                        "Trailing whitespace"
                    )
            
            return review
    
    def review_directory(self, directory: str) -> List[CodeReview]:
        """Review all code files in a directory"""
        reviews = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if Path(file).suffix.lower() in self.supported_extensions:
                    review = self.review_file(file_path)
                    if review and (review.findings or review.suggestions):
                        reviews.append(review)
        
        return reviews
    
    def generate_report(self, reviews: List[CodeReview]) -> str:
        """Generate a formatted report from reviews"""
        if not reviews:
            return "✅ No issues found! Code looks good."
        
        report = ["🔍 Code Review Report", "=" * 50, ""]
        
        total_findings = sum(len(review.findings) for review in reviews)
        total_high = sum(review.severity_counts["high"] for review in reviews)
        total_medium = sum(review.severity_counts["medium"] for review in reviews)
        total_low = sum(review.severity_counts["low"] for review in reviews)
        
        report.extend([
            f"📊 Summary:",
            f"  Files reviewed: {len(reviews)}",
            f"  Total findings: {total_findings}",
            f"  🔴 High severity: {total_high}",
            f"  🟡 Medium severity: {total_medium}",
            f"  🟢 Low severity: {total_low}",
            ""
        ])
        
        for review in reviews:
            if review.findings or review.suggestions:
                report.extend([
                    f"📁 {review.file_path}",
                    "-" * len(f"📁 {review.file_path}"),
                    ""
                ])
                
                # Group findings by severity
                for severity in ["high", "medium", "low"]:
                    severity_findings = [f for f in review.findings if f["severity"] == severity]
                    if severity_findings:
                        emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}[severity]
                        report.append(f"  {emoji} {severity.upper()} SEVERITY:")
                        for finding in severity_findings:
                            report.append(f"    Line {finding['line']}: {finding['message']} [{finding['category']}]")
                        report.append("")
                
                if review.suggestions:
                    report.append("  💡 SUGGESTIONS:")
                    for suggestion in review.suggestions:
                        report.append(f"    • {suggestion}")
                    report.append("")
        
        return "\n".join(report)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Coding Agent - Code Review Tool")
    parser.add_argument("target", help="File or directory to review")
    parser.add_argument("--config", default="config.yaml", help="Configuration file path")
    parser.add_argument("--output", help="Output file for report (default: stdout)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.target):
        print(f"Error: {args.target} does not exist")
        sys.exit(1)
    
    agent = CodingAgent(args.config)
    
    if os.path.isfile(args.target):
        reviews = [agent.review_file(args.target)]
        reviews = [r for r in reviews if r]  # Filter out None results
    else:
        reviews = agent.review_directory(args.target)
    
    report = agent.generate_report(reviews)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()