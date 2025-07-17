# Function Reference

This document provides detailed technical specifications for all functions and components in the LLaVA Image Downloader project.

## Table of Contents

- [Core Functions](#core-functions)
- [Utility Functions](#utility-functions)
- [Configuration Constants](#configuration-constants)
- [Error Handling](#error-handling)
- [Type Specifications](#type-specifications)

## Core Functions

### `main() -> int`

**Purpose**: Entry point for the image download process.

**Parameters**: None

**Returns**: 
- `int`: Exit code (0 = success, 1 = failure)

**Behavior**:
1. Displays configuration information
2. Validates wget availability
3. Initiates download process
4. Reports final results

**Usage**:
```python
exit_code = main()
sys.exit(exit_code)
```

**Dependencies**: 
- `download_image_range()`
- System `wget` command

---

### `download_image_range(base_url, start=1, end=25, output_dir="images", verbose=False) -> Tuple[int, int]`

**Purpose**: Download a sequential range of numbered images.

**Parameters**:
- `base_url` (str): Base URL where images are hosted
- `start` (int, optional): Starting image number (inclusive). Default: 1
- `end` (int, optional): Ending image number (exclusive). Default: 25
- `output_dir` (str, optional): Local directory for downloads. Default: "images"
- `verbose` (bool, optional): Enable detailed logging. Default: False

**Returns**: 
- `Tuple[int, int]`: (successful_downloads, total_attempts)

**Example**:
```python
# Download images 1-10 to 'my_images' directory
success, total = download_image_range(
    "https://example.com/images/", 
    start=1, 
    end=11, 
    output_dir="my_images",
    verbose=True
)
print(f"Downloaded {success}/{total} images")
```

**Error Conditions**:
- Returns (0, 0) if output directory creation fails
- Continues on individual download failures

---

### `download_single_image(image_url, local_path, verbose=False) -> bool`

**Purpose**: Download a single image file using wget.

**Parameters**:
- `image_url` (str): Complete URL of the image to download
- `local_path` (str): Local file path where image should be saved
- `verbose` (bool, optional): Show wget command output. Default: False

**Returns**: 
- `bool`: True if download succeeded, False otherwise

**Technical Details**:
- Uses `os.system()` to execute wget command
- Wget flags: `-v` (verbose) or `-q` (quiet)
- Always uses `-O` flag to specify output file

**Example**:
```python
success = download_single_image(
    "https://example.com/image.jpg",
    "local/path/image.jpg",
    verbose=True
)
```

**System Requirements**:
- `wget` must be installed and in PATH
- Write permissions to target directory

---

## Utility Functions

### `create_output_directory(directory_path="images") -> bool`

**Purpose**: Create directory for downloaded files if it doesn't exist.

**Parameters**:
- `directory_path` (str, optional): Path to create. Default: "images"

**Returns**: 
- `bool`: True if directory exists or was created, False on error

**Behavior**:
- Checks existence with `os.path.exists()`
- Creates with `os.makedirs()` if needed
- Handles OSError exceptions gracefully

**Example**:
```python
if create_output_directory("downloads/images"):
    print("Directory ready")
else:
    print("Failed to create directory")
```

---

### `format_image_number(number, width=3) -> str`

**Purpose**: Format integers with leading zeros for consistent file naming.

**Parameters**:
- `number` (int): Integer to format
- `width` (int, optional): Total width of result string. Default: 3

**Returns**: 
- `str`: Zero-padded string representation

**Technical Details**:
- Uses Python's `str.zfill()` method
- Useful for maintaining sort order in file systems

**Examples**:
```python
format_image_number(1)      # Returns "001"
format_image_number(42)     # Returns "042"
format_image_number(5, 4)   # Returns "0005"
```

---

### `construct_image_url(base_url, image_number, extension="jpg") -> str`

**Purpose**: Build complete URL for image download.

**Parameters**:
- `base_url` (str): Base URL ending with "/" 
- `image_number` (str): Formatted image number (e.g., "001")
- `extension` (str, optional): File extension. Default: "jpg"

**Returns**: 
- `str`: Complete download URL

**URL Structure**: `{base_url}{image_number}.{extension}`

**Example**:
```python
url = construct_image_url(
    "https://example.com/images/",
    "042",
    "png"
)
# Returns: "https://example.com/images/042.png"
```

---

### `construct_local_path(directory, image_number, extension="jpg") -> str`

**Purpose**: Build local file path for saving images.

**Parameters**:
- `directory` (str): Local directory path
- `image_number` (str): Formatted image number (e.g., "001")
- `extension` (str, optional): File extension. Default: "jpg"

**Returns**: 
- `str`: Local file path

**Path Structure**: `{directory}/{image_number}.{extension}`

**Example**:
```python
path = construct_local_path("images", "042", "png")
# Returns: "images/042.png"
```

---

## Configuration Constants

### Default Configuration (in `main()`)

| Constant | Value | Description |
|----------|-------|-------------|
| `BASE_URL` | `"https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild/resolve/main/images/"` | Source URL for images |
| `START_IMAGE` | `1` | First image number to download |
| `END_IMAGE` | `25` | One past the last image number (downloads 1-24) |
| `OUTPUT_DIRECTORY` | `"images"` | Local directory for downloads |

### Customizable Parameters

```python
# Example custom configuration
CUSTOM_CONFIG = {
    "base_url": "https://my-server.com/images/",
    "start": 10,
    "end": 50,
    "output_dir": "downloaded_images",
    "verbose": True
}
```

---

## Error Handling

### System Dependency Checks

```python
# Check for wget availability
if os.system("which wget > /dev/null 2>&1") != 0:
    # Handle missing wget
    return 1
```

### Directory Creation Errors

```python
try:
    os.makedirs(directory_path)
except OSError as e:
    print(f"Error creating directory: {e}")
    return False
```

### Download Failures

- Individual download failures don't stop the batch process
- Failed downloads are logged but process continues
- Final summary shows success/failure ratio

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All downloads successful |
| 1 | System dependency missing or critical error |
| 1 | Some downloads failed |

---

## Type Specifications

### Import Requirements

```python
import os
import sys
from typing import Optional, Tuple
```

### Function Signatures

```python
def create_output_directory(directory_path: str = "images") -> bool: ...

def format_image_number(number: int, width: int = 3) -> str: ...

def construct_image_url(base_url: str, image_number: str, extension: str = "jpg") -> str: ...

def construct_local_path(directory: str, image_number: str, extension: str = "jpg") -> str: ...

def download_single_image(image_url: str, local_path: str, verbose: bool = False) -> bool: ...

def download_image_range(
    base_url: str,
    start: int = 1,
    end: int = 25,
    output_dir: str = "images",
    verbose: bool = False
) -> Tuple[int, int]: ...

def main() -> int: ...
```

### Data Structures

#### Return Tuples

- `download_image_range()` returns `(successful_downloads: int, total_attempts: int)`
- Both values are non-negative integers
- `successful_downloads <= total_attempts` always

#### String Formats

- Image numbers: Zero-padded strings (e.g., "001", "042")
- URLs: Must end with file extension
- Paths: Use forward slashes for cross-platform compatibility

---

## Performance Considerations

### Download Speed

- Sequential downloads (not parallel)
- Speed limited by network bandwidth and server response
- Typical: 1-5 minutes for 24 images

### Memory Usage

- Minimal memory footprint
- No image data stored in memory
- Direct stream from source to disk via wget

### Disk Usage

- ~5-10MB total for 24 LLaVA images
- Individual images: 50-200KB each
- No temporary files created

### Scalability

```python
# For large batches, consider progress reporting
def download_with_progress(base_url, start, end, output_dir):
    total = end - start
    for i, current in enumerate(range(start, end), 1):
        # Download logic here
        print(f"Progress: {i}/{total} ({100*i/total:.1f}%)")
```

---

## Testing Examples

### Unit Test Structure

```python
import unittest
import tempfile
import os

class TestImageDownloader(unittest.TestCase):
    
    def test_format_image_number(self):
        self.assertEqual(format_image_number(1), "001")
        self.assertEqual(format_image_number(42, 4), "0042")
    
    def test_construct_paths(self):
        url = construct_image_url("https://example.com/", "001")
        self.assertEqual(url, "https://example.com/001.jpg")
        
        path = construct_local_path("images", "001")
        self.assertEqual(path, "images/001.jpg")
    
    def test_directory_creation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "test_images")
            result = create_output_directory(test_dir)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(test_dir))
```

### Integration Test

```python
def test_download_workflow():
    """Test complete download workflow with mock server."""
    # Setup mock HTTP server
    # Test directory creation
    # Test URL construction
    # Test download process
    # Verify file creation
    # Cleanup
```

---

*Function Reference - Version 1.0.0*  
*Generated: $(date)*