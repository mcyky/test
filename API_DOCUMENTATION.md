# API Documentation

## Project Overview

This project is an **Image Download Utility** that automatically downloads a collection of 24 images from the LLaVA benchmark dataset hosted on Hugging Face. The utility creates a local `images` directory and downloads sequentially numbered JPEG files.

## Project Structure

```
.
├── download.py          # Main download script
├── .gitignore          # Git ignore configuration
├── images/             # Downloaded images directory (created automatically)
│   ├── 001.jpg
│   ├── 002.jpg
│   └── ... (up to 024.jpg)
└── API_DOCUMENTATION.md # This documentation file
```

## Public APIs and Functions

### Main Script: `download.py`

#### Overview
The main script provides a simple, automated way to download the LLaVA benchmark images for local use.

#### Dependencies
- **Python Standard Library**:
  - `os`: For directory creation and system command execution
- **System Requirements**:
  - `wget`: Command-line tool for downloading files (must be installed on the system)

#### Configuration

| Variable | Type | Value | Description |
|----------|------|-------|-------------|
| `base_url` | `str` | `"https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild/resolve/main/images/"` | Base URL for downloading images |
| Image range | `int` | `1-24` | Number of images to download (001.jpg to 024.jpg) |
| Output directory | `str` | `"images/"` | Local directory where images are stored |

#### Workflow

1. **Directory Creation**: Automatically creates an `images` directory if it doesn't exist
2. **URL Generation**: Constructs download URLs for images numbered 001-024
3. **Image Download**: Uses `wget` to download each image with proper naming
4. **Completion Notification**: Prints completion message when all downloads finish

#### Usage Examples

##### Basic Usage
```bash
# Run the download script
python download.py
```

##### Expected Output
```
Download complete.
```

##### Verification
```bash
# Check downloaded images
ls -la images/
# Should show files: 001.jpg, 002.jpg, ..., 024.jpg
```

#### Error Handling

The script has minimal error handling and relies on:
- System `wget` availability
- Network connectivity to Hugging Face
- Write permissions in the current directory

#### File Operations

##### Directory Creation
```python
if not os.path.exists("images"):
    os.makedirs("images")
```
- **Purpose**: Ensures the output directory exists before downloading
- **Behavior**: Creates directory only if it doesn't already exist
- **Permissions**: Uses default system permissions

##### Image Download
```python
os.system(f"wget -O {image_path} {image_url}")
```
- **Purpose**: Downloads individual images using wget
- **Parameters**:
  - `image_path`: Local file path (e.g., "images/001.jpg")
  - `image_url`: Remote URL (e.g., "https://huggingface.co/.../001.jpg")
- **Behavior**: Overwrites existing files with same name

## Usage Instructions

### Prerequisites

1. **Python Installation**: Ensure Python 3.x is installed
2. **wget Installation**: 
   ```bash
   # Ubuntu/Debian
   sudo apt-get install wget
   
   # macOS (with Homebrew)
   brew install wget
   
   # Windows (with Chocolatey)
   choco install wget
   ```

### Running the Script

1. **Clone or download** the project files
2. **Navigate** to the project directory:
   ```bash
   cd /path/to/project
   ```
3. **Execute** the download script:
   ```bash
   python download.py
   ```
4. **Verify** the download:
   ```bash
   ls images/
   ```

### Expected Results

After successful execution:
- An `images/` directory will be created
- 24 JPEG files will be downloaded (001.jpg through 024.jpg)
- Each image is approximately 50-200KB in size
- Total download time varies based on network speed (typically 1-5 minutes)

### Customization Options

#### Download Different Image Range
```python
# Modify the range in download.py
for i in range(1, 50):  # Download 1-49 instead of 1-24
```

#### Change Output Directory
```python
# Modify directory name
output_dir = "my_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```

#### Add Progress Indication
```python
# Enhanced version with progress
for i in range(1, 25):
    image_number = str(i).zfill(3)
    print(f"Downloading image {i}/24: {image_number}.jpg")
    # ... download code ...
```

## Troubleshooting

### Common Issues

1. **wget not found**:
   ```
   Error: 'wget' is not recognized as an internal or external command
   ```
   **Solution**: Install wget using package manager

2. **Permission denied**:
   ```
   Error: Permission denied when creating directory
   ```
   **Solution**: Run with appropriate permissions or change target directory

3. **Network connectivity**:
   ```
   Error: Unable to resolve host
   ```
   **Solution**: Check internet connection and Hugging Face availability

4. **Disk space**:
   ```
   Error: No space left on device
   ```
   **Solution**: Free up disk space (images total ~5-10MB)

### Debugging Tips

1. **Enable verbose wget output**:
   ```python
   os.system(f"wget -v -O {image_path} {image_url}")
   ```

2. **Check individual URLs**:
   ```bash
   curl -I "https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild/resolve/main/images/001.jpg"
   ```

3. **Verify directory permissions**:
   ```bash
   ls -ld images/
   ```

## Integration Examples

### Using as a Module

Create a more modular version:

```python
# download_module.py
import os
from typing import List, Optional

class ImageDownloader:
    def __init__(self, base_url: str, output_dir: str = "images"):
        self.base_url = base_url
        self.output_dir = output_dir
    
    def download_images(self, start: int = 1, end: int = 25) -> bool:
        """Download images in the specified range."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        for i in range(start, end):
            success = self._download_single_image(i)
            if not success:
                return False
        return True
    
    def _download_single_image(self, number: int) -> bool:
        """Download a single image by number."""
        image_number = str(number).zfill(3)
        image_url = f"{self.base_url}{image_number}.jpg"
        image_path = f"{self.output_dir}/{image_number}.jpg"
        
        result = os.system(f"wget -q -O {image_path} {image_url}")
        return result == 0

# Usage
downloader = ImageDownloader(
    "https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild/resolve/main/images/"
)
success = downloader.download_images()
print(f"Download {'succeeded' if success else 'failed'}")
```

### Web API Wrapper

```python
# api_server.py
from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def trigger_download():
    """API endpoint to trigger image download."""
    try:
        result = subprocess.run(['python', 'download.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "Download completed"})
        else:
            return jsonify({"status": "error", "message": result.stderr})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/status', methods=['GET'])
def check_status():
    """Check download status by counting images."""
    if os.path.exists('images'):
        image_count = len([f for f in os.listdir('images') if f.endswith('.jpg')])
        return jsonify({"images_downloaded": image_count, "expected": 24})
    else:
        return jsonify({"images_downloaded": 0, "expected": 24})

if __name__ == '__main__':
    app.run(debug=True)
```

## License and Attribution

This utility downloads images from the **LLaVA Bench in the Wild** dataset:
- **Dataset**: [liuhaotian/llava-bench-in-the-wild](https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild)
- **Host**: Hugging Face Datasets
- **Usage**: Please respect the original dataset's license and terms of use

## Contributing

To contribute to this project:

1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** improvements with proper error handling
4. **Test** on multiple platforms
5. **Submit** a pull request

### Suggested Improvements

- Add proper error handling and logging
- Implement retry logic for failed downloads
- Add progress bars for better UX
- Support for different image formats
- Configuration file support
- Parallel downloads for speed improvement
- Resume capability for interrupted downloads

---

*Documentation generated on: $(date)*
*Project Version: 1.0.0*