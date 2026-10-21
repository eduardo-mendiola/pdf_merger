# PDF Merger App

A professional command-line application for Ubuntu that merges multiple PDF files into a single document and compresses individual PDFs with precision. Built with a clean modular architecture and native GNOME integration.

## Features

- **Two main workflows**:
  - **Merge**: Combine multiple PDFs into one document
  - **Compress**: Reduce the size of a single PDF with a precise 0-100 scale
- **Zero quality loss in merge mode**: Page-level copying using `pypdf` ensures no recompression or rendering artifacts
- **Precise compression scale**: Continuous 0-100 scale powered by Ghostscript (industry standard), with linear interpolation of DPI and JPEG quality
- **Flexible file selection**: Three ways to add PDFs for merging
  - Manual selection (one by one)
  - Multiple selection (Ctrl+click or Shift+click in file dialog)
  - Batch loading (load all PDFs from a folder, sorted alphabetically)
- **Native GNOME dialogs**: Beautiful file picker windows via `zenity`
- **Security focused**: All file operations restricted to the user's home directory
- **Smart file handling**: Combined folder + filename selection in a single dialog (like browser downloads)
- **Overwrite protection**: Warns when a file already exists and offers safe alternatives
- **Non-destructive compression**: Compressed files are saved with a `_compressed` suffix, preserving the original
- **Professional console UI**: Color-coded output with clean formatting (no emoji spam)
- **Robust error handling**: Graceful handling of invalid inputs, cancellations, and `Ctrl+C`
- **Multi-session workflow**: Run as many merge or compress sessions as you want without restarting the app
- **Modular architecture**: Clean separation of concerns across dedicated modules

## Requirements

- **Ubuntu Linux** (or any Linux distribution with GNOME desktop)
- **Python 3.8** or higher
- **System packages** (pre-installed on Ubuntu):
  - `zenity` - Native GNOME dialogs
  - `ghostscript` - PDF compression engine

## Installation

### 1. Verify system dependencies

```bash
zenity --version
gs --version
```

If missing, install them:

```bash
sudo apt update
sudo apt install zenity ghostscript -y
```

### 2. Set up the project

```bash
mkdir -p ~/Apps
cd ~/Apps
git clone <repository-url> pdf_merger   # or copy the folder manually
cd pdf_merger
```

### 3. Create and activate the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python dependencies

```bash
pip install pypdf
```

## Quick Start

```bash
cd ~/Apps/pdf_merger
source venv/bin/activate
python pdf_merger.py
```

The application presents a main menu:

1. Choose your workflow:
   - **m)** Merge multiple PDFs into one
   - **c)** Compress a single PDF with a precise 0-100 scale
   - **q)** Quit
2. Follow the guided prompts (file selection, output location, compression options)
3. Review the summary and confirm
4. Repeat as many times as you want, or exit cleanly

## Project Structure

```
pdf_merger/
├── venv/                  # Virtual environment (auto-generated)
├── src/                   # Application source code
│   ├── __init__.py        # Package marker with metadata
│   ├── main.py            # Application orchestrator and user workflow
│   ├── merger.py          # PDF merging logic using pypdf
│   ├── compressor.py      # PDF compression logic using Ghostscript
│   ├── dialogs.py         # Native GNOME dialogs via zenity
│   ├── console.py         # Color-coded console output formatting
│   └── utils.py           # Path validation, file handling, helpers
├── pdf_merger.py          # Executable launcher (entry point)
├── README.md              # This file
├── USAGE.md               # Detailed usage instructions
└── LICENSE                # MIT License
```

## Architecture

The application follows a clean modular design:

| Module | Responsibility |
|--------|----------------|
| `main.py` | Orchestrates the user workflow, presents the main menu, handles input validation and error management |
| `merger.py` | Merges PDF files using `pypdf` without quality loss |
| `compressor.py` | Applies image compression via Ghostscript (preset-based for merge, precise scale for standalone mode) |
| `dialogs.py` | Wraps `zenity` commands for native file/folder selection (single, multiple, folder) |
| `console.py` | Provides styled console output with ANSI colors |
| `utils.py` | Security validations, path helpers, and file utilities |

## Technical Details

### PDF Merging

Uses `pypdf` to copy pages at the structural level. This means:
- No re-rendering of content
- No recompression of images
- 100% preservation of original quality
- Text, vector graphics, and metadata remain intact

### PDF Compression

Uses **Ghostscript** (`gs`), the industry-standard PDF processor, in two modes:

#### Preset-based compression (used in merge workflow)
- Three presets: `/prepress`, `/ebook` (~150 DPI), `/screen` (~72 DPI)
- Only affects raster images; text and vectors remain crisp
- Safe in-place compression using temporary files (original is never lost if compression fails)

#### Precise scale-based compression (used in standalone compress mode)
- Continuous 0-100 scale with **linear interpolation** of parameters
- Every value from 0 to 100 produces a distinct result
- **DPI range**: 300 (level 0) → 72 (level 100)
- **JPEG quality range**: 98 (level 0) → 20 (level 100)
- Formula: `value = max_value - (max_value - min_value) × (level / 100)`
- Non-destructive: the original file is never modified; the compressed version is saved with a `_compressed` suffix
- Displays the actual DPI and JPEG quality that will be applied, so you always know exactly what you're getting

### File Selection Methods

The app provides three ways to load PDFs for merging:

1. **Manual selection (option a)**: Opens file dialog for each file, one at a time. Best when files are in different folders or you want precise control.

2. **Multiple selection (option b)**: Opens a single file dialog where you can select multiple files using Ctrl+click or Shift+click. Best for selecting specific files from the same folder.

3. **Batch loading (option c)**: Opens a folder selection dialog, scans for all PDFs, sorts them alphabetically, and shows a preview list before loading. Best when you want to merge all PDFs in a folder.

### Security Model

- All file paths are validated against the user's home directory
- Symlinks and `..` traversals are resolved before validation
- Files outside the home directory are rejected with a clear warning
- No system directories can be accessed through the application

### Error Handling

- Invalid user inputs are caught and re-prompted with clear messages
- `Ctrl+C` is handled gracefully without stack traces
- Failed compression falls back to the uncompressed version (in merge mode) or reports an error (in compress mode)
- Corrupted PDFs are detected and skipped with warnings

## Troubleshooting

### "zenity: command not found"
```bash
sudo apt install zenity -y
```

### "gs: command not found"
```bash
sudo apt install ghostscript -y
```

### "No module named 'pypdf'"
```bash
source venv/bin/activate
pip install pypdf
```

### File dialog doesn't appear
- Ensure you're running on a graphical desktop (not SSH)
- Verify zenity is installed: `zenity --version`

### Compression doesn't reduce file size
- The PDF may contain vector graphics or text (not affected by compression)
- Images may already be compressed at a lower quality than the target
- Try a higher level (e.g., 80 or 100) for more aggressive compression

### Batch loading doesn't find files
- Ensure the folder contains `.pdf` files (case-insensitive)
- Check that files are not in subfolders (only scans the selected folder)
- Verify you have read permissions for the folder

### Compressed file is larger than the original
- Some PDFs are already optimized or contain content that doesn't compress well
- Try a lower compression level (e.g., 20 or 30)
- The original file is preserved, so no data is lost

## License

This project is licensed under the **MIT License**. 
In short: you are free to use, copy, modify, merge, publish, distribute, and sell copies of the software, for both personal and commercial purposes. 
See the [LICENSE](LICENSE) file for the full legal text.

## Author

Eduardo Mendiola
