# PDF Merger - Usage Instructions

## Quick Start

```bash
cd ~/Apps/pdf_merger
source venv/bin/activate
python pdf_merger.py
```

## Complete Workflow Guide

### Starting the Application

When you run the application, you'll see:

```
============================================================
                       PDF MERGER APP                       
============================================================

ℹ Merge multiple PDFs or compress a single PDF with precision
```

The application presents a main menu:

```
--- MAIN MENU ---

  m) Merge multiple PDFs into one
  c) Compress a single PDF (precise scale 0-100)
  q) Quit

Select option (m/c/q):
> 
```

- Type `m` to start the merge workflow
- Type `c` to start the compress-only workflow
- Type `q` to exit the application

---

## Merge Workflow

### Step 1: Select PDF Files

After choosing `m` from the main menu, the application will present a menu with multiple loading options:

```
--- FILE LOADING ---

  a) Select PDF files manually (one by one)
  b) Select multiple PDF files (Ctrl+click)
  c) Load ALL PDFs from a folder (alphabetical order)
  q) Finish loading

Select option (a/b/c/q):
> 
```

#### Option A: Manual Selection (One by One)

**What to do:**
- Type `a` and press ENTER
- A native GNOME file picker window will open
- Navigate to your PDF file (only files within your home directory are accessible)
- Select the PDF and click "Open"
- The terminal will confirm: `+ filename.pdf`

**Adding more files:**

```
Add another PDF? (y/n):
> 
```

- Type `y` and press ENTER to add another PDF
- Type `n` and press ENTER to finish selecting files

#### Option B: Multiple Selection (Ctrl+click)

**What to do:**
- Type `b` and press ENTER
- A file picker window will open with instructions
- Use **Ctrl+click** to select individual files
- Use **Shift+click** to select a range of files
- Click "Open" to confirm all selected files

The app will validate each file and show:
```
+ file1.pdf
+ file2.pdf
+ file3.pdf
✓ Added 3 file(s).
```

**Note:** Invalid or corrupted PDFs will be skipped with a warning.

#### Option C: Batch Loading from Folder

**What to do:**
- Type `c` and press ENTER
- A folder selection dialog will open
- Navigate to and select the folder containing your PDFs
- The app will scan the folder and display all found PDFs:

```
→ Scanning folder: /home/user/Documents/PDFs

ℹ Found 19 PDF file(s) in folder:
------------------------------------------------------------
   1. document_001.pdf
   2. document_002.pdf
   3. document_003.pdf
   ...
  19. document_019.pdf
------------------------------------------------------------

Load all these files? (y/n):
> 
```

- Type `y` to load all files in alphabetical order
- Type `n` to cancel and return to the menu

**Important:** Files are loaded in alphabetical order (case-insensitive). Plan your filenames accordingly if order matters.

#### Finishing File Selection

When you have at least 2 files, type `q` to finish loading and proceed to the next step.

**Minimum requirement:** You must select at least 2 PDF files.

**Exiting early:**
- Type `q` at the menu to exit file selection
- If you have fewer than 2 files, you'll be asked to confirm exit
- If you have 2+ files, typing `q` will proceed to the next step

### Step 2: Choose Output Location

After selecting your files, you'll see:

```
✓ Total files: 2
✓ Total pages: 7

--- OUTPUT LOCATION ---

Press ENTER to select output folder and filename:
> 
```

**What to do:**
- Press **ENTER** to open the save dialog
- A file picker window will open in your Downloads folder
- The filename field will show: `MERGED_PDF_FINAL.pdf`
- You can:
  - Navigate to a different folder using the sidebar or path bar
  - Change the filename by editing the text field
  - The dialog will warn you if the file already exists
- Click "Save" to confirm

**Default behavior:**
- If you cancel the dialog, you'll be asked to try again
- The file will be saved with a `.pdf` extension (added automatically if missing)

### Step 3: Select Compression Level

```
--- COMPRESSION OPTIONS ---

  1. No compression (original quality)
  2. Standard (~150 DPI, good balance)
  3. Maximum (~72 DPI, smallest size)

Note: Compression only affects images. Text remains clear.

Select option (1-3) [default: 1]:
> 
```

**Options explained:**

**Option 1 - No compression (default):**
- Preserves 100% original quality
- File size = sum of all input files
- Best for: Documents with text, vector graphics, or when quality is critical

