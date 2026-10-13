"""
Utility functions for path validation, file handling, and system paths.
"""
import os
import re
from pathlib import Path


def get_user_home() -> str:
    """
    Get the current user's home directory path.
    
    Returns:
        str: Absolute path to user's home directory
    """
    return os.path.expanduser("~")


def get_downloads_folder() -> str:
    """
    Get the user's Downloads folder path.
    
    Returns:
        str: Absolute path to Downloads folder
    """
    return os.path.join(get_user_home(), "Downloads")


def is_path_safe(path: str) -> bool:
    """
    Check if a path is within the user's home directory.
    This prevents access to system directories.
    
    Args:
        path: Path to validate
        
    Returns:
        bool: True if path is safe (within home), False otherwise
    """
    try:
        home = get_user_home()
        # Resolve to absolute path to handle .. and symlinks
        resolved_path = os.path.realpath(path)
        resolved_home = os.path.realpath(home)
        
        return resolved_path.startswith(resolved_home)
    except Exception:
        return False


def is_valid_filename(filename: str) -> bool:
    """
    Check if a filename is valid for a PDF file.
    
    Rules:
    - Cannot be empty
    - Cannot contain invalid characters (/, \\, :, *, ?, ", <, >, |)
    - Must end with .pdf (case insensitive)
    - Cannot be too long (max 255 characters)
    
    Args:
        filename: Filename to validate
        
    Returns:
        bool: True if filename is valid, False otherwise
    """
    if not filename or not filename.strip():
        return False
    
    # Check length
    if len(filename) > 255:
        return False
    
    # Check for invalid characters
    invalid_chars = r'[\/\\:*?"<>|]'
    if re.search(invalid_chars, filename):
        return False
    
    # Check if ends with .pdf
    if not filename.lower().endswith('.pdf'):
        return False
    
    return True


def ensure_pdf_extension(filename: str) -> str:
    """
    Ensure filename ends with .pdf extension.
    If it doesn't, append .pdf to it.
    
    Args:
        filename: Filename to check
        
    Returns:
        str: Filename with .pdf extension
    """
    if not filename.lower().endswith('.pdf'):
        return f"{filename}.pdf"
    return filename


def file_exists(filepath: str) -> bool:
    """
    Check if a file already exists.
    
    Args:
        filepath: Full path to the file
        
    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.isfile(filepath)


def get_unique_filename(folder: str, filename: str) -> str:
    """
    Generate a unique filename if the original already exists.
    Adds a number suffix like (1), (2), etc.
    
    Args:
        folder: Folder path
        filename: Original filename
        
    Returns:
        str: Unique filename (may be modified if original exists)
    """
    filepath = os.path.join(folder, filename)
    
    if not file_exists(filepath):
        return filename
    
    # Extract name and extension
    name, ext = os.path.splitext(filename)
    
    # Try adding numbers until we find a unique name
    counter = 1
    while True:
        new_filename = f"{name} ({counter}){ext}"
        new_filepath = os.path.join(folder, new_filename)
        
        if not file_exists(new_filepath):
            return new_filename
        
        counter += 1
        
        # Safety limit to prevent infinite loop
        if counter > 999:
            raise ValueError("Cannot generate unique filename after 999 attempts")


def create_folder_if_not_exists(folder: str) -> bool:
    """
    Create a folder if it doesn't exist.
    
    Args:
        folder: Folder path to create
        
    Returns:
        bool: True if folder exists or was created successfully, False otherwise
    """
    try:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        return True
    except Exception:
        return False


def get_file_size_mb(filepath: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        filepath: Path to the file
        
    Returns:
        float: File size in MB, or 0.0 if file doesn't exist
    """
    try:
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0
