import argparse
from pypdf import PdfReader, PdfWriter

def pdf_merge(paths, output):
    """
    Merge multiple PDF files into a single PDF file.

    Parameters:
    - paths (list): List of input PDF file paths to be merged.
    - output (str): Output PDF file path for the merged result.
    """
    pdf_writer = PdfWriter()
    for path in paths:
        pdf_reader = PdfReader(path)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    with open(output, 'wb') as out:
        pdf_writer.write(out)

def pdf_split(path, ranges):
    """
    Split a PDF file into multiple PDF files based on specified page ranges.

    Parameters:
    - path (str): Input PDF file path to be split.
    - ranges (list): List of tuples specifying page ranges for each output PDF file.
    """
    pdf_reader = PdfReader(path)
    for i in range(len(ranges)):
        pdf_writer = PdfWriter()
        pages = pdf_reader.pages[ranges[i][0]:ranges[i][1]]
        for page in pages:
            pdf_writer.add_page(page)
        output = f'{i}_output.pdf'
        with open(output, 'wb') as out:
            pdf_writer.write(out)

def main():
    """
    Main function to parse command-line arguments and perform PDF merge or split actions.
    """
    parser = argparse.ArgumentParser(description="PDF Merge and Split Tool")
    parser.add_argument('action', choices=['merge', 'split'], help='Action to perform: merge or split')
    parser.add_argument('input', nargs='+', help='Input PDF file paths')
    parser.add_argument('--output', help='Output PDF file path for merge action')
    parser.add_argument('--ranges', nargs='+', type=int, help='Page ranges for split action (e.g., --ranges 1 5 10 15)')

    args = parser.parse_args()

    if args.action == 'merge':
        if not args.output:
            parser.error('--output is required for merge action')
        pdf_merge(args.input, args.output)
    elif args.action == 'split':
        if not args.ranges:
            parser.error('--ranges is required for split action')
        ranges = [(args.ranges[i], args.ranges[i + 1]) for i in range(0, len(args.ranges), 2)]
        pdf_split(args.input[0], ranges)

if __name__ == "__main__":
    main()