**Option 2 - Standard compression:**
- Reduces image resolution to ~150 DPI
- Good balance between quality and size
- Typical reduction: 30-50% smaller file size
- Best for: Documents with photos that will be viewed on screen or printed at normal size

**Option 3 - Maximum compression:**
- Reduces image resolution to ~72 DPI
- Smallest file size
- Typical reduction: 60-80% smaller file size
- Best for: Email attachments, web uploads, or when file size is critical
- Note: Images may appear pixelated when zoomed in

**What to do:**
- Type `1`, `2`, or `3` and press ENTER
- Press ENTER without typing anything to use the default (Option 1)
- If you choose 2 or 3, you'll be asked to confirm:

```
⚠ Compression will reduce image quality.
Proceed with compression? (y/n):
> 
```

- Type `y` to proceed with compression
- Type `n` to cancel and use no compression instead

### Step 4: Review and Confirm

Before processing, you'll see a summary:

```
Summary:
----------------------------------------
  Files to merge: 2
  Output file: MERGED_PDF_FINAL.pdf
  Output folder: /home/user/Downloads
  Compression: Standard
----------------------------------------

Proceed with merge? (y/n):
> 
```

**What to do:**
- Review the summary to ensure everything is correct
- Type `y` and press ENTER to start merging
- Type `n` and press ENTER to cancel and start over

### Step 5: Processing

The application will show progress:

```
→ Merging PDF files...

Processing 2 files...
  ✅ Added: /home/user/Documents/file1.pdf (3 pages)
  ✅ Added: /home/user/Documents/file2.pdf (4 pages)

📦 Applying compression (level 2)...
✓ Standard compression applied (~150 DPI)

============================================================
                          SUCCESS                           
============================================================

✓ File saved to: /home/user/Downloads/MERGED_PDF_FINAL.pdf
✓ File size: 2.34 MB
```

### Step 6: Continue or Exit

After a successful merge:

```
Do you want to merge more PDFs? (y/n):
> 
```

- Type `y` to start a new merge session (go back to Step 1)
- Type `n` to return to the main menu

---

## Compress Workflow

### Step 1: Select PDF to Compress

After choosing `c` from the main menu:

```
--- SELECT PDF TO COMPRESS ---
ℹ Opening file explorer...
```

**What to do:**
- A file picker window will open
- Navigate to and select the PDF file you want to compress
- The terminal will confirm:

```
✓ Selected: large_document.pdf (27.45 MB)
```

### Step 2: Choose Compression Level (0-100)

The application will display the precise compression scale:

```
--- COMPRESSION LEVEL (0-100) ---
The scale is continuous: every value produces a distinct result.
Higher number = smaller file + lower image quality.

  Examples:
    10  -> Very light  (277 DPI, JPEG quality 90)
    25  -> Light       (243 DPI, JPEG quality 79)
    50  -> Medium      (186 DPI, JPEG quality 59)
    75  -> Strong      (129 DPI, JPEG quality 40)
    100 -> Maximum     ( 72 DPI, JPEG quality 20)

  0   = no compression (direct copy)
  100 = maximum compression (lowest quality)

Warning: Heavy compression (60+) may degrade scanned text,
since in scanned PDFs the text is actually an image.

Enter compression level (0-100) [default: 40]:
> 
```

**Understanding the scale:**

The compression uses **linear interpolation** between two endpoints:
- **DPI range**: 300 (level 0) → 72 (level 100)
- **JPEG quality range**: 98 (level 0) → 20 (level 100)

Every value from 0 to 100 produces a distinct result. For example:
- Level 45 → 197 DPI, JPEG quality 63
- Level 50 → 186 DPI, JPEG quality 59
- Level 60 → 163 DPI, JPEG quality 51

**What to do:**
- Enter a number from 0 to 100
- Press ENTER without typing to use the default (40)
- If you enter 60 or higher, you'll be asked to confirm:

```
⚠ Level 75 (Strong - 129 DPI, JPEG quality 40) will noticeably reduce quality.
Proceed with this level? (y/n):
> 
```

- Type `y` to proceed
- Type `n` to choose a different level

### Step 3: Review and Confirm

Before processing, you'll see a summary:

```
Summary:
----------------------------------------
  Input file:        large_document.pdf
  Input size:        27.45 MB
  Output file:       large_document_compressed.pdf
  Output folder:     /home/user/Documents
  Compression level: 50 - Medium (186 DPI, JPEG quality 59)
----------------------------------------

Proceed with compression? (y/n):
> 
```

