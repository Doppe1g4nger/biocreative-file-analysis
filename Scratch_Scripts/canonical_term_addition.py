import lxml.etree as etree
import pickle
import os.path as path
from os import listdir
from AnnotatedArticle import AnnotatedArticle


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]

if __name__ == "__main__":
    syn_to_can = {}
    root = etree.parse("/home/daniel/Downloads/ConMapDictionaries/Protein Dictionaries/all_kinases.xml")
    for token in root.iter("token"):
        for variant in token.iter("variant"):
            syn_to_can[variant.attrib["base"].strip().lower()] = token.attrib["canonical"]
    for file in get_all_files(input("Give pickle folder: ")):
        hit = False
        an_obj = None
        with open(file, "rb") as infile:
            infile.seek(0)
            an_obj = pickle.load(infile)
        new_hit_terms = set()
        for term in an_obj.set_of_hit_terms:
            if term.strip().lower() in syn_to_can.keys():
                hit = True
                print(term, syn_to_can[term.strip().lower()])
                new_hit_terms.add(syn_to_can[term.strip().lower()])
        for item in new_hit_terms:
            an_obj.set_of_hit_terms.add(item)
        if hit:
            with open(file, "wb") as outfile:
                pickle.dump(an_obj, outfile)
