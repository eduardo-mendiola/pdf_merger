"""
PDF Merger - A professional CLI application for merging and compressing PDF files.

This package provides the core functionality for merging multiple PDF documents
without quality loss, with optional image compression via Ghostscript.

Modules:
    main: Application orchestrator and user workflow
    merger: PDF merging logic using pypdf
    compressor: PDF compression logic using Ghostscript
    dialogs: Native GNOME dialogs via zenity
    console: Color-coded console output formatting
    utils: Path validation, file handling, and helpers
"""

__version__ = "1.0.0"
__author__ = "Eduardo Mendiola"