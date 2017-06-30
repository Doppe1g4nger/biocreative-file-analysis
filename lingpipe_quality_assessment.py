import lxml.etree as etree
import os.path as path
from os import listdir


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]


if __name__ == "__main__":
    kinase_path = "/home/daniel/Downloads/ConMapDictionaries/Protein Dictionaries/all_kinases.xml"
    kinase_set = set()
    tree = etree.parse(kinase_path)
    for elem in tree.iter("token"):
        for item in [child.attrib["base"] for child in elem.iter("variant")]:
            kinase_set.add(item)
    none_found_count = 0
    no_annotations = 0
    tot_annotations = 0
    num_articles = 0
    num_art_over_9 = 0
    num_art_over_5 = 0
    num_art_over_1 = 0
    num_ann_over_9 = 0
    num_ann_over_5 = 0
    num_ann_over_1 = 0
    count = 0
    for file in get_all_files(input("Give file path to LingPipe output xml folder: ")):
        count += 1
        print(count, file)
        o_9 = False
        o_5 = False
        o_1 = False
        num_articles += 1
        xml_tree = etree.parse(file)
        found_match = False
        if not xml_tree.iter("ENAMAX"):
            no_annotations += 1
        for elem in xml_tree.iter("ENAMEX"):
            tot_annotations += 1
            for term in kinase_set:
                if term in elem.text:
                    found_match = True
            if float(elem.attrib["condProb"]) >= .9:
                o_9 = True
                num_ann_over_9 += 1
            if float(elem.attrib["condProb"]) >= .5:
                o_5 = True
                num_ann_over_5 += 1
            if float(elem.attrib["condProb"]) >= .1:
                o_1 = True
                num_ann_over_1 += 1
        if o_9:
            num_art_over_9 += 1
        if o_5:
            num_art_over_5 += 1
        if o_1:
            num_art_over_1 += 1
        if not found_match:
            none_found_count += 1
    print("num articles with hits >= .9: ", num_art_over_9)
    print("num articles with hits >= .5: ", num_art_over_5)
    print("num articles with hits >= .1: ", num_art_over_1)
    print("avg annotations with >= .9 hits: ", num_ann_over_9 / num_articles)
    print("avg annotations with >= .5 hits: ", num_ann_over_5 / num_articles)
    print("avg annotations with >= .1 hits: ", num_ann_over_1 / num_articles)
    print("avg annotations per article:", tot_annotations / num_articles)
    print("abstracts with no annotations:", no_annotations)
    print("no matches found:", none_found_count)
    print("articles with no matches >= .9 hits: ", num_articles - num_art_over_9)
    print("articles with no matches >= .5 hits: ", num_articles - num_art_over_5)
    print("articles with no matches >= .1 hits: ", num_articles - num_art_over_1)
