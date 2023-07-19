# a function to handle the strong suffix case.
def preprocess_suffix(shift, borderPosition, pattern, m):
    i = m
    j = m + 1
    borderPosition[i] = j
    # traversing until the size of the pattern is greater than 0
    while i > 0:
        """
        If the character at position (i-1) is not the same as the character at (j-1), then continue the algorithm.
        """
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            ''' the character preceding the occurrence 
                of t in pattern P is different than the 
                mismatching character in P, we stop skipping
                the occurrences and shift the pattern 
                from i to j '''
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

# a function to handle the prefix case.


def preprocess_prefix(shift, borderPosition, pattern, m):
    j = borderPosition[0]
    for i in range(m + 1):
        """
        setting the border position of the pattern's first character to all the indices in the shift array.
        """
        if shift[i] == 0:
            shift[i] = j

        """
        suffix becomes shorter than borderPosition[0], use the position of the next widest border as the value of j.

        Now if the suffix becomes shorter than borderPosition[0], we need to use the next position of
        the widest border as the new value of j.
        """
        if i == j:
            j = borderPosition[j]

#  A function that searches the string and returns the occurrence.


def boyerMooreAlgorithm(text, pattern):
    # s is a shift of the pattern concerning input text.
    s = 0
    m = len(pattern)
    n = len(text)

    """
    an array to store the shifts and border position will store the widest border of the pattern.

    initialize all occurrences of the shift to 0.
    """
    shift = [0] * (m + 1)
    borderPosition = [0] * (m + 1)

    # first performing the preprocessing
    preprocess_suffix(shift, borderPosition, pattern, m)
    preprocess_prefix(shift, borderPosition, pattern, m)
    print(borderPosition)

    while s <= n - m:
        j = m - 1

        """
        If the pattern and text are matching, keep on reducing the j variable.
        """
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        """
        If the pattern is present at the current shift, then j will become -1.
        """
        if j < 0:
            print("Pattern found at index:", s)
            s += shift[0]
        else:
            """
            pattern[i] != pattern[s+j] so Shifting the pattern so that the bad character of the text is aligned.
            """
            s += shift[j + 1]
            # print(shift[j+1])


text = "can i find it nope but i hope"
pattern = "coltcol"
boyerMooreAlgorithm(text, pattern)