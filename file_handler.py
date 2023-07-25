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
import shutil
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

    def __init__(self, path: str = None, enable_logging: bool = False):
        self.folder_path = path
        self.enable_logging = enable_logging
        self.current_log = ""
        self.copied_files_list = []

    def set_path(self, path: str):
        """
        Set folder path to batch-read PDF files on.
        """
        self.folder_path = path

        if self.enable_logging:
            logger.log(f"Set root directory to {path}")

    def read(self, path: str = None) -> dict[str, str]:
        """
        Reads all PDF files from the root directory and its PDF contents.
        ### Returns
        - a dictionary where the key is the pdf filename as string, and the value is that pdf's contents as string
        """
        pdf_files_with_content = {}

        if path == None:
            path = self.folder_path

        if self.enable_logging:
            logger.log(f"Initializing data set from {self.folder_path}")

        for file in os.listdir(path):
            if file.endswith('.pdf'):
                file_path = f'{path}\{file}'

                if self.enable_logging:
                    logger.log(f"Reading {file}...")

                file_contents = self._read_pdf(file_path)
                pdf_files_with_content[file] = file_contents

                if self.enable_logging:
                    logger.log(f"Done reading {file}")

        # if self.enable_logging:
        #     logger.log(f"End of reading folder {self.folder_path}")

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

    def _copy_pdf(self, path, file_matches, pattern):
        """
        Creates a new folder in root directory with pattern as the name, then copies all the file with
        matches into it. Lists all the copied lists for deletion
        :param path: root path
        :param file_matches: filenames of the matched pdfs
        :param pattern: the pattern to be used in new directory
        :return:
        """

        file_matches_list = [file_matches]

        new_path = os.path.join(path, pattern)
        try:
            os.mkdir(new_path)
            logger.log(f"{new_path} has been created")
        except OSError:
            logger.log(f"{new_path} already exists")

        for file in range(len(file_matches_list)):
            current_file = file_matches_list[file]

            source_file = os.path.join(path, current_file)
            destination_file = os.path.join(new_path, current_file)

            shutil.copy2(source_file, destination_file)
            logger.log(f"{source_file} has been moved to {destination_file}")

            self.copied_files_list.append(source_file)

    def _del_pdf(self, path):
        """
        deletes the files that has been copied. Essentially moving a file but due to code structure, this has to be done
        separately. 'cfl' creates a list with all duplicate filenames removed.
        :param path: root path
        :return:
        """

        cfl = list(set(self.copied_files_list))

        for file in range(len(cfl)):
            current_file = os.path.join(path, cfl[file])

            if os.path.exists(current_file):
                os.remove(current_file)
                logger.log(f"{cfl[file]} has been removed in {path}")

            else:
                logger.log(f"{cfl[file]} doesn't exist")