**What to do:**
- Review the summary to ensure everything is correct
- Type `y` and press ENTER to start compression
- Type `n` to cancel

**Important:** The compressed file will be saved in the same folder as the original, with a `_compressed` suffix added to the filename. The original file is never modified.

### Step 4: Processing

The application will compress the file:

```
→ Compressing PDF...
```

### Step 5: Results

After successful compression, you'll see:

```
============================================================
                          SUCCESS                           
============================================================

✓ File saved to: /home/user/Documents/large_document_compressed.pdf
✓ Original size:   27.45 MB
✓ Compressed size: 12.34 MB
✓ Size reduction:  55.0%
```

The application shows:
- The path where the compressed file was saved
- The original file size
- The compressed file size
- The percentage of size reduction

### Step 6: Continue or Exit

```
Compress another file? (y/n):
> 
```

- Type `y` to compress another file (go back to Step 1)
- Type `n` to return to the main menu

---

## Common Scenarios

### Scenario 1: Simple Merge (No Compression)

You have 2 PDFs and want to combine them without changing quality:

1. Type `m` → Start merge workflow
2. Type `a` → Select first PDF manually
3. Type `y` → Select second PDF manually
4. Type `n` → Finish selecting
5. Press ENTER → Choose output location
6. Press ENTER → Use default compression (Option 1)
7. Type `y` → Confirm merge
8. Type `n` → Return to main menu

### Scenario 2: Merge Multiple Files from Same Folder

You have 19 PDFs in a folder and want to merge them all:

1. Type `m` → Start merge workflow
2. Type `c` → Select the folder containing the PDFs
3. Review the list of files shown
4. Type `y` → Confirm loading all files
5. Press ENTER → Choose output location
6. Type `2` → Select standard compression (optional)
7. Type `y` → Confirm compression
8. Type `y` → Confirm merge
9. Type `n` → Return to main menu

### Scenario 3: Select Specific Files with Multiple Selection

You have 10 PDFs in a folder but only want to merge 5 specific ones:

1. Type `m` → Start merge workflow
2. Type `b` → Open multiple file selection dialog
3. Use Ctrl+click to select the 5 files you want
4. Click "Open" → Files are loaded
5. Press ENTER → Choose output location
6. Press ENTER → Use default compression
7. Type `y` → Confirm merge
8. Type `n` → Return to main menu

### Scenario 4: Compress a Large PDF

You have a 27 MB PDF with images and want to reduce its size:

1. Type `c` → Start compress workflow
2. Select the PDF file
3. Type `50` → Choose medium compression
4. Type `y` → Confirm the level
5. Type `y` → Confirm compression
6. Check the results (should be ~12 MB, 55% reduction)
7. Type `n` → Return to main menu

### Scenario 5: Compress with Maximum Reduction

You need to email a PDF but it's too large:

1. Type `c` → Start compress workflow
2. Select the PDF file
3. Type `80` → Choose strong compression
4. Type `y` → Confirm the level
5. Type `y` → Confirm compression
6. Check the results (should be significantly smaller)
7. Type `n` → Return to main menu

### Scenario 6: Cancel and Restart

You selected files but want to start over:

1. At the confirmation prompt, type `n`
2. You'll be asked: "Start a new merge session? (y/n):"
3. Type `y` to start over from file selection

### Scenario 7: Exit Without Doing Anything

You opened the app but changed your mind:

1. At the main menu, type `q`
2. Application exits cleanly

---

## Keyboard Shortcuts

### In File Dialogs (Zenity)

- `Ctrl + L`: Type a path manually
- `Alt + Up`: Go to parent folder
- `Alt + Home`: Go to home folder
- `Ctrl + H`: Show/hide hidden files (disabled in this app for security)
- `Ctrl + click`: Select multiple files (in multiple selection mode)
- `Shift + click`: Select range of files (in multiple selection mode)
- `Esc`: Cancel and close dialog

### In Terminal

- `Ctrl + C`: Cancel current operation and exit application
- `Ctrl + D`: Send EOF (same as typing `q` in most prompts)

---

## Tips and Best Practices

### File Organization

- Keep your PDFs organized in folders within your home directory
- Use descriptive filenames before merging
- The merged PDF will be saved with the name you specify (default: `MERGED_PDF_FINAL.pdf`)
- For batch loading, name files with numbers (001, 002, 003) to ensure correct order
- Compressed files are automatically saved with `_compressed` suffix in the same folder

