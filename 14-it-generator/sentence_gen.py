"""
Sentence: iterate over words using a generator function
"""

import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    """An iterable class"""

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        # list of str objects
        for word in self.words:  # <1>
            yield word  # <2>
        return  # <3>

# done! <4>
