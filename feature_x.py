#!/usr/bin/env python3
"""
Feature X - File Information and Repository Manager

This script provides utility functions for managing and analyzing files
in the pilot-test-fork repository.

Author: Generated for pilot-test-fork
"""

import os
import sys
from pathlib import Path
import hashlib
from datetime import datetime


class FeatureX:
    """
    Feature X implementation - A simple file management and analysis utility.
    """
    
    def __init__(self, repo_path="."):
        """Initialize Feature X with repository path."""
        self.repo_path = Path(repo_path)
        self.supported_formats = {
            '.mp4': 'Video',
            '.md': 'Markdown',
            '.txt': 'Text',
            '.py': 'Python',
            '.zip': 'Archive'
        }
    
    def get_file_info(self, filepath):
        """Get detailed information about a file."""
        file_path = Path(filepath)
        
        if not file_path.exists():
            return None
            
        stat = file_path.stat()
        file_type = self.supported_formats.get(file_path.suffix.lower(), 'Unknown')
        
        return {
            'name': file_path.name,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'type': file_type,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'extension': file_path.suffix.lower()
        }
    
    def analyze_repository(self):
        """Analyze all files in the repository."""
        files_info = []
        total_size = 0
        
        for file_path in self.repo_path.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                info = self.get_file_info(file_path)
                if info:
                    files_info.append(info)
                    total_size += info['size']
        
        return {
            'files': files_info,
            'total_files': len(files_info),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'file_types': self._get_file_type_summary(files_info)
        }
    
    def _get_file_type_summary(self, files_info):
        """Get summary of file types in the repository."""
        type_counts = {}
        for file_info in files_info:
            file_type = file_info['type']
            type_counts[file_type] = type_counts.get(file_type, 0) + 1
        return type_counts
    
    def generate_report(self):
        """Generate a comprehensive repository report."""
        analysis = self.analyze_repository()
        
        print("=" * 60)
        print("FEATURE X - REPOSITORY ANALYSIS REPORT")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Repository: {self.repo_path.absolute()}")
        print()
        
        print(f"📊 SUMMARY:")
        print(f"   Total Files: {analysis['total_files']}")
        print(f"   Total Size: {analysis['total_size_mb']} MB")
        print()
        
        print(f"📁 FILE TYPES:")
        for file_type, count in analysis['file_types'].items():
            print(f"   {file_type}: {count} files")
        print()
        
        print(f"📄 DETAILED FILE LIST:")
        for file_info in sorted(analysis['files'], key=lambda x: x['size'], reverse=True):
            print(f"   {file_info['name']:<25} | {file_info['size_mb']:>8} MB | {file_info['type']:<10} | {file_info['modified']}")
        
        print("=" * 60)
        
        return analysis


def main():
    """Main function to run Feature X."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Feature X - File Information and Repository Manager")
            print("Usage: python feature_x.py [options]")
            print("Options:")
            print("  --help, -h    Show this help message")
            print("  --version     Show version information")
            return
        elif sys.argv[1] == '--version':
            print("Feature X v1.0.0")
            return
    
    # Initialize Feature X
    feature_x = FeatureX()
    
    # Generate and display report
    try:
        feature_x.generate_report()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()