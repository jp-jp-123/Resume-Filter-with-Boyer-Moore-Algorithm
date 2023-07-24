
import os
from pypdf import PdfReader as PDFReader


class PDFHandler:
    """
    Initialiaze a PDF Handler object to batch-read PDFs in a folder.

    Params
    ----------
    path : str
        Folder's directory to operate on.
    """
    
    def __init__(self, path: str=None):
        self.folder_path = path

    def set_path(self, path: str):
        self.folder_path = path

    def read(self, path: str=None) -> dict[str, str]:
        """
        Reads all PDF files from the root directory and its PDF contents.
        ### Returns
        - a dictionary where the key is the pdf filename as string, and the value is that pdf's contents as string
        """
        pdf_files_with_content = {}

        if path == None:
            path = self.folder_path

        for file in os.listdir(path):
            if file.endswith('.pdf'):
                file_path = f'{path}\{file}'
                file_contents = self._read_pdf(file_path)
                pdf_files_with_content[file] = file_contents

        return pdf_files_with_content

    def _read_pdf(self, filepath: str):
        """
        Extracts text content from a single PDF file.
        ### Params
        - filepath of the PDF file.
        ### Returns
        - string of text containing all PDF contents.
        """
        # Read PDF
        reader = PDFReader(filepath)
        content = ""

        for page in reader.pages:
            content += page.extract_text() + "\n"

        return content