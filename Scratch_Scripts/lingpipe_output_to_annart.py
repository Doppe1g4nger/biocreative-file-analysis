import lxml.etree as etree
import os.path as path
from os import listdir
from AnnotatedArticle import AnnotatedArticle
from collections import Counter
import pickle


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]

if __name__ == "__main__":
    outpath = input("Input folder path to dump annotation pickles: ")
    for file in get_all_files(input("Give file path to LingPipe output: ")):
        an_art = AnnotatedArticle("LingPipe", 0, set(), Counter(), [])
        root = etree.parse(file)
        hit_list = []
        attrib_list = []
        for item in root.iter("ENAMEX"):
            if float(item.attrib["condProb"]) >= .9:
                an_art.number_of_hits += 1
                an_art.set_of_hit_terms.add(item.attrib["TEXT"])
                hit_list.append(item.attrib["TEXT"])
                attrib_list.append(dict(item.attrib))
        an_art.counter_of_hit_terms = Counter(hit_list)
        an_art.list_of_attrib_dicts = attrib_list
        print(an_art.__dict__)
        with open(outpath + file.split("/")[-1].strip(".xml") + ".pkl", "wb") as outfile:
            pickle.dump(an_art, outfile)
