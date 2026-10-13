"""
PDF compression logic using Ghostscript.
Provides reliable, high-quality image downsampling without affecting text/vector graphics.
"""
import os
import subprocess
import tempfile
from typing import Optional


class CompressionError(Exception):
    """Custom exception for compression-related errors."""
    pass


def get_ghostscript_settings(level: int) -> str:
    """
    Map compression level to Ghostscript PDFSETTINGS.
    
    Args:
        level: 1 (none), 2 (standard), 3 (maximum)
        
    Returns:
        str: Ghostscript PDFSETTINGS parameter
    """
    if level == 2:
        return "/ebook"
    elif level == 3:
        return "/screen"
    else:
        return "/prepress"


def compress_pdf(input_path: str, output_path: str, level: int) -> bool:
    """
    Compress a PDF file using Ghostscript.
    
    Args:
        input_path: Path to the source PDF file
        output_path: Path where the compressed PDF will be saved
        level: Compression level (2=standard, 3=maximum)
        
    Returns:
        bool: True if compression was successful, False otherwise
    """
    if level not in [2, 3]:
        return False
    
    pdf_setting = get_ghostscript_settings(level)
    
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={pdf_setting}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    try:
        result = subprocess.run(
            gs_command,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return True
        else:
            return False
            
    except subprocess.TimeoutExpired:
        return False
    except FileNotFoundError:
        return False
    except Exception:
        return False


def apply_compression(input_path: str, level: int) -> bool:
    """
    Compress a PDF file in-place (safely, using a temporary file).
    
    Args:
        input_path: Path to the PDF file to compress
        level: Compression level (2=standard, 3=maximum)
        
    Returns:
        bool: True if successful, False if it failed (original file remains untouched)
    """
    if level == 1:
        return True
    
    # Use a temporary file with .pdf extension in the same directory
    temp_dir = os.path.dirname(input_path)
    temp_filename = f"temp_compressed_{os.getpid()}.pdf"
    temp_output = os.path.join(temp_dir, temp_filename)
    
    try:
        success = compress_pdf(input_path, temp_output, level)
        
        if success:
            # Replace original with compressed version
            os.replace(temp_output, input_path)
            return True
        else:
            # Clean up temp file if it exists
            if os.path.exists(temp_output):
                os.remove(temp_output)
            return False
            
    except Exception:
        # Clean up temp file if it exists
        if os.path.exists(temp_output):
            try:
                os.remove(temp_output)
            except Exception:
                pass
        return False
