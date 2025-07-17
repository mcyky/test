#!/usr/bin/env python3
"""
LLaVA Image Downloader

This module provides functionality to download images from the LLaVA Bench in the Wild dataset
hosted on Hugging Face. It creates a local directory structure and downloads numbered image files.

Author: Generated Documentation
Version: 1.0.0
License: See original dataset license
"""

import os
import sys
from typing import Optional, Tuple


def create_output_directory(directory_path: str = "images") -> bool:
    """
    Create the output directory for downloaded images if it doesn't exist.
    
    Args:
        directory_path (str): Path to the directory to create. Defaults to "images".
        
    Returns:
        bool: True if directory exists or was created successfully, False otherwise.
        
    Raises:
        OSError: If directory creation fails due to permissions or other system errors.
        
    Example:
        >>> create_output_directory("my_images")
        True
        >>> create_output_directory("/invalid/path")
        False
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")
        else:
            print(f"Directory already exists: {directory_path}")
        return True
    except OSError as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False


def format_image_number(number: int, width: int = 3) -> str:
    """
    Format an image number with leading zeros.
    
    Args:
        number (int): The image number to format.
        width (int): Total width of the formatted string. Defaults to 3.
        
    Returns:
        str: Zero-padded string representation of the number.
        
    Example:
        >>> format_image_number(1)
        '001'
        >>> format_image_number(42, 4)
        '0042'
    """
    return str(number).zfill(width)


def construct_image_url(base_url: str, image_number: str, extension: str = "jpg") -> str:
    """
    Construct the full URL for downloading an image.
    
    Args:
        base_url (str): The base URL where images are hosted.
        image_number (str): The formatted image number (e.g., "001").
        extension (str): File extension. Defaults to "jpg".
        
    Returns:
        str: Complete URL for the image.
        
    Example:
        >>> construct_image_url("https://example.com/images/", "001")
        'https://example.com/images/001.jpg'
    """
    return f"{base_url}{image_number}.{extension}"


def construct_local_path(directory: str, image_number: str, extension: str = "jpg") -> str:
    """
    Construct the local file path for saving an image.
    
    Args:
        directory (str): Local directory where the image will be saved.
        image_number (str): The formatted image number (e.g., "001").
        extension (str): File extension. Defaults to "jpg".
        
    Returns:
        str: Local file path for the image.
        
    Example:
        >>> construct_local_path("images", "001")
        'images/001.jpg'
    """
    return f"{directory}/{image_number}.{extension}"


def download_single_image(image_url: str, local_path: str, verbose: bool = False) -> bool:
    """
    Download a single image using wget.
    
    Args:
        image_url (str): URL of the image to download.
        local_path (str): Local path where the image should be saved.
        verbose (bool): Whether to show wget output. Defaults to False.
        
    Returns:
        bool: True if download succeeded (exit code 0), False otherwise.
        
    Note:
        This function requires wget to be installed on the system.
        
    Example:
        >>> download_single_image("https://example.com/image.jpg", "local/image.jpg")
        True
    """
    wget_flags = "-v" if verbose else "-q"
    command = f"wget {wget_flags} -O {local_path} {image_url}"
    
    if verbose:
        print(f"Executing: {command}")
    
    result = os.system(command)
    return result == 0


def download_image_range(
    base_url: str,
    start: int = 1,
    end: int = 25,
    output_dir: str = "images",
    verbose: bool = False
) -> Tuple[int, int]:
    """
    Download a range of numbered images from a base URL.
    
    Args:
        base_url (str): Base URL where images are hosted.
        start (int): Starting image number (inclusive). Defaults to 1.
        end (int): Ending image number (exclusive). Defaults to 25.
        output_dir (str): Local directory for downloaded images. Defaults to "images".
        verbose (bool): Whether to show detailed download progress. Defaults to False.
        
    Returns:
        Tuple[int, int]: (successful_downloads, total_attempts)
        
    Example:
        >>> success, total = download_image_range("https://example.com/", 1, 5)
        >>> print(f"Downloaded {success}/{total} images")
        Downloaded 4/4 images
    """
    if not create_output_directory(output_dir):
        print("Failed to create output directory. Aborting.")
        return 0, 0
    
    successful_downloads = 0
    total_attempts = end - start
    
    print(f"Starting download of {total_attempts} images...")
    
    for i in range(start, end):
        image_number = format_image_number(i)
        image_url = construct_image_url(base_url, image_number)
        local_path = construct_local_path(output_dir, image_number)
        
        if verbose:
            print(f"Downloading image {i}/{end-1}: {image_number}.jpg")
        
        if download_single_image(image_url, local_path, verbose):
            successful_downloads += 1
        else:
            print(f"Failed to download image {image_number}")
    
    return successful_downloads, total_attempts


def main() -> int:
    """
    Main function to download LLaVA benchmark images.
    
    Downloads 24 images (001.jpg to 024.jpg) from the LLaVA Bench in the Wild dataset
    hosted on Hugging Face to a local 'images' directory.
    
    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    # Configuration
    BASE_URL = "https://huggingface.co/datasets/liuhaotian/llava-bench-in-the-wild/resolve/main/images/"
    START_IMAGE = 1
    END_IMAGE = 25  # Exclusive, so downloads 1-24
    OUTPUT_DIRECTORY = "images"
    
    print("LLaVA Image Downloader")
    print("=" * 50)
    print(f"Source: {BASE_URL}")
    print(f"Range: {START_IMAGE:03d}.jpg to {END_IMAGE-1:03d}.jpg")
    print(f"Output: {OUTPUT_DIRECTORY}/")
    print("=" * 50)
    
    # Check if wget is available
    if os.system("which wget > /dev/null 2>&1") != 0:
        print("Error: wget is not installed or not in PATH")
        print("Please install wget and try again:")
        print("  Ubuntu/Debian: sudo apt-get install wget")
        print("  macOS: brew install wget")
        print("  Windows: choco install wget")
        return 1
    
    # Download images
    successful, total = download_image_range(
        BASE_URL,
        START_IMAGE,
        END_IMAGE,
        OUTPUT_DIRECTORY,
        verbose=False
    )
    
    # Report results
    print("=" * 50)
    if successful == total:
        print(f"Download complete! Successfully downloaded {successful}/{total} images.")
        return 0
    else:
        print(f"Download completed with errors. {successful}/{total} images downloaded.")
        return 1


if __name__ == "__main__":
    """
    Entry point when script is run directly.
    
    Usage:
        python download_documented.py
    """
    exit_code = main()
    sys.exit(exit_code)