#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import logging

# We'll import convert_from_path in the function after we've confirmed dependencies
# to avoid throwing an immediate ImportError on import if pdf2image isn't installed.
# Comment: This code works, but avoid using jpeg and for some reason the loop which is meant to raise an error when you pass a jpeg format doesn't work.
def setup_logging():
    """
    Configure logging for debug and error information.
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO
    )

def check_dependencies(poppler_path=None):
    """
    Ensure that pdf2image library is installed and Poppler is accessible.

    - Try importing pdf2image
    - Check if pdftoppm binary is on PATH or in poppler_path
    """
    # 1) Check for pdf2image
    try:
        import pdf2image  # noqa: F401
    except ImportError:
        logging.error("The 'pdf2image' library is not installed. Install it via: pip install pdf2image")
        sys.exit(1)

    # 2) Check for Poppler (pdftoppm)
    # If poppler_path is provided, look in that directory; otherwise, look on the system PATH.
    pdftoppm_cmd = "pdftoppm"
    if poppler_path is not None:
        pdftoppm_full = os.path.join(poppler_path, pdftoppm_cmd)
        if not os.path.isfile(pdftoppm_full):
            logging.error(f"Poppler utility 'pdftoppm' was not found in: {poppler_path}")
            sys.exit(1)
    else:
        # If poppler_path is None, we check PATH
        if shutil.which(pdftoppm_cmd) is None:
            logging.error("Poppler utility 'pdftoppm' is not in your PATH. Please install Poppler or provide --poppler_path.")
            sys.exit(1)

def check_file_permissions(pdf_file, output_dir):
    """
    Verify that the script has read access to the PDF file and write access to the output directory.
    """
    # Check PDF readability
    if not os.path.isfile(pdf_file):
        logging.error(f"PDF file '{pdf_file}' does not exist.")
        sys.exit(1)
    if not os.access(pdf_file, os.R_OK):
        logging.error(f"PDF file '{pdf_file}' is not readable. Check permissions.")
        sys.exit(1)

    # Check output dir writability
    # If output_dir doesn't exist, try to create it.
    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            logging.error(f"Failed to create output directory '{output_dir}': {e}")
            sys.exit(1)

    # If it exists, confirm we can write to it
    if not os.access(output_dir, os.W_OK):
        logging.error(f"Output directory '{output_dir}' is not writable. Check permissions.")
        sys.exit(1)

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Convert a PDF file into a series of images with dependency and permission checks.'
    )
    parser.add_argument('pdf_file', help='Path to the input PDF file.')
    parser.add_argument('output_dir', help='Path to output directory.')
    parser.add_argument('--dpi', type=int, default=200,
                        help='Dots per inch for the output images.')
    parser.add_argument('--fmt', default='png',
                        help='Image format (e.g. "png", "jpeg").')
    parser.add_argument('--poppler_path', default=None,
                        help='Path to Poppler executables if not in system PATH.')
    return parser.parse_args()

def convert_pdf_to_images(pdf_file, output_dir, dpi=200, fmt='png', poppler_path=None):
    """
    Convert a PDF file into a series of images.
    """
    # Only import pdf2image here to ensure we've passed the check_dependencies function first
    from pdf2image import convert_from_path

    logging.info(f"Converting '{pdf_file}' to images...")
    pages = convert_from_path(
        pdf_file,
        dpi=dpi,
        fmt=fmt,
        poppler_path=poppler_path
    )

    for idx, page in enumerate(pages, start=1):
        out_file = os.path.join(output_dir, f"page_{idx}.{fmt}")
        print(out_file)
        # fmt.upper() just converts e.g. 'png' → 'PNG' for Pillow to correctly identify the format
        # Convert image to RGB if saving as JPEG
        if fmt.lower() == 'jpeg':
            logging.error("Jpeg does not have an alpha channel, and thus we might get 'OSError: cannot write RGBA as JPEG. In any case, jpeg is not an acceptable format. Feel free to make it acceptable by modifying the code.")
            sys.exit(1)
        page.save(out_file, fmt.upper())
        logging.info(f"Saved page {idx} to '{out_file}'")

    logging.info("Conversion complete.")

def main():
    setup_logging()
    args = parse_arguments()

    # Check for required dependencies (poppler, pdf2image)
    check_dependencies(args.poppler_path)
    
    # Check if input file is readable and output directory is writable
    check_file_permissions(args.pdf_file, args.output_dir)

    print(args.pdf_file)   # should be "input.pdf"
    print(args.output_dir) # should be "output_folder"
    print(args.fmt)        # should be "png"
    print(args.dpi)        # should be 300

    # If everything is good, proceed with conversion
    convert_pdf_to_images(
        args.pdf_file,
        args.output_dir,
        dpi=args.dpi,
        fmt=args.fmt,
        poppler_path=args.poppler_path
    )

if __name__ == '__main__':
    main()
