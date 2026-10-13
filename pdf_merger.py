"""
PDF Merger App - Main launcher script.
This is the entry point for the application.
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.main import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print("❌ Error: Could not import application modules.")
    print(f"   Details: {e}")
    print("\nPlease ensure:")
    print("  1. You are running this script from the project root directory")
    print("  2. The 'src' folder exists with all required modules")
    print("  3. All dependencies are installed (pypdf, pikepdf)")
    sys.exit(1)
except Exception as e:
    print(f"❌ Fatal error: {e}")
    sys.exit(1)
