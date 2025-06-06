import os
from pathlib import Path
from typing import List, Set, Tuple

# Configuration
ROOT_DIR = "/path/to/photos"  # Replace with your actual root directory
RAW_FOLDER = "raw"
ALLOWED_EXTENSIONS = {'.nef', '.arw'}  # Case-insensitive check will be performed
DRY_RUN = True  # Set to False to actually remove empty directories

def is_hidden(path: Path) -> bool:
    """Check if a file or directory is hidden (starts with '.')"""
    return path.name.startswith('.')

def is_truly_empty(directory: Path) -> bool:
    """
    Double-check if a directory is truly empty.
    This is a safety check to ensure no files exist, including hidden ones.
    """
    try:
        # List all contents including hidden files
        items = list(directory.iterdir())
        return len(items) == 0
    except Exception as e:
        print(f"Warning: Could not check if directory {directory} is empty: {str(e)}")
        return False  # Err on the side of caution

def find_invalid_files(directory: Path) -> Tuple[List[Path], List[Path], List[Path]]:
    """
    Recursively check the directory for invalid files and empty directories.
    
    Args:
        directory: Path object pointing to the directory to check
        
    Returns:
        Tuple of (invalid extension files, hidden files, empty directories)
    """
    invalid_files = []
    hidden_files = []
    empty_dirs = []
    
    try:
        # First pass: collect files
        for item in directory.rglob('*'):
            if item.is_file():
                if is_hidden(item):
                    hidden_files.append(item)
                elif item.suffix.lower() not in ALLOWED_EXTENSIONS:
                    invalid_files.append(item)
        
        # Second pass: check for empty directories
        for item in directory.rglob('*'):
            if item.is_dir():
                if is_truly_empty(item):
                    empty_dirs.append(item)
                
    except Exception as e:
        print(f"Error accessing {directory}: {str(e)}")
        
    return invalid_files, hidden_files, empty_dirs

def remove_empty_directories(empty_dirs: List[Path]) -> int:
    """
    Remove empty directories with additional safety checks.
    Returns the count of removed directories.
    """
    if DRY_RUN:
        print("\nDRY RUN - No directories will be removed")
        print("The following directories would be removed:")
        for dir_path in sorted(empty_dirs, reverse=True):
            print(f"- {dir_path}")
        return 0
        
    removed_count = 0
    # Sort in reverse order to handle nested directories properly (deepest first)
    for dir_path in sorted(empty_dirs, reverse=True):
        try:
            # Double-check the directory is still empty before removing
            if is_truly_empty(dir_path):
                dir_path.rmdir()
                removed_count += 1
                print(f"Removed empty directory: {dir_path}")
            else:
                print(f"Skipped directory {dir_path} as it is no longer empty")
        except PermissionError as e:
            print(f"Permission denied when trying to remove {dir_path}: {str(e)}")
        except Exception as e:
            print(f"Error removing directory {dir_path}: {str(e)}")
    return removed_count

def main():
    raw_dir = Path(ROOT_DIR) / RAW_FOLDER
    
    if not raw_dir.exists():
        print(f"Error: Raw directory not found at {raw_dir}")
        return
    
    print(f"Checking for invalid files in {raw_dir}")
    print(f"Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}")
    if DRY_RUN:
        print("Running in DRY RUN mode - no directories will be removed")
    print("-" * 50)
    
    invalid_files, hidden_files, empty_dirs = find_invalid_files(raw_dir)
    
    # Report invalid extension files
    if not invalid_files:
        print("No invalid extensions found. All files are valid raw camera files.")
    else:
        print(f"\nFound {len(invalid_files)} files with invalid extensions:")
        for file_path in invalid_files:
            print(f"- {file_path}")
    
    # Report hidden files
    if hidden_files:
        print(f"\nFound {len(hidden_files)} hidden files:")
        for file_path in hidden_files:
            print(f"- {file_path}")
    
    # Handle empty directories
    if empty_dirs:
        print(f"\nFound {len(empty_dirs)} empty directories:")
        for dir_path in empty_dirs:
            print(f"- {dir_path}")
        
        removed_count = remove_empty_directories(empty_dirs)
        if not DRY_RUN and removed_count > 0:
            print(f"\nRemoved {removed_count} empty directories")
    else:
        print("\nNo empty directories found")
            
if __name__ == "__main__":
    main()
