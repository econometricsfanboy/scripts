# PDF to Image Converter

A simple Python script that converts a PDF file into a series of images, with built-in dependency and permission checks. The script ensures that the required libraries and utilities are installed and accessible before proceeding with the conversion.

---

## Features

- **Dependency Checking:**  
  - Verifies that the `pdf2image` library is installed.
  - Checks for the Poppler utility `pdftoppm` (either on the system PATH or in a specified directory).

- **File and Directory Permissions:**  
  - Ensures that the input PDF file exists and is readable.
  - Checks that the output directory exists or can be created and is writable.

- **Customizable Conversion Settings:**  
  - Supports specifying the DPI (Dots Per Inch) for the conversion.
  - Allows the choice of image format (default is PNG).

- **Logging:**  
  - Provides informative logging to trace execution and troubleshoot errors.

---

## Requirements

- **Python 3.x**
- **pdf2image:** Install via:
  ```bash
  pip install pdf2image

## Note
The script includes a check that exits if the image format is specified as JPEG. This is because JPEG does not support an alpha channel, which might lead to errors when saving images that include transparency. If you need to support JPEG, use something else or modify the code.

## Usage
  ```bash
  python extractor.py <pdf_file> <output_dir> [--dpi DPI] [--fmt FORMAT] [--poppler_path PATH]
