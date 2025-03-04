from cocopack.figure_ops import (
    slides_to_images,
    convert_all_images_to_pdf
)

from os.path import splitext

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Convert Keynote slides to images and optionally crop whitespace.')
    parser.add_argument('-i', '--input_path', help='Path to the Keynote file.')
    parser.add_argument('-o', '--output_path', default=None, help='Output path for the images. (default: same as input_path)')
    parser.add_argument('-c', '--crop_images', default=True, type=bool, help='Crop whitespace around images. (default: True)')
    parser.add_argument('-m', '--margin_size', default='1cm', help='Margin size (in cm) to add back after cropping. (default: 1cm)')
    parser.add_argument('--pdf', action='store_true', help='Convert images to high-quality PDFs (300 DPI)')
    parser.add_argument('--pdf_only', action='store_true', help='Only save as PDFs (delete original PNG files)')
    
    args = parser.parse_args()

    if args.output_path is None:
        args.output_path = splitext(args.input_path)[0]

    slides_to_images(args.input_path, args.output_path, 
                     crop_images=args.crop_images, 
                     margin_size=args.margin_size)

    if args.pdf or args.pdf_only:
        convert_all_images_to_pdf(args.output_path, dpi=300, pdf_only=args.pdf_only)