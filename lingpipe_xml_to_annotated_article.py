from AnnotatedArticle import AnnotatedArticle
import os.path as path
from os import listdir
import lxml.etree as etree
import pickle
from collections import Counter


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]


if __name__ == "__main__":
    cutoff = float(input("Choose conditional probability cutoff: "))
    num_over_1 = 0
    num_over_5 = 0
    total = 0
    for file in get_all_files("/home/daniel/Downloads/LingPipeAnnotations/GeneTagConfidence/BP_Relevant/"):
        annotation_set = set()
        annotation_count = 0
        article_attribute_dict = []
        annotation_list = []
        annotatated_xml = etree.parse(file)
        for annotation in annotatated_xml.iter("ENAMEX"):
            total += 1
            if float(annotation.attrib["condProb"]) >= .5:
                num_over_5 += 1
                num_over_1 += 1
            elif float(annotation.attrib["condProb"]) >= .1:
                num_over_1 += 1
            if float(annotation.attrib["condProb"]) >= cutoff:
                annotation_set.add(annotation.attrib["TEXT"])
                annotation_count += 1
                article_attribute_dict.append(dict(annotation.attrib))
                annotation_list.append(annotation.attrib["TEXT"])
        ann_obj = AnnotatedArticle("BP_Relevant", annotation_count, annotation_set,
                                   Counter(annotation_list), article_attribute_dict)
        file_id = str(file.split("/")[-1].strip(".xml"))
        with open("/home/daniel/Downloads/PickleFiles/LingPipeAA_Confidence/GeneTag/BP_Relevant/"
                  + file_id + ".pkl", "wb") as out:
            pickle.dump(ann_obj, out)
    print(total, num_over_1, num_over_5)
