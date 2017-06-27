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
    for file in get_all_files("/home/daniel/Downloads/LingPipeAnnotations/BP_Irrelevant_genia/"):
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
        if not found_match:
            none_found_count += 1
    print("avg annotations per article:", tot_annotations / num_articles)
    print("abstracts with no annotations:", no_annotations)
    print("no matches found:", none_found_count)
