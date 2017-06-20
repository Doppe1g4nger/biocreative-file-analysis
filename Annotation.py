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
            if not args:
                if self._text is None or self._start is None or self._end is None:
                    raise ValueError("Too few arguments passed, Annotation must have at least text, start, and end", 0)
            elif len(args) == 1:
                if self._start is None or self._end is None:
                    raise ValueError("Too few arguments passed, Annotation must have at least text, start, and end", 0)
                else:
                    self._text = args[0]
            elif len(args) == 2:
                if self._end is None:
                    raise ValueError("Too few arguments passed, Annotation must have at least text, start, and end", 0)
                else:
                    self._text = args[0]
                    self._start = args[1]
            elif len(args) == 3:
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
            else:
                self._text = args[0]
                self._start = args[1]
                self._end = args[2]
                self._ontology = args[3]
                self._id = args[4]
                raise ValueError("Too many arguments passed, Some parameter were ignored", 1)
        except ValueError as err:
            if err.args[1] == 1:
                print(err.args[0])
            else:
                raise

    def get_text(self):
        return self._text

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_bounds(self):
        return self._start, self._end

    def get_id(self):
        return self._id

    def get_ontology(self):
        return self._ontology