import PyPDF2
import re
from tkinter import Tk, filedialog
from spellchecker import SpellChecker

#' For the pell checker
spell = SpellChecker()

#' Function to extract words from a PDF file
def extract_words_from_pdf(pdf_file):
    words = set()
    
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                #' Split text into words using regex to exclude punctuation
                page_words = re.findall(r'\b\w+\b', text)
                #' Add to the set of unique words
                words.update(page_words)
                
    return list(words)

#' Spell Checker
def correct_spelling(words):
    print("Correcting spelling...")
    corrected_words = [spell.correction(word) for word in words if word]  #' Ignore empty or None values
    corrected_words = [word for word in corrected_words if word]  #' Filter out any remaining None or empty values
    print(f"Total words after spelling correction: {len(corrected_words)}")
    return corrected_words

#' Function to sort words by length (longest to shortest), and then alphabetically
def sort_words(words):
    return sorted(words, key=lambda x: (-len(x), x.lower()))

#' Selects the PDF file
def select_pdf_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a PDF File", filetypes=[("PDF files", "*.pdf")])
    return file_path

# Processes and Saves PDF File
def process_pdf_and_save(output_file):
    pdf_file = select_pdf_file()
    if not pdf_file:
        print("No file selected. Exiting.")
        return
    
    words = extract_words_from_pdf(pdf_file)
    corrected_words = correct_spelling(words)
    sorted_words = sort_words(corrected_words)
    
    with open(output_file, 'w') as f:
        for word in sorted_words:
            f.write(word + '\n')
    
    print(f"Sorted word list saved to {output_file}")


#' Can set to .md or .txt etc.
output_file_path = '/Users/main/output.txt'

process_pdf_and_save(output_file_path)
