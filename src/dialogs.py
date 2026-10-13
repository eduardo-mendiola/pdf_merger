"""
Dialog functions using zenity for native GNOME file pickers.
All user communication happens through the console module.
"""
import subprocess
from typing import Optional, List
from src.utils import get_user_home, get_downloads_folder, is_path_safe


def _run_zenity(args: list) -> tuple[int, str]:
    """
    Internal helper to run zenity command and capture output.
    
    Args:
        args: List of zenity arguments
        
    Returns:
        tuple: (return_code, output_text)
    """
    try:
        result = subprocess.run(
            ["zenity"] + args,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return -1, ""
    except FileNotFoundError:
        return -1, ""
    except Exception:
        return -1, ""


def select_pdf_file() -> Optional[str]:
    """
    Open a native GNOME file dialog to select a single PDF file.
    Only allows selection from the user's home directory for security.
    
    Returns:
        Optional[str]: Absolute path to selected PDF, or None if cancelled
    """
    home_dir = get_user_home()
    
    returncode, output = _run_zenity([
        "--file-selection",
        "--title=Select a PDF file",
        "--file-filter=PDF files | *.pdf",
        f"--filename={home_dir}/"
    ])
    
    if returncode != 0 or not output:
        return None
    
    selected_path = output
    
    if not is_path_safe(selected_path):
        return None
    
    return selected_path


def select_multiple_pdf_files() -> Optional[List[str]]:
    """
    Open a native GNOME file dialog to select multiple PDF files.
    User can select multiple files using Ctrl+click or Shift+click.
    Only allows selection from the user's home directory for security.
    
    Returns:
        Optional[List[str]]: List of absolute paths to selected PDFs, or None if cancelled
    """
    home_dir = get_user_home()
    
    returncode, output = _run_zenity([
        "--file-selection",
        "--multiple",
        "--separator=|",
        "--title=Select PDF files (Ctrl+click or Shift+click for multiple)",
        "--file-filter=PDF files | *.pdf",
        f"--filename={home_dir}/"
    ])
    
    if returncode != 0 or not output:
        return None
    
    # Zenity returns paths separated by |
    selected_paths = output.split("|")
    
    # Validate all paths
    valid_paths = []
    for path in selected_paths:
        path = path.strip()
        if path and is_path_safe(path):
            valid_paths.append(path)
    
    return valid_paths if valid_paths else None


def select_folder_for_pdfs() -> Optional[str]:
    """
    Open a native GNOME folder dialog to select a folder containing PDFs.
    Only allows selection from the user's home directory for security.
    
    Returns:
        Optional[str]: Absolute path to selected folder, or None if cancelled
    """
    home_dir = get_user_home()
    
    returncode, output = _run_zenity([
        "--file-selection",
        "--directory",
        "--title=Select a folder containing PDF files",
        f"--filename={home_dir}/"
    ])
    
    if returncode != 0 or not output:
        return None
    
    selected_folder = output
    
    if not is_path_safe(selected_folder):
        return None
    
    return selected_folder


def select_output_file() -> Optional[str]:
    """
    Open a native GNOME file dialog to choose folder AND filename for the output PDF.
    Opens in Downloads folder by default with a default filename.
    User can navigate to any folder and modify the filename.
    Zenity will warn if file already exists.
    
    Returns:
        Optional[str]: Absolute path to output file, or None if cancelled
    """
    downloads_dir = get_downloads_folder()
    default_filename = "MERGED_PDF_FINAL.pdf"
    default_path = f"{downloads_dir}/{default_filename}"
    
    returncode, output = _run_zenity([
        "--file-selection",
        "--save",
        "--confirm-overwrite",
        "--title=Save merged PDF as",
        "--file-filter=PDF files | *.pdf",
        f"--filename={default_path}"
    ])
    
    if returncode != 0 or not output:
        return None
    
    selected_path = output
    
    if not is_path_safe(selected_path):
        return None
    
    return selected_path