"""
Main application logic - orchestrates the PDF merger workflow.
Handles user interaction, validation, and error management.
"""
import sys
import os
from typing import List, Optional

from src.console import (
    print_header,
    print_section,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_prompt,
    print_summary,
    print_file_added,
    print_progress,
    Colors
)
from src.utils import (
    get_file_size_mb,
    ensure_pdf_extension
)
from src.dialogs import (
    select_pdf_file,
    select_multiple_pdf_files,
    select_folder_for_pdfs,
    select_output_file
)
from src.merger import merge_pdfs, MergerError, get_total_pages, validate_pdf_file
from src.compressor import apply_compression


def collect_pdf_files() -> List[str]:
    """
    Collect PDF files from user with multiple selection methods.
    
    Returns:
        List[str]: List of valid PDF file paths
    """
    files = []
    
    while True:
        print_section("FILE LOADING")
        print(f"  {Colors.BOLD}a){Colors.RESET} Select PDF files manually (one by one)")
        print(f"  {Colors.BOLD}b){Colors.RESET} Select multiple PDF files (Ctrl+click)")
        print(f"  {Colors.BOLD}c){Colors.RESET} Load ALL PDFs from a folder (alphabetical order)")
        print(f"  {Colors.BOLD}q){Colors.RESET} Finish loading")
        print()
        print_prompt("Select option (a/b/c/q):")
        
        choice = input("> ").strip().lower()
        
        if choice == 'q':
            if len(files) >= 2:
                break
            elif len(files) == 1:
                print_warning("You have selected 1 file, but need at least 2.")
                print_prompt("Exit anyway? (y/n):")
                confirm = input("> ").strip().lower()
                if confirm == 'y':
                    print_info("Exiting file selection.")
                    return []
                continue
            else:
                print_prompt("Exit without selecting any files? (y/n):")
                confirm = input("> ").strip().lower()
                if confirm == 'y':
                    print_info("Exiting file selection.")
                    return []
                continue
        
        elif choice == 'a':
            # Manual selection (one by one)
            print_info("Opening file explorer for single file selection...")
            file_path = select_pdf_file()
            
            if not file_path:
                print_warning("No file selected.")
                continue
            
            if not validate_pdf_file(file_path):
                print_error(f"Invalid PDF: {os.path.basename(file_path)}")
                continue
            
            files.append(file_path)
            print_file_added(os.path.basename(file_path))
            
            print_prompt("Add another PDF? (y/n):")
            another = input("> ").strip().lower()
            if another != 'y':
                if len(files) < 2:
                    print_warning("You need at least 2 files. Continue selecting or choose another option.")
                else:
                    break
        
        elif choice == 'b':
            # Multiple selection
            print_info("Opening file explorer for multiple file selection...")
            print_info("Use Ctrl+click or Shift+click to select multiple files.")
            
            selected_files = select_multiple_pdf_files()
            
            if not selected_files:
                print_warning("No files selected.")
                continue
            
            # Validate and add all selected files
            valid_count = 0
            for file_path in selected_files:
                if validate_pdf_file(file_path):
                    files.append(file_path)
                    print_file_added(os.path.basename(file_path))
                    valid_count += 1
                else:
                    print_error(f"Invalid PDF (skipped): {os.path.basename(file_path)}")
            
            print_success(f"Added {valid_count} file(s).")
            
            if len(files) < 2:
                print_warning("You need at least 2 files. Continue selecting or choose another option.")
            else:
                break
        
        elif choice == 'c':
            # Load all PDFs from a folder
            print_info("Opening folder selection dialog...")
            folder_path = select_folder_for_pdfs()
            
            if not folder_path:
                print_warning("No folder selected.")
                continue
            
            # Scan folder for PDF files
            print_progress(f"Scanning folder: {folder_path}")
            
            pdf_files = []
            try:
                for filename in os.listdir(folder_path):
                    if filename.lower().endswith('.pdf'):
                        full_path = os.path.join(folder_path, filename)
                        if os.path.isfile(full_path):
                            pdf_files.append(full_path)
            except Exception as e:
                print_error(f"Error reading folder: {e}")
                continue
            
            if not pdf_files:
                print_warning("No PDF files found in the selected folder.")
                continue
            
            # Sort alphabetically
            pdf_files.sort(key=lambda x: os.path.basename(x).lower())
            
            # Show list of files to be loaded
            print()
            print_info(f"Found {len(pdf_files)} PDF file(s) in folder:")
            print(f"{Colors.DIM}{'-' * 60}{Colors.RESET}")
            for i, file_path in enumerate(pdf_files, 1):
                print(f"  {Colors.CYAN}{i:2d}.{Colors.RESET} {os.path.basename(file_path)}")
            print(f"{Colors.DIM}{'-' * 60}{Colors.RESET}")
            print()
            
            print_prompt("Load all these files? (y/n):")
            confirm = input("> ").strip().lower()
            
            if confirm == 'y':
                # Validate and add all files
                valid_count = 0
                for file_path in pdf_files:
                    if validate_pdf_file(file_path):
                        files.append(file_path)
                        print_file_added(os.path.basename(file_path))
                        valid_count += 1
                    else:
                        print_error(f"Invalid PDF (skipped): {os.path.basename(file_path)}")
                
                print_success(f"Loaded {valid_count} file(s).")
                break
            else:
                print_info("Folder loading cancelled.")
                continue
        
        else:
            print_error("Invalid option. Please enter a, b, c, or q.")
            continue
    
    return files


