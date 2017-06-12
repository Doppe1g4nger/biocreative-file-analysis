class NCIConcept:
    """
    A wrapper class to represent concepts from the NCI Thesaurus
    """

    def __init__(self, *args, **kwargs):
        # Case for inputting a single OrderedDict from csv.DictReader
        if len(args) == 1:
            prop_dict = args[0]
            self.code = prop_dict["code"]
            self.concept_name = prop_dict["concept_name"]
            self.parents = set(prop_dict["parents"].split("|"))
            self.synonyms = set(prop_dict["synonyms"].split("|"))
            self.definition = prop_dict["definition"]
            self.display_name = set(prop_dict["display_name"].split("|"))
            self.concept_status = set(prop_dict["concept_status"].split("|"))
            self.semantic_type = set(prop_dict["semantic_type"].split("|"))
        # Case for manual entry of all 8 arguments
        elif len(args) == 8:
            self.code = args[0]
            self.concept_name = args[1]
            self.parents = args[2]
            self.synonyms = args[3]
            self.definition = args[4]
            self.display_name = args[5]
            self.concept_status = args[6]
            self.semantic_type = args[7]
        # Case for no arguments or partial args via named assignments
        elif len(args) == 0:
            self.code = kwargs.get("code", "")
            self.concept_name = kwargs.get("concept_name", "")
            self.parents = kwargs.get("parents", set())
            self.synonyms = kwargs.get("synonyms", set())
            self.definition = kwargs.get("definition", "")
            self.display_name = kwargs.get("display_name", set())
            self.concept_status = kwargs.get("concept_status", set())
            self.semantic_type = kwargs.get("semantic_type", set())
