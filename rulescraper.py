import os
import subprocess

def get_pdf_page_count(pdf_path):
    """Run pdfinfo to get the number of pages in the PDF."""
    result = subprocess.run(['pdfinfo', pdf_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running pdfinfo: {result.stderr.decode()}")
        return None
    # Extract the number of pages from the output
    output = result.stdout.decode()
    for line in output.split('\n'):
        if 'Pages' in line:
            return int(line.split(':')[1].strip())
    return None

def clean_and_save(text: str, filepath: str):
    # clean clean clean
    lines = text.split('\n')
    cleanlines = [line for line in lines if line.strip() and len(line.strip()) > 3]
    cleantext = '\n'.join(cleanlines)
    if len(cleantext):
        with open(filepath, 'w') as f:
            f.write(cleantext)
        return 0
    else:
        return 1
        


def extract_pdf_pages(pdf_path, num_pages):
    """Run pdftotext for each page and save to individual text files."""
    name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    for page_num in range(1, num_pages + 1):
        command = ['pdftotext', '-f', str(page_num), '-l', str(page_num), '-enc', 'UTF-8', '-nopgbrk', pdf_path, "-"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            output = result.stdout.decode()
            if len(output) > 1:
                output_file = f'data/text/{name}_{page_num}.txt'
                clean_and_save(output, output_file)
                print(f'{output_file} saved')
        else:
            print(f"Error extracting page {page_num}: {result.stderr.decode()}")

def pdf_has_enough_text(pdf_path,cutoff=10):
    command = ['pdftotext', '-enc', 'UTF-8', '-nopgbrk', pdf_path, "-"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        output = result.stdout.decode()
        return len(output) > cutoff

game_name = 'Cascadia'
pdf_path = f'data/pdfs/{game_name}.pdf'

if pdf_has_enough_text(pdf_path):
    num_pages = get_pdf_page_count(pdf_path)
    if num_pages:
        print(f"{game_name} PDF has {num_pages} pages.")
        extract_pdf_pages(pdf_path, num_pages)
    else:
        print("Failed to retrieve the number of pages.")
else:
    print(game_name, "PDF doesn't have enough text!")