def ask_compression_level() -> int:
    """
    Ask user for compression level with validation.
    
    Returns:
        int: 1 (no compression), 2 (standard), or 3 (maximum)
    """
    print_section("COMPRESSION OPTIONS")
    print(f"  {Colors.BOLD}1.{Colors.RESET} No compression (original quality)")
    print(f"  {Colors.BOLD}2.{Colors.RESET} Standard (~150 DPI, good balance)")
    print(f"  {Colors.BOLD}3.{Colors.RESET} Maximum (~72 DPI, smallest size)")
    print()
    print(f"{Colors.DIM}Note: Compression only affects images. Text remains clear.{Colors.RESET}")
    print()
    
    while True:
        print_prompt("Select option (1-3) [default: 1]:")
        choice = input("> ").strip()
        
        if not choice:
            print_info("Using default: No compression")
            return 1
        
        if choice in ["1", "2", "3"]:
            level = int(choice)
            if level in [2, 3]:
                print_warning("Compression will reduce image quality.")
                print_prompt("Proceed with compression? (y/n):")
                confirm = input("> ").strip().lower()
                if confirm != 'y':
                    print_info("Using no compression instead.")
                    return 1
            return level
        else:
            print_error("Invalid option. Please enter 1, 2, or 3.")


def run_merge_session() -> bool:
    """
    Run a single merge session.
    
    Returns:
        bool: True if user wants to continue, False if wants to exit
    """
    try:
        # Step 1: Collect PDF files
        files_to_merge = collect_pdf_files()
        
        # Check if user cancelled file selection
        if not files_to_merge:
            print_info("File selection cancelled.")
            print_prompt("Do you want to start a new merge session? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        if len(files_to_merge) < 2:
            print_error("You need to select at least 2 PDF files to merge.")
            print_prompt("Try again? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        print()
        print_success(f"Total files: {len(files_to_merge)}")
        print_success(f"Total pages: {get_total_pages(files_to_merge)}")
        
        # Step 2: Select output file
        print_section("OUTPUT LOCATION")
        print_prompt("Press ENTER to select output folder and filename:")
        input("> ")
        
        output_path = select_output_file()
        
        if not output_path:
            print_warning("No output location selected.")
            print_prompt("Try again? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        # Ensure .pdf extension
        output_path = ensure_pdf_extension(output_path)
        
        print_success(f"Output file: {output_path}")
        
        # Step 3: Ask for compression
        compression_level = ask_compression_level()
        
        # Step 4: Confirm before processing
        compression_text = "None" if compression_level == 1 else "Standard" if compression_level == 2 else "Maximum"
        
        print_summary({
            "Files to merge": len(files_to_merge),
            "Output file": os.path.basename(output_path),
            "Output folder": os.path.dirname(output_path),
            "Compression": compression_text
        })
        
        print_prompt("Proceed with merge? (y/n):")
        confirm = input("> ").strip().lower()
        
        if confirm != 'y':
            print_info("Operation cancelled by user.")
            print_prompt("Start a new merge session? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        # Step 5: Merge PDFs
        print()
        print_progress("Merging PDF files...")
        
        try:
            success = merge_pdfs(files_to_merge, output_path)
            
            if not success:
                print_error("Failed to merge PDF files.")
                print_prompt("Try again? (y/n):")
                retry = input("> ").strip().lower()
                return retry == 'y'
            
            # Step 6: Apply compression if requested
            if compression_level > 1:
                print_progress(f"Applying compression (level {compression_level})...")
                compression_success = apply_compression(output_path, compression_level)
                
                if compression_success:
                    if compression_level == 2:
                        print_success("Standard compression applied (~150 DPI)")
                    else:
                        print_success("Maximum compression applied (~72 DPI)")
                else:
                    print_warning("Compression failed. Saved uncompressed version.")
            
            # Step 7: Show success message
            file_size = get_file_size_mb(output_path)
            
            print()
            print_header("SUCCESS")
            print_success(f"File saved to: {output_path}")
            print_success(f"File size: {file_size:.2f} MB")
            print()
            
        except MergerError as e:
            print_error(str(e))
            print_prompt("Try again? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        # Ask if user wants to merge more PDFs
        print_prompt("Do you want to merge more PDFs? (y/n):")
        continue_choice = input("> ").strip().lower()
        
        return continue_choice == 'y'
        
    except Exception as e:
        print_error(f"Error during merge session: {e}")
        print_prompt("Try again? (y/n):")
        retry = input("> ").strip().lower()
        return retry == 'y'


def main():
    """
    Main application entry point.
    Orchestrates the complete PDF merger workflow with loop support.
    """
    try:
        print_header("PDF MERGER APP")
        print_info("Merge multiple PDFs without quality loss")
        
        # Loop to allow multiple merge sessions
        while True:
            should_continue = run_merge_session()
            
            if not should_continue:
                print()
                print_info("Thank you for using PDF Merger App!")
                break
        
    except KeyboardInterrupt:
        print()
        print()
        print_warning("Operation cancelled by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print()
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()