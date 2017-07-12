import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle
import multiprocessing as mp


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


if __name__ == "main":
    kinase_input_dir = ""
    axis_input_dir = ""
    dictionary_input = ""

    pred_dict = load_obj(dictionary_input)

    for kinase in pred_dict:
        for doc in kinase:
            axis_AA = load_obj(axis_input_dir + "/" + doc)
            kinase_AA = load_obj(axis_input_dir + "/" + doc)
            axis_tokens = axis_AA.list_of_attrib_dicts[3]
            kinase_tokens = axis_AA.list_of_attrib_dicts[3]
            min_proximity = 999999
            for k in kinase_tokens:
                for a in axis_tokens:
                    if abs(k - a) < min_proximity:
                        min_proximity = abs(k - a)

            print(doc + ": " + min_proximity)



