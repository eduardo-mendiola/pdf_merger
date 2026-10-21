"""
PDF compression logic using Ghostscript.
Provides reliable, high-quality image downsampling without affecting text/vector graphics.
Includes both preset-based compression (for merging) and precise scale-based compression (0-100).
"""
import os
import subprocess
import shutil
from typing import Optional, List


class CompressionError(Exception):
    """Custom exception for compression-related errors."""
    pass


# ============================================================================
# PRESET-BASED COMPRESSION (used by merge workflow)
# ============================================================================

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
    Compress a PDF file using Ghostscript with preset-based settings.
    
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
    
    temp_dir = os.path.dirname(input_path)
    temp_filename = f"temp_compressed_{os.getpid()}.pdf"
    temp_output = os.path.join(temp_dir, temp_filename)
    
    try:
        success = compress_pdf(input_path, temp_output, level)
        
        if success:
            os.replace(temp_output, input_path)
            return True
        else:
            if os.path.exists(temp_output):
                os.remove(temp_output)
            return False
            
    except Exception:
        if os.path.exists(temp_output):
            try:
                os.remove(temp_output)
            except Exception:
                pass
        return False


# ============================================================================
# PRECISE SCALE-BASED COMPRESSION (0-100, used by standalone compression mode)
# ============================================================================

def get_compression_params(level: int) -> List[str]:
    """
    Build Ghostscript parameters for precise compression level (0-100).
    
    Uses LINEAR INTERPOLATION instead of fixed steps, so every value from
    0 to 100 produces a distinct result:
    
      - DPI range: 300 (level 0) -> 72 (level 100)
      - JPEG quality range: 98 (level 0) -> 20 (level 100)
    
    Args:
        level: Compression intensity from 0 to 100
        
    Returns:
        List[str]: Ghostscript command-line arguments (excluding input/output files)
    """
    if level <= 0:
        return []
    
    level = max(0, min(100, level))
    
    # Linear interpolation: level 0 -> max quality, level 100 -> min quality
    # DPI: 300 -> 72
    dpi = int(round(300 - (300 - 72) * (level / 100.0)))
    # JPEG quality: 98 -> 20
    jpeg_q = int(round(98 - (98 - 20) * (level / 100.0)))
    
    return [
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        # Disable PDFSETTINGS so our manual params take full effect
        "-dPDFSETTINGS=/default",
        # Image downsampling configuration
        "-dDownsampleColorImages=true",
        "-dColorImageDownsampleType=/Bicubic",
        f"-dColorImageResolution={dpi}",
        "-dColorImageDownsampleThreshold=1.0",
        "-dAutoFilterColorImages=false",
        "-dColorImageFilter=/DCTEncode",
        f"-dJPEGQ={jpeg_q}",
        "-dDownsampleGrayImages=true",
        "-dGrayImageDownsampleType=/Bicubic",
        f"-dGrayImageResolution={dpi}",
        "-dGrayImageDownsampleThreshold=1.0",
        "-dDownsampleMonoImages=true",
        "-dMonoImageDownsampleType=/Bicubic",
        f"-dMonoImageResolution={dpi}",
        "-dMonoImageDownsampleThreshold=1.0",
        # Preserve fonts and text rendering
        "-dEmbedAllFonts=true",
        "-dSubsetFonts=true",
        "-dProcessColorModel=/DeviceRGB",
    ]


def compress_pdf_precise(input_path: str, output_path: str, level: int) -> bool:
    """
    Compress a PDF file using precise scale-based parameters (0-100).
    
    Level 0 performs a direct copy (no Ghostscript call).
    Levels 1-100 use Ghostscript with tuned DPI and JPEG quality.
    
    Args:
        input_path: Path to the source PDF file
        output_path: Path where the compressed PDF will be saved
        level: Compression intensity from 0 (none) to 100 (maximum)
        
    Returns:
        bool: True if compression was successful, False otherwise
    """
    level = max(0, min(100, level))
    
    if level == 0:
        try:
            shutil.copy2(input_path, output_path)
            return True
        except Exception:
            return False
    
    params = get_compression_params(level)
    
    gs_command = ["gs"] + params + [
        f"-sOutputFile={output_path}",
        input_path
    ]
    
    try:
        result = subprocess.run(
            gs_command,
            capture_output=True,
            text=True,
            timeout=300
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


def generate_compressed_filename(input_path: str) -> str:
    """
    Generate an output filename for a compressed PDF, appending '_compressed'
    before the extension.
    
    Examples:
        /home/user/doc.pdf         -> /home/user/doc_compressed.pdf
        /home/user/report final.pdf -> /home/user/report final_compressed.pdf
    
    Args:
        input_path: Original PDF file path
        
    Returns:
        str: New file path with '_compressed' suffix
    """
    directory = os.path.dirname(input_path)
    basename = os.path.basename(input_path)
    name, ext = os.path.splitext(basename)
    
    if not ext:
        return os.path.join(directory, f"{name}_compressed.pdf")
    
    return os.path.join(directory, f"{name}_compressed{ext}")


def get_compression_description(level: int) -> str:
    """
    Return a human-readable description of the compression level,
    including the actual DPI and JPEG quality that will be applied.
    
    Args:
        level: Compression intensity from 0 to 100
        
    Returns:
        str: Description string for console display
    """
    level = max(0, min(100, level))
    
    if level == 0:
        return "No compression (direct copy)"
    
    # Calculate the actual values that will be used
    dpi = int(round(300 - (300 - 72) * (level / 100.0)))
    jpeg_q = int(round(98 - (98 - 20) * (level / 100.0)))
    
    if level <= 20:
        intensity = "Very light"
    elif level <= 40:
        intensity = "Light"
    elif level <= 60:
        intensity = "Medium"
    elif level <= 80:
        intensity = "Strong"
    else:
        intensity = "Maximum"
    
    return f"{intensity} ({dpi} DPI, JPEG quality {jpeg_q})"