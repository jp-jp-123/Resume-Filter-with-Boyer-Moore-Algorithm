#
#   Author:
#   John Paul Beltran
#   - Base code and functionality
#   
#   Gian Paolo Buenconsejo
#   - Refactoring
#

import os
import datetime
from logger import logger
from pypdf import PdfReader as PDFReader


class PDFHandler:
    """
    Initialiaze a PDF Handler object to batch-read PDFs in a folder.

    Params
    ----------
    path : str
        Folder's directory to operate on.
    """
    
    def __init__(self, path: str=None, enableLogging: bool=False):
        self.folder_path = path
        self.EnableLogging = enableLogging
        self.current_log = ""

    def set_path(self, path: str):
        """
        Set folder path to batch-read PDF files on.
        """
        self.folder_path = path
        
        if self.EnableLogging:
            logger.log(f"Set root directory to {path}")

    def read(self, path: str=None) -> dict[str, str]:
        """
        Reads all PDF files from the root directory and its PDF contents.
        ### Returns
        - a dictionary where the key is the pdf filename as string, and the value is that pdf's contents as string
        """
        pdf_files_with_content = {}

        if path == None:
            path = self.folder_path

        if self.EnableLogging:
            logger.log(f"Start reading folder {self.folder_path}")

        for file in os.listdir(path):
            if file.endswith('.pdf'):
                file_path = f'{path}\{file}'

                if self.EnableLogging:
                    logger.log(f"Reading {file}...")

                file_contents = self._read_pdf(file_path)
                pdf_files_with_content[file] = file_contents

                if self.EnableLogging:
                    logger.log(f"Done reading {file}")

        if self.EnableLogging:
            logger.log(f"End of reading folder {self.folder_path}")

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