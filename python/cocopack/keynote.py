import os, re
import glob
import subprocess
import argparse
from copy import copy
from PIL import Image, ImageChops

def reformat_image_filenames(output_path, reformat_pattern):
    image_files = glob.glob(os.path.join(output_path, '*.png'))
    
    for image_file in image_files:
        basename = os.path.basename(image_file)
        slide_number = re.search(r'\d+', basename).group(0)
        new_filename = reformat_pattern.format(int(slide_number))
        new_filepath = os.path.join(output_path, new_filename)
        os.rename(image_file, new_filepath)

def keynote_to_images(input_path, output_path, filename_format='figure{:01d}.png'):
    #source: https://iworkautomation.com/keynote/document-export.html
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    applescript = f'''
    tell application "Keynote"
        set theDocument to open "{input_path}"
        set documentName to the name of theDocument
        set targetFolderHFSPath to POSIX file "{output_path}" as string

        export theDocument as slide images to file targetFolderHFSPath with properties {{image format:PNG, skipped slides:FALSE}}
    end tell
    '''
    
    subprocess.run(['osascript', '-e', applescript])
    
    if filename_format:
        reformat_image_filenames(output_path, filename_format)

def crop_whitespace(image_path, output_path=None, margin_size='1cm', dpi=300):

    def add_margin(image, margin_pixels):
        width, height = image.size
        new_width = width + 2 * margin_pixels
        new_height = height + 2 * margin_pixels
        new_image = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 255))
        new_image.paste(image, (margin_pixels, margin_pixels))
        return new_image

    def crop_single_image(source_file, output_file):
        image = Image.open(source_file)
        image = image.convert("RGBA")

        # Remove alpha channel by pasting the image onto a white background
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))
        background.paste(image, mask=image.split()[3])
        image_rgb = background.convert("RGB")

        # Find the bounding box and crop the image
        difference = ImageChops.difference(image_rgb, Image.new("RGB", image.size, (255, 255, 255)))
        bounds = difference.getbbox()
        cropped_image = image.crop(bounds)

        # Add margin if specified
        if margin_size:
            margin_cm = float(margin_size.strip('cm'))
            margin_pixels = int(margin_cm * dpi / 2.54)  # Convert cm to pixels
            cropped_image = add_margin(cropped_image, margin_pixels)

        cropped_image.save(output_file)

    if os.path.isdir(image_path):
        for filename in os.listdir(image_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                source_file = os.path.join(image_path, filename)
                if output_path:
                    output_file = os.path.join(output_path, filename)
                else:
                    output_file = source_file
                crop_single_image(source_file, output_file)
    else:
        if output_path is None:
            output_path = image_path
        crop_single_image(image_path, output_path)

def convert_to_pdf(image_path, output_path=None, dpi=300, **kwargs):
    """Convert PNG images to high-quality PDF files."""
    if output_path is None:
        output_path = copy(image_path)
    
    if os.path.isdir(image_path):
        for filename in os.listdir(image_path):
            if filename.lower().endswith('.png'):
                source_file = os.path.join(image_path, filename)
                output_file = os.path.join(output_path, os.path.splitext(filename)[0] + '.pdf')
                print(f'Converting {source_file} to {output_file}...')
                image = Image.open(source_file)
                # Convert to RGB mode if necessary
                if image.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1])
                    image = background
                image.save(output_file, 'PDF', resolution=dpi)
    else:
        output_file = os.path.splitext(output_path)[0] + '.pdf'
        image = Image.open(image_path)
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        image.save(output_file, 'PDF', resolution=dpi)

    if kwargs.get('pdf_only', False):
        os.remove(image_path)

def convert_all_images_to_pdf(input_path, dpi=300, **kwargs):
    image_files = glob.glob(os.path.join(input_path, '**/*.png'), recursive=True)
    for image_file in image_files:
        convert_to_pdf(image_file, None, dpi, **kwargs)

def mogrify_images_to_pdf(input_path, **kwargs):
    image_files = glob.glob(os.path.join(input_path, '**/*.png'), recursive=True)
    for image_file in image_files:
        subprocess.run(['mogrify', '-format', 'pdf', '-quality', '100', '-density', '300', image_file])

    if kwargs.get('pdf_only', False):
        for image_file in image_files:
            os.remove(image_file)
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Keynote slides to images and optionally crop whitespace.')
    parser.add_argument('-i', '--input_path', help='Path to the Keynote file.')
    parser.add_argument('-o', '--output_path', default=None, help='Output path for the images. (default: same as input_path)')
    parser.add_argument('-c', '--crop_images', default=True, type=bool, help='Whether to crop whitespace around images. (default: True)')
    parser.add_argument('-m', '--margin_size', default=None, help='Margin size to add back after cropping. (default: None)')
    parser.add_argument('--pdf', action='store_true', help='Convert images to high-quality PDFs (300 DPI)')
    parser.add_argument('--pdf_only', action='store_true', help='Only save as PDFs (delete PNG files)')
    
    args = parser.parse_args()

    if args.output_path is None:
        args.output_path = os.path.splitext(args.input_path)[0]

    keynote_to_images(args.input_path, args.output_path)

    if args.crop_images:
        crop_whitespace(args.output_path, margin_size=args.margin_size)

    if args.pdf or args.pdf_only:
        convert_all_images_to_pdf(args.output_path, dpi=300, pdf_only=args.pdf_only)