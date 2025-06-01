#!/usr/bin/env python3

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import re


def parse_markdown(text):
    """
    Parse markdown content and convert to reportlab elements
    """
    elements = []
    styles = getSampleStyleSheet()

    # Create custom styles with unique names
    heading1_style = ParagraphStyle(
        name='CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.navy
    )

    heading2_style = ParagraphStyle(
        name='CustomHeading2',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.navy
    )

    normal_style = ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        spaceBefore=6,
        spaceAfter=6
    )

    # Split the content by lines
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Handle headings
        if line.startswith('# '):
            elements.append(Paragraph(line[2:], heading1_style))
        elif line.startswith('## '):
            elements.append(Paragraph(line[3:], heading2_style))
        # Handle horizontal rules
        elif line.startswith('---'):
            elements.append(Spacer(1, 10))
        # Handle empty lines
        elif line == '':
            elements.append(Spacer(1, 6))
        # Handle bold text
        elif '**' in line:
            # Replace markdown bold with reportlab bold
            line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
            elements.append(Paragraph(line, normal_style))
        # Handle normal text
        else:
            elements.append(Paragraph(line, normal_style))

        i += 1

    return elements


def convert_md_to_pdf(input_file, output_file):
    """
    Convert a markdown file to PDF
    """
    try:
        # Read the markdown file
        with open(input_file, "r") as f:
            md_content = f.read()

        # Create the PDF document
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        elements = parse_markdown(md_content)

        # Build the PDF
        doc.build(elements)
        return True
    except Exception as e:
        print(f"Error converting {input_file}: {str(e)}")
        return False


def main():
    """
    Main function to process all markdown files in input_resumes directory
    """
    input_dir = "input-resumes"
    output_dir = "resume-pdfs"

    # Check if directories exist
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Created input directory: {input_dir}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Get all markdown files from input directory
    md_files = [f for f in os.listdir(input_dir) if f.endswith(('.md', '.markdown'))]

    if not md_files:
        print(f"No markdown files found in {input_dir} directory.")
        return

    # Process each markdown file
    success_count = 0
    for md_file in md_files:
        input_path = os.path.join(input_dir, md_file)

        # Create output filename (replace .md or .markdown with .pdf)
        output_filename = os.path.splitext(md_file)[0] + ".pdf"
        output_path = os.path.join(output_dir, output_filename)

        print(f"Processing: {md_file}")
        if convert_md_to_pdf(input_path, output_path):
            success_count += 1
            print(f"  ✓ Successfully converted to {output_filename}")
        else:
            print(f"  ✗ Failed to convert {md_file}")

    print(f"\nConversion complete: {success_count} of {len(md_files)} files converted successfully.")


if __name__ == "__main__":
    main()
