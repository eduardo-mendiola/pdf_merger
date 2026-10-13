"""
PDF merging logic using pypdf.
Merges multiple PDF files into a single document without quality loss.
"""
from typing import List
from pypdf import PdfWriter, PdfReader


class MergerError(Exception):
    """Custom exception for merger-related errors."""
    pass


def merge_pdfs(file_list: List[str], output_path: str) -> bool:
    """
    Merge a list of PDF files into a single output file.
    Uses page-level copying, so there's NO quality loss or recompression.
    
    Args:
        file_list: List of PDF file paths to merge (in order)
        output_path: Path where the merged PDF will be saved
        
    Returns:
        bool: True if merge was successful, False otherwise
        
    Raises:
        MergerError: If there are no files to merge or a critical error occurs
    """
    if not file_list:
        raise MergerError("No files provided for merging")
    
    if len(file_list) < 2:
        raise MergerError("At least 2 files are required for merging")
    
    print(f"\nProcessing {len(file_list)} files...")
    
    try:
        writer = PdfWriter()
        
        # Append each PDF file to the writer
        for pdf_file in file_list:
            try:
                # Verify file exists and is readable
                reader = PdfReader(pdf_file)
                
                # Check if PDF is valid
                if len(reader.pages) == 0:
                    print(f"⚠️  Warning: {pdf_file} has no pages, skipping...")
                    continue
                
                writer.append(pdf_file)
                print(f"  ✅ Added: {pdf_file} ({len(reader.pages)} pages)")
                
            except Exception as e:
                print(f"⚠️  Error reading {pdf_file}: {e}")
                continue
        
        # Check if we have at least some pages to merge
        if len(writer.pages) == 0:
            raise MergerError("No valid pages found in the provided PDFs")
        
        # Write the merged PDF to the output path
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)
        
        writer.close()
        
        print(f"\n📄 No compression applied (original quality)")
        print(f"✅ Success! Merged file saved to: {output_path}")
        
        return True
        
    except IOError as e:
        raise MergerError(f"Failed to write output file: {e}")
    except Exception as e:
        raise MergerError(f"Unexpected error during merge: {e}")


def get_total_pages(file_list: List[str]) -> int:
    """
    Count total pages across all PDF files.
    
    Args:
        file_list: List of PDF file paths
        
    Returns:
        int: Total number of pages
    """
    total = 0
    
    for pdf_file in file_list:
        try:
            reader = PdfReader(pdf_file)
            total += len(reader.pages)
        except Exception:
            continue
    
    return total


def validate_pdf_file(filepath: str) -> bool:
    """
    Validate that a file is a readable PDF.
    
    Args:
        filepath: Path to the PDF file
        
    Returns:
        bool: True if file is a valid PDF, False otherwise
    """
    try:
        reader = PdfReader(filepath)
        # Try to access pages to verify it's valid
        _ = len(reader.pages)
        return True
    except Exception:
        return False
