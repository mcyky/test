# LLaVA Image Downloader

A simple Python utility to download images from the LLaVA Bench in the Wild dataset.

## Quick Start

```bash
# Install wget (if not already installed)
sudo apt-get install wget  # Ubuntu/Debian
# or brew install wget      # macOS

# Run the downloader
python download.py
```

This will download 24 images (001.jpg to 024.jpg) to an `images/` directory.

## What it does

- Downloads images from [Hugging Face LLaVA dataset](https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild)
- Creates a local `images/` directory
- Downloads 24 numbered images (001.jpg through 024.jpg)
- Uses `wget` for reliable downloads

## Requirements

- Python 3.x
- `wget` command-line tool
- Internet connection
- ~5-10MB free disk space

## Output

```
images/
├── 001.jpg
├── 002.jpg
├── 003.jpg
└── ... (up to 024.jpg)
```

## Full Documentation

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for comprehensive documentation including:
- Detailed API reference
- Usage examples
- Troubleshooting guide
- Integration examples
- Customization options

## License

Please respect the original dataset's license terms when using these images.