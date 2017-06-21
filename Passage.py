"""
Simple passage class built to encapsulate a diverse group of passage types
"""


class Passage:
    def __init__(self):
        self._type = ""
        self._offset = 0
        self._text = ""
        self._keys = {}
