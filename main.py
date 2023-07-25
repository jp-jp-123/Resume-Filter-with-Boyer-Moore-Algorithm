#
#   Authors:
#   John Paul Beltran
#   Gian Paolo Buenconsejo
#   Johnmar James Munar
#   Kim Montana
#   

import os
from logger import logger
from file_handler import PDFHandler

# Expanded the char table to questionable size to accommodate questionable characters
NO_OF_CHARS = 10000

def cls():
    """
    Clears the console.
    """
    os.system('cls')


class BoyerMoore:   
    """
    Initialize a Boyer-Moore object to be used on string pattern matching...
    """

    class Result:
        """
        Boyer-Moore result object.
        """

        def __init__(self, filename: str=""):
            self.filename = filename
            self.pattern = ""
            self.text_length = 0
            self.pattern_length = 0
            self.matches = []
            self.matches_count = len(self.matches)
            self.total_shifts = 0
            

    def __init__(self, enable_logging=False) -> None:
        self.filepath = ""
        self.patterns = []
        self.results = []
        self.matched_pdfs = []
        self.unmatched_pdfs = []
        self.enable_logging = enable_logging

    def set_path(self, filepath: str):
        """
        Set filepath of folder to search.
        """
        self.filepath = filepath

    def add_pattern(self, pattern: str):
        """
        Add pattern to search.
        """
        self.patterns.append(pattern)

    def _preprocess_bad_char(self, pattern: str):
        """
        Preprocessing function for bad character heuristic.
        """
        bad_char = [-1] * NO_OF_CHARS

        for i in range(len(pattern)):
            bad_char[ord(pattern[i])] = i

        return bad_char

    def _preprocess_suffix(self, shift, borderPosition, pattern, m):
        """
        Preprocessing function for strong suffix case (case one).
        """
        i = len(pattern)
        j = m + 1
        borderPosition[i] = j

        # traversing until the size of the pattern is greater than 0
        while i > 0:
            """
            If the character at position (i-1) is not the same as the character at (j-1), then continue the algorithm.
            """
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                '''
                The character preceding the occurrence 
                of t in pattern P is different than the 
                mismatching character in P, we stop skipping
                the occurrences and shift the pattern 
                from i to j
                '''
                if shift[j] == 0:
                    shift[j] = j - i

                # Updating the position of the next border
                j = borderPosition[j]

            """
            Since p[i-1] is matched with p[j-1] then we have found the border, then store the border.
            """
            i -= 1
            j -= 1
            borderPosition[i] = j

    def _preprocess_prefix(self, shift, borderPosition, pattern, m):
        """
        Preprocessing function for prefix case (case two).
        """
        j = borderPosition[0]

        for i in range(m + 1):
            """
            setting the border position of the pattern's first character to all the indices in the shift array.
            """
            if shift[i] == 0:
                shift[i] = j

            """
            Suffix becomes shorter than borderPosition[0], use the position of the next widest border as the value of j.

            Now if the suffix becomes shorter than borderPosition[0], we need to use the next position of
            the widest border as the new value of j.
            """
            if i == j:
                j = borderPosition[j]

    def _search(self, text: str, pattern: str, enable_debugging=False) -> Result:
        """
        Search a given pattern in a given text using the
        Bad Character and Good Suffix rules of the Boyer Moore Algorithm.

        ### Params
        - text: text to search into
        - pattern: pattern to search in text
        """

        result = self.Result()
        result.text_length = text_length = len(text)
        result.pattern_length = pattern_length = len(pattern)
        border_position = [0] * (pattern_length + 1)
        suffix_shift_table = [0] * (pattern_length + 1)

        # Preprocessing
        bad_char = self._preprocess_bad_char(pattern)
        self._preprocess_suffix(suffix_shift_table, border_position, pattern, pattern_length)
        self._preprocess_prefix(suffix_shift_table, border_position, pattern, pattern_length)

        current_shift = 0  # Shift of the pattern with respect to text
        while current_shift <= text_length - pattern_length:
            j = pattern_length - 1

            # Keep comparing characters until mismatch
            # This is relative to the current shift
            while j >= 0 and pattern[j] == text[current_shift + j]:
                if enable_debugging:
                    cls()
                    print(text)
                    space = " " * current_shift
                    needle_offset = " " * (current_shift + j)
                    print(f"{space}{pattern}".format())
                    print(f"{needle_offset}^".format())
                    print(f"Characters match")
                    input()
                j -= 1

            if enable_debugging and j > 0:
                cls()
                print(text)
                space = " " * current_shift
                needle_offset = " " * (current_shift + j)
                print(f"{space}{pattern}".format())
                print(f"{needle_offset}^".format())
                print(f"Mismatch occured at index: {j}")

            # If the pattern is present at current shift
            # then index j will become -1 after the above loop
            if j < 0:
                if enable_debugging:
                    print(f"Pattern match at: {current_shift + 1}")
                result.matches.append(current_shift)

                """   
                Shift the pattern so that the next character in text
                aligns with the last occurrence of it in pattern.
                The condition s+m < n is necessary for the case when
                pattern occurs at the end of text
                """
                bad_character_shift = (pattern_length - bad_char[
                    ord(text[current_shift + pattern_length])] if current_shift + pattern_length < text_length else 1)
                good_suffix_shift = suffix_shift_table[0]
            else:
                """
                Shift the pattern so that the bad character in text
                aligns with the last occurrence of it in pattern.
                The max function is used to make sure that we get a positive
                shift. We may get a negative shift if the last occurrence
                of bad character in pattern is on the right side of the
                current character.
                """
                # print(current_shift)
                bad_character_shift = max(1, j - bad_char[ord(text[current_shift + j])])
                good_suffix_shift = suffix_shift_table[j + 1]

            if enable_debugging:
                print(f"BCS: {bad_character_shift} | GSS: {good_suffix_shift}")
                if (bad_character_shift > good_suffix_shift):
                    print("Will use Bad character rule")
                else:
                    print("Will use Good suffix rule")
                input()
                cls()

            current_shift += max(bad_character_shift, good_suffix_shift)

        result.pattern = pattern
        result.total_shifts = current_shift
        result.matches_count = len(result.matches)
        return result

    def start(self):
        """
        Start Boyer-Moore algorithm.
        """
        # Process files
        pdf_handler = PDFHandler(enable_logging=True)
        pdf_handler.set_path(self.filepath)
        folder = pdf_handler.read()

        cls()
        for pdf_file, pdf_contents in folder.items():
            if not self.patterns:
                break

            text = pdf_contents

            for pattern in self.patterns:
                result = self._search(text, pattern)
                result.filename = pdf_file
                self.results.append(result)

                #TODO: Resume segretation (matched and unmatched)


def main():
    boyer_moore = BoyerMoore(enable_logging=True)
    # GUI should utilize this command vv
    set_path = r"C:\Users\Lenovo\Documents\DOCX\test data\ACCOUNTANT"
    boyer_moore.set_path(set_path)
    boyer_moore.add_pattern("staff")
    boyer_moore.add_pattern("person")
    boyer_moore.add_pattern("data")
    boyer_moore.start()

    pdfhandler = PDFHandler()

    for result in boyer_moore.results:
        print(f"File: {result.filename}")
        print(f"\tPattern: {result.pattern}")
        print(f"\tText length: {result.text_length}")
        print(f"\tPattern occurences: {result.matches}")
        print(f"\tPattern count: {result.matches_count}")

        # Add condition later to enable and disable this function
        if result.matches_count > 0:
            pdfhandler._copy_pdf(set_path, result.filename, result.pattern)

    pdfhandler._del_pdf(set_path)

    print("\nLogs:")
    print(logger.get_logs())

main()
