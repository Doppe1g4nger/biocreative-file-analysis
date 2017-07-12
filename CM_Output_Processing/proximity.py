import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle
import multiprocessing as mp


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

kinase_input_dir = r"C:/Users/Adam/Documents/MSU REU/FT_Post-Processed/HP"
axis_input_dir = r"C:/Users/Adam/Documents/MSU REU/FT_Post-Processed/GO"
predicted_dictionary_input = r"C:/Users/Adam/Documents/MSU REU/FT_All_TestSet_GO.pkl"
word_count_dictionary_input = ""
axis_tokens = []
kinase_tokens = []
metric_dict = {}

pred_dict = load_obj(predicted_dictionary_input)
# wc_dict = load_obj(word_count_dictionary_input)


for kinase in pred_dict:
    try:
        for doc in pred_dict[kinase]:
            axis_AA = load_obj(axis_input_dir + "/" + doc + ".txt.xmi.pkl")
            kinase_AA = load_obj(kinase_input_dir + "/" + doc + ".txt.xmi.pkl")
            axis_tokens = []
            kinase_tokens = []
            axis_attribs = axis_AA.list_of_attrib_dicts
            kinase_attribs = kinase_AA.list_of_attrib_dicts
            for attrib in axis_attribs:
                for token in attrib['matchedTokens'].split(" "):
                    axis_tokens.append(int(token))
            for attrib in kinase_attribs:
                for token in attrib['matchedTokens'].split(" "):
                    kinase_tokens.append(int(token))
            min_proximity = 999999
            for k in kinase_tokens:
                for a in axis_tokens:
                    dist = abs(k - a) / 10
                    if dist < min_proximity:
                        min_proximity = dist
            # print(doc + ": " + str(min_proximity))
            try:
                metric_dict[kinase].append([doc, min_proximity])
            except KeyError:
                metric_dict[kinase] = [[doc, min_proximity]]
            # print(metric_dict)
    except EOFError:
        pass
