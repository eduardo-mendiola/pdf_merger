"""
Main application logic - orchestrates the PDF merger and compressor workflows.
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
from src.compressor import (
    apply_compression,
    compress_pdf_precise,
    generate_compressed_filename,
    get_compression_description
)


# ============================================================================
# MERGE WORKFLOW
# ============================================================================

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
            print_info("Opening file explorer for multiple file selection...")
            print_info("Use Ctrl+click or Shift+click to select multiple files.")
            
            selected_files = select_multiple_pdf_files()
            
            if not selected_files:
                print_warning("No files selected.")
                continue
            
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
            print_info("Opening folder selection dialog...")
            folder_path = select_folder_for_pdfs()
            
            if not folder_path:
                print_warning("No folder selected.")
                continue
            
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
            
            pdf_files.sort(key=lambda x: os.path.basename(x).lower())
            
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
    Ask user for compression level (preset-based, used in merge workflow).
    
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
        files_to_merge = collect_pdf_files()
        
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
        
        print_section("OUTPUT LOCATION")
        print_prompt("Press ENTER to select output folder and filename:")
        input("> ")
        
        output_path = select_output_file()
        
        if not output_path:
            print_warning("No output location selected.")
            print_prompt("Try again? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        output_path = ensure_pdf_extension(output_path)
        print_success(f"Output file: {output_path}")
        
        compression_level = ask_compression_level()
        
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
        
        print()
        print_progress("Merging PDF files...")
        
        try:
            success = merge_pdfs(files_to_merge, output_path)
            
            if not success:
                print_error("Failed to merge PDF files.")
                print_prompt("Try again? (y/n):")
                retry = input("> ").strip().lower()
                return retry == 'y'
            
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
        
        print_prompt("Do you want to merge more PDFs? (y/n):")
        continue_choice = input("> ").strip().lower()
        
        return continue_choice == 'y'
        
    except Exception as e:
        print_error(f"Error during merge session: {e}")
        print_prompt("Try again? (y/n):")
        retry = input("> ").strip().lower()
        return retry == 'y'


# ============================================================================
# COMPRESS-ONLY WORKFLOW
# ============================================================================

def ask_compression_level_precise() -> int:
    """
    Ask user for precise compression level on a 0-100 scale.
    
    Returns:
        int: Compression level from 0 to 100
    """
    print_section("COMPRESSION LEVEL (0-100)")
    print(f"{Colors.DIM}The scale is continuous: every value produces a distinct result.{Colors.RESET}")
    print(f"{Colors.DIM}Higher number = smaller file + lower image quality.{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}Examples:{Colors.RESET}")
    print(f"    {Colors.CYAN}10{Colors.RESET}  -> Very light  (277 DPI, JPEG quality 90)")
    print(f"    {Colors.CYAN}25{Colors.RESET}  -> Light       (243 DPI, JPEG quality 79)")
    print(f"    {Colors.CYAN}50{Colors.RESET}  -> Medium      (186 DPI, JPEG quality 59)")
    print(f"    {Colors.CYAN}75{Colors.RESET}  -> Strong      (129 DPI, JPEG quality 40)")
    print(f"    {Colors.CYAN}100{Colors.RESET} -> Maximum     ( 72 DPI, JPEG quality 20)")
    print()
    print(f"  {Colors.BOLD}0{Colors.RESET}   = no compression (direct copy)")
    print(f"  {Colors.BOLD}100{Colors.RESET} = maximum compression (lowest quality)")
    print()
    print(f"{Colors.YELLOW}Warning: Heavy compression (60+) may degrade scanned text,")
    print(f"since in scanned PDFs the text is actually an image.{Colors.RESET}")
    print()
    
    while True:
        print_prompt("Enter compression level (0-100) [default: 40]:")
        choice = input("> ").strip()
        
        if not choice:
            print_info("Using default: 40")
            return 40
        
        try:
            level = int(choice)
        except ValueError:
            print_error("Invalid input. Please enter a number between 0 and 100.")
            continue
        
        if level < 0 or level > 100:
            print_error("Level must be between 0 and 100.")
            continue
        
        # Confirm if level is high
        if level >= 60:
            print_warning(f"Level {level} ({get_compression_description(level)}) will noticeably reduce quality.")
            print_prompt("Proceed with this level? (y/n):")
            confirm = input("> ").strip().lower()
            if confirm != 'y':
                print_info("Choose a different level.")
                continue
        
        return level


def run_compress_session() -> bool:
    """
    Run a single compress-only session.
    
    Returns:
        bool: True if user wants to continue, False if wants to exit
    """
    try:
        # Step 1: Select a single PDF
        print_section("SELECT PDF TO COMPRESS")
        print_info("Opening file explorer...")
        
        input_path = select_pdf_file()
        
        if not input_path:
            print_warning("No file selected.")
            print_prompt("Try again? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        if not validate_pdf_file(input_path):
            print_error(f"Invalid PDF: {os.path.basename(input_path)}")
            print_prompt("Try again? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        original_size = get_file_size_mb(input_path)
        print_success(f"Selected: {os.path.basename(input_path)} ({original_size:.2f} MB)")
        
        # Step 2: Ask for compression level (0-100)
        compression_level = ask_compression_level_precise()
        
        # Step 3: Build output path
        output_path = generate_compressed_filename(input_path)
        output_name = os.path.basename(output_path)
        
        print()
        print_summary({
            "Input file": os.path.basename(input_path),
            "Input size": f"{original_size:.2f} MB",
            "Output file": output_name,
            "Output folder": os.path.dirname(output_path),
            "Compression level": f"{compression_level} - {get_compression_description(compression_level)}"
        })
        
        print_prompt("Proceed with compression? (y/n):")
        confirm = input("> ").strip().lower()
        
        if confirm != 'y':
            print_info("Operation cancelled by user.")
            print_prompt("Compress another file? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        # Step 4: Compress
        print()
        print_progress("Compressing PDF...")
        
        success = compress_pdf_precise(input_path, output_path, compression_level)
        
        if not success:
            print_error("Compression failed. Original file was not modified.")
            print_prompt("Try again? (y/n):")
            retry = input("> ").strip().lower()
            return retry == 'y'
        
        # Step 5: Show results
        compressed_size = get_file_size_mb(output_path)
        
        if original_size > 0:
            reduction_pct = ((original_size - compressed_size) / original_size) * 100
        else:
            reduction_pct = 0.0
        
        print()
        print_header("SUCCESS")
        print_success(f"File saved to: {output_path}")
        print_success(f"Original size:   {original_size:.2f} MB")
        print_success(f"Compressed size: {compressed_size:.2f} MB")
        
        if reduction_pct > 0:
            print_success(f"Size reduction:  {reduction_pct:.1f}%")
        elif reduction_pct == 0:
            print_warning("File size unchanged (file may already be optimized).")
        else:
            print_warning("File size increased (unusual, compression may not suit this PDF).")
        
        print()
        
        print_prompt("Compress another file? (y/n):")
        continue_choice = input("> ").strip().lower()
        
        return continue_choice == 'y'
        
    except Exception as e:
        print_error(f"Error during compression session: {e}")
        print_prompt("Try again? (y/n):")
        retry = input("> ").strip().lower()
        return retry == 'y'


# ============================================================================
# ENTRY POINT
# ============================================================================

def show_main_menu() -> str:
    """
    Show the main menu and return the user's choice.
    
    Returns:
        str: 'm' for merge, 'c' for compress, 'q' for quit
    """
    print_section("MAIN MENU")
    print(f"  {Colors.BOLD}m){Colors.RESET} Merge multiple PDFs into one")
    print(f"  {Colors.BOLD}c){Colors.RESET} Compress a single PDF (precise scale 0-100)")
    print(f"  {Colors.BOLD}q){Colors.RESET} Quit")
    print()
    
    while True:
        print_prompt("Select option (m/c/q):")
        choice = input("> ").strip().lower()
        
        if choice in ["m", "c", "q"]:
            return choice
        
        print_error("Invalid option. Please enter m, c, or q.")


def main():
    """
    Main application entry point.
    Presents a main menu to choose between merge and compress workflows.
    """
    try:
        print_header("PDF MERGER APP")
        print_info("Merge multiple PDFs or compress a single PDF with precision")
        
        while True:
            choice = show_main_menu()
            
            if choice == 'q':
                print()
                print_info("Thank you for using PDF Merger App!")
                break
            
            elif choice == 'm':
                print()
                print_info("Starting merge workflow...")
                while True:
                    should_continue = run_merge_session()
                    if not should_continue:
                        break
            
            elif choice == 'c':
                print()
                print_info("Starting compress workflow...")
                while True:
                    should_continue = run_compress_session()
                    if not should_continue:
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