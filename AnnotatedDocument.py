"""
Hella not finished
"""


class AnnotatedObject:
    def __init__(self):
        self._id = ""
        self._tags = {}  # Dict of infon tags found at the beginning of each abstract or fulltext
        self._passages = {}  # Dict of passages, each key links to a list of Passage objects
