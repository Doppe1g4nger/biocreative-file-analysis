from collections import Counter
import copy


class AnnotatedArticle:

    dictionary_name = ""
    number_of_hits = 0
    set_of_hit_terms = set()
    counter_of_hit_terms = Counter()
    list_of_attrib_dicts = []
    original_text = ""

    def __init__(self, dictionary_name, number_of_hits, set_of_hit_terms, counter_of_hit_terms,
                 list_of_attrib_dicts, original_text=""):
        self.dictionary_name = dictionary_name
        self.number_of_hits = number_of_hits
        self.set_of_hit_terms = set_of_hit_terms
        self.counter_of_hit_terms = counter_of_hit_terms
        self.list_of_attrib_dicts = list_of_attrib_dicts
        self.original_text = original_text

    @classmethod
    def copy(cls, cls_instance):
            d_name = copy.deepcopy(cls_instance.dictionary_name)
            num_hits = copy.deepcopy(cls_instance.number_of_hits)
            set_terms = copy.deepcopy(cls_instance.set_of_hit_terms)
            hit_counter = copy.deepcopy(cls_instance.counter_of_hit_terms)
            attrib_dict = copy.deepcopy(cls_instance.list_of_attrib_dicts)
            return cls(d_name, num_hits, set_terms, hit_counter, attrib_dict)
