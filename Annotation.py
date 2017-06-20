"""
Annotation class, stores data on Annotations from CM or NCBO annotations
"""


class Annotation:
    def __init__(self, *args, **kwargs):
        self._text = kwargs.get("text", None)
        self._start = kwargs.get("start", None)
        self._end = kwargs.get("end", None)
        self._ontology = kwargs.get("ontology", None)
        self._id = kwargs.get("id", None)
        try:
            if self._text is None or self._start is None or self._end is None:
                if len(args) < 3:
                    raise ValueError("Too few arguments passed, Annotation must have at least text, start, and end")
            if len(args) == 3:
                self._text = args[0]
                self._start = args[1]
                self._end = args[2]
            elif len(args) == 4:
                self._text = args[0]
                self._start = args[1]
                self._end = args[2]
                self._ontology = args[3]
            elif len(args) == 5:
                self._text = args[0]
                self._start = args[1]
                self._end = args[2]
                self._ontology = args[3]
                self._id = args[4]

