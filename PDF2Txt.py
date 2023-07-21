import os
from pypdf import PdfReader as pdfreader

# The folder directory
# once the gui is added, we replace the directory here
path = 'C:\\Users\\Lenovo\\Documents\\DOCX\\data\\selected'
os.chdir(path)


# Read the PDF files
def ReadPDF(filePath):
    reader = pdfreader(filePath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


# Don't bother, i just used this to troubleshoot the offending index in the PDF
def SplitPDF():
    reader = pdfreader('C:\\Users\\Lenovo\\Documents\\DOCX\\data\\selected\\18159866.pdf')
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # text = text.encode('utf-8')
    text = text[10130:]
    return text


# Iterate the folder, not used, but kept for reference
def IterateFolder():
    for file in os.listdir():
        if file.endswith('.pdf'):
            filePath = f'{path}\{file}'

            ReadPDF(filePath)


# Modified IterateFolder, the usable one
def ReadFolder():
    textPerFile = {}

    for file in os.listdir():
        if file.endswith('.pdf'):
            filePath = f'{path}\{file}'
            text = ReadPDF(filePath)
            textPerFile[file] = text

    return textPerFile


if __name__ == '__main__':
    folder = ReadFolder()

    for file, filetext in folder.items():
        print(f"File: {file}")
        print(f"{filetext}")
