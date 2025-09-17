# Example of good Python code

import os
from pathlib import Path
from typing import List, Optional


def process_files(file_paths: List[str]) -> Optional[List[str]]:
    """
    Process a list of file paths and return their contents.
    
    Args:
        file_paths: List of file paths to process
        
    Returns:
        List of file contents, or None if error occurred
    """
    results = []
    
    for file_path in file_paths:
        try:
            path = Path(file_path)
            if path.exists():
                content = path.read_text(encoding='utf-8')
                results.append(content)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    return results


class FileProcessor:
    """A class for processing files safely and efficiently."""
    
    def __init__(self, base_directory: str):
        """
        Initialize the file processor.
        
        Args:
            base_directory: Base directory for file operations
        """
        self.base_directory = Path(base_directory)
    
    def get_files(self, pattern: str = "*.txt") -> List[Path]:
        """
        Get all files matching the given pattern.
        
        Args:
            pattern: File pattern to match
            
        Returns:
            List of matching file paths
        """
        return list(self.base_directory.glob(pattern))


if __name__ == "__main__":
    processor = FileProcessor("./examples")
    files = processor.get_files("*.py")
    print(f"Found {len(files)} Python files")