### Choosing the Right Loading Method

**Use Option A (Manual) when:**
- Files are in different folders
- You want to add files from multiple locations
- You need precise control over the order
- You're merging just 2-3 files

**Use Option B (Multiple) when:**
- Files are in the same folder
- You want to select specific files (not all)
- You're merging 5-10 files
- You want to see the files before selecting

**Use Option C (Batch) when:**
- You want to merge ALL PDFs in a folder
- You have many files (10+)
- Files are already named in the correct order
- You want the fastest workflow

### Compression Guidelines

#### For Merge Workflow (Preset-based)

**When to use no compression (Option 1):**
- Documents with text only
- Legal documents requiring original quality
- Files that will be printed at high quality
- When you're unsure about compression

**When to use standard compression (Option 2):**
- Documents with photos for screen viewing
- Reports with images that don't need zoom
- General purpose PDFs
- Good default for most use cases

**When to use maximum compression (Option 3):**
- Email attachments with size limits
- Web uploads
- Archive storage
- Documents where text is more important than image quality

#### For Compress Workflow (Precise scale 0-100)

**Level 0-20 (Very light):**
- Minimal size reduction
- Maximum quality preservation
- Best for: High-quality prints, important documents

**Level 21-40 (Light):**
- Moderate size reduction
- Good quality preservation
- Best for: General documents with images

**Level 41-60 (Medium):**
- Good balance of size and quality
- Best for: Most use cases, screen viewing

**Level 61-80 (Strong):**
- Significant size reduction
- Noticeable quality reduction
- Best for: Email attachments, web uploads

**Level 81-100 (Maximum):**
- Maximum size reduction
- Significant quality reduction
- Best for: When size is critical, archival copies

**Warning:** For scanned PDFs (where text is actually an image), compression levels above 60 may make text difficult to read.

### File Size Expectations

**Merge workflow (preset-based):**

Without compression:
- Final size ≈ Sum of all input file sizes
- Example: 3 files of 2MB each = ~6MB merged file

With standard compression (Option 2):
- Typical reduction: 30-50%
- Example: 6MB merged file → ~3-4MB

With maximum compression (Option 3):
- Typical reduction: 60-80%
- Example: 6MB merged file → ~1-2MB

**Compress workflow (precise scale):**

The actual reduction depends on:
- The compression level chosen
- Number and size of images in the PDF
- Original image quality and resolution
- Content type (text-heavy PDFs compress less)

Typical reductions:
- Level 40: 20-40% reduction
- Level 60: 40-60% reduction
- Level 80: 60-80% reduction

### Order Matters

**Manual and Multiple selection (Options A & B):**
- PDFs are merged in the exact order you select them
- First file selected = First pages in merged PDF
- Second file selected = Next pages
- And so on...

**Batch loading (Option C):**
- Files are sorted alphabetically (case-insensitive)
- Example: `001_intro.pdf`, `002_chapter1.pdf`, `003_chapter2.pdf`
- Plan your filenames accordingly

**Tip:** For batch loading, use numbered prefixes to ensure correct order.

---

## Troubleshooting

### "Invalid option. Please enter m, c, or q."

**Cause:** You typed something other than m, c, or q in the main menu

**Solution:** 
- Type `m`, `c`, or `q` and press ENTER
- These are the only valid options in the main menu

### "Invalid option. Please enter a, b, c, or q."

**Cause:** You typed something other than a, b, c, or q in the file loading menu

**Solution:** 
- Type `a`, `b`, `c`, or `q` and press ENTER
- These are the only valid options in the file loading menu

### "You need to select at least 2 PDF files."

**Cause:** You tried to proceed with fewer than 2 files

**Solution:**
- Continue selecting files until you have at least 2
- Or type `q` to exit and start a new session

### "Invalid PDF: filename.pdf"

**Cause:** The selected file is not a valid PDF or is corrupted

**Solution:**
- Verify the file is actually a PDF (check the extension)
- Try opening the file in a PDF viewer to confirm it's not corrupted
- Select a different file

### "No file selected."

**Cause:** You closed the file dialog without selecting a file

**Solution:**
- If you have files already selected, choose whether to continue or finish
- If no files selected, the dialog will reopen

### "No folder selected."

**Cause:** You cancelled the folder selection dialog (option c)

**Solution:**
- You'll return to the menu
- Try option `c` again or choose a different option

### "No PDF files found in the selected folder."

**Cause:** The selected folder doesn't contain any `.pdf` files

**Solution:**
- Verify the folder contains PDF files
- Check that files have `.pdf` extension (case-insensitive)
- Files in subfolders are not scanned (only the selected folder)
- Choose a different folder or use option `a` or `b`

### "No output location selected."

**Cause:** You cancelled the save dialog

**Solution:**
- You'll be asked to try again
- Press ENTER to reopen the dialog and select a location

### "Invalid input. Please enter a number between 0 and 100."

**Cause:** You entered text or a number outside the 0-100 range in the compression level prompt

**Solution:**
- Enter a number from 0 to 100
- Press ENTER without typing to use the default (40)

### "Compression failed. Saved uncompressed version."

**Cause:** Ghostscript encountered an error during compression (in merge workflow)

**Solution:**
- The merged PDF was still saved successfully (without compression)
- Check if Ghostscript is installed: `gs --version`
- Try a different compression level
- The file may contain elements that cannot be compressed

### "Compression failed. Original file was not modified."

**Cause:** Ghostscript encountered an error during compression (in compress workflow)

**Solution:**
- The original file is preserved (never modified)
- Check if Ghostscript is installed: `gs --version`
- Try a different compression level
- The file may contain elements that cannot be compressed

### "File size unchanged" or "File size increased"

**Cause:** The compressed file is the same size or larger than the original

**Solution:**
- Some PDFs are already optimized or contain content that doesn't compress well
- Try a different compression level
- The original file is preserved, so no data is lost

### "Operation cancelled by user (Ctrl+C)"

**Cause:** You pressed Ctrl+C to exit

**Solution:**
- This is normal behavior
- The application exits cleanly
- No files are lost or corrupted

### Application doesn't respond

**Cause:** Large files or system resources

**Solution:**
- Wait a moment (large files take time to process)
- If it hangs for more than 2 minutes, press Ctrl+C to cancel
- Try with smaller files or fewer files at once

---

## Advanced Usage

### Multiple Sessions

You can run multiple merge or compress sessions without restarting:

1. Complete a merge or compress session
2. At the prompt, type `y` to continue or `n` to return to main menu
3. From the main menu, choose a different workflow or exit

### Custom Filenames (Merge Workflow)

When saving a merged PDF, you can specify any valid filename:

- `report_final.pdf`
- `merged_document_2024.pdf`
- `combined-files.pdf`

**Rules:**
- Must end with `.pdf` (added automatically if missing)
- Cannot contain: `/ \ : * ? " < > |`
- Maximum 255 characters

### Handling Existing Files

If the output file already exists, Zenity will warn you:

- Click "Replace" to overwrite the existing file
- Or change the filename in the text field to save with a different name

### Mixing Selection Methods

You can combine different loading methods in the same merge session:

1. Type `c` → Load 10 files from a folder
2. Type `y` → Confirm loading
3. Type `a` → Add 1 more file manually from another folder
4. Type `n` → Finish selecting

The files will be merged in the order they were added.

### Compressed File Naming

In the compress workflow, the output file is automatically named:
- Original: `document.pdf`
- Compressed: `document_compressed.pdf`

The compressed file is saved in the same folder as the original.

---

## Performance Notes

**Processing speed depends on:**
- Number of files
- Total page count
- File sizes
- Compression level chosen
- System resources (CPU, RAM, disk speed)

**Typical processing times:**

Merge workflow:
- Small files (< 1MB each): 1-3 seconds
- Medium files (1-10MB each): 3-10 seconds
- Large files (> 10MB each): 10-30 seconds
- Compression adds 2-5 seconds per file

Compress workflow:
- Small files (< 5MB): 2-5 seconds
- Medium files (5-20MB): 5-15 seconds
- Large files (> 20MB): 15-45 seconds

**Batch loading performance:**
- Scanning a folder with 100+ files: < 1 second
- Validation of 50 files: 2-5 seconds
- Total time is dominated by the merge and compression steps

---

## Security Reminders

- You can only select files from your home directory (`/home/username`)
- System directories (`/etc`, `/usr`, etc.) are not accessible
- Hidden files and folders are not shown in dialogs
- All file paths are validated before processing
- Batch loading only scans the selected folder (not subfolders)
- In compress workflow, the original file is never modified

---

## Support

For technical issues or questions:
- Check the [README.md](README.md) for installation and architecture details
- Review this USAGE.md for workflow guidance
- Ensure all dependencies are installed and up to date
