import lxml.etree as etree
from collections import defaultdict
import pickle


def id_to_canonical_dict():
    nx_to_canon_dict = {}
    with open("/home/daniel/Downloads/ConMapDictionaries/Protein Dictionaries/all_kinases.xml") as infile:
        root = etree.parse(infile)
        for token in root.iter("token"):
            nx_to_canon_dict[token.attrib["id"]] = token.attrib["canonical"]
    return nx_to_canon_dict


if __name__ == "__main__":
    id_to_canon = id_to_canonical_dict()
    canon_to_docset = defaultdict(set)
    fpath = input("Give path to training data qrel file: ")
    with open(fpath) as qrel_file:
        for line in qrel_file:
            line = line.split()
            doc_id, doc = line[0], line[2]
            canonical = id_to_canon[doc_id]
            canon_to_docset[canonical].add(doc)
    fname = fpath.split("/")[-1].strip(".qrel")
    with open("/home/daniel/Downloads/PickleFiles/TrainingCanonicalNames_ToDocID_dicts/"
              + fname + "_canon_to_docid_dict.pkl", "wb") as outfile:
        pickle.dump(dict(canon_to_docset), outfile)
