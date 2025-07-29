import os
from typing import List, Optional


def get_files_in_directory(directory_path: str, include_subdirectories: bool = False) -> List[str]:
    """
    Get a list of files in the specified directory.
    
    Args:
        directory_path (str): The path to the directory to scan
        include_subdirectories (bool): If True, includes files from subdirectories recursively
        
    Returns:
        List[str]: A list of file paths found in the directory
        
    Raises:
        FileNotFoundError: If the directory doesn't exist
        PermissionError: If access to the directory is denied
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Directory '{directory_path}' does not exist")
    
    if not os.path.isdir(directory_path):
        raise ValueError(f"'{directory_path}' is not a directory")
    
    files = []
    
    if include_subdirectories:
        # Walk through directory and subdirectories
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
    else:
        # Only get files in the specified directory (not subdirectories)
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                files.append(item_path)
    
    return files

