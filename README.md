# Raw Photo Files Checker

A Python script to validate and maintain a directory of raw camera files. The script checks for invalid file extensions, hidden files, and empty directories within your raw photos directory.

## Features

- Validates file extensions against a list of allowed raw photo formats (`.nef`, `.arw`)
- Identifies hidden files (files starting with '.')
- Finds and optionally removes empty directories
- Includes a dry-run mode for safe testing

## Requirements

- Python 3.6 or higher
- No additional dependencies required

## Configuration

The script uses the following configuration variables at the top of `check_raw_files.py`:

```python
ROOT_DIR = "/path/to/photos"           # Replace with your photo directory path
RAW_FOLDER = "raw"                     # Name of the raw photos subdirectory
ALLOWED_EXTENSIONS = {'.nef', '.arw'}  # Allowed raw file extensions (case-insensitive)
DRY_RUN = True                         # Set to False to actually remove empty directories
```

## Usage

1. Edit the configuration variables in `check_raw_files.py` to match your setup:
   - Set `ROOT_DIR` to your photos directory path
   - Adjust `RAW_FOLDER` if your raw photos are in a different subdirectory
   - Modify `ALLOWED_EXTENSIONS` if you need to support different raw formats
   - Set `DRY_RUN` to `False` when you're ready to remove empty directories

2. Run the script:

```bash
python check_raw_files.py
```

## Example Output

```text
Checking for invalid files in /path/to/photos/raw
Allowed extensions: .nef, .arw
Running in DRY RUN mode - no directories will be removed
--------------------------------------------------

No invalid extensions found. All files are valid raw camera files.

Found 2 hidden files:
- /path/to/photos/raw/.DS_Store
- /path/to/photos/raw/2023/.hidden_file

Found 3 empty directories:
- /path/to/photos/raw/2023/empty_folder
- /path/to/photos/raw/2022/unused_folder
- /path/to/photos/raw/old_imports

DRY RUN - No directories will be removed
The following directories would be removed:
- /path/to/photos/raw/2023/empty_folder
- /path/to/photos/raw/2022/unused_folder
- /path/to/photos/raw/old_imports
```

## Safety Features

- Dry-run mode (enabled by default) lets you preview changes before making them
- Double verification of empty directories before removal
- Proper handling of nested directories (removes deepest directories first)
- Error handling for permission issues and other potential problems

## Notes

- The script performs case-insensitive extension checking
- Hidden files are reported but not removed
- Empty directory removal is optional and controlled by the `DRY_RUN` setting
- The script will only remove directories that are completely empty (including hidden files)
