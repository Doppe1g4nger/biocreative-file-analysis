# AA_to_F1Score
import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle
import multiprocessing as mp

kinase_input_dir = '/data/CM_output/FT/Post-Processed/All/Kinase_BP_Test'
axis_input_dir = '/data/CM_output/FT/Post-Processed/All/GO-old'
output_file = '/data/CM_output/FT/Post-Processed/All/FT_All_TestSet_GO-old.pkl'
#del axis_input_dirs[0]
kinase_list = []
axis_list = []
total_positives = 0
pred_positives = {}
results_dict = {}


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def kinase_processor(filename):
    obj = load_obj(kinase_input_dir + "/" + filename)
    if obj.number_of_hits > 0:
        return filename


def axis_processor(filename):
    obj = load_obj(axis_input_dir + "/" + filename)
    if obj.number_of_hits > 0:
        return filename


def overlap_processor(filename):
    if filename is not None:
        pmcid = filename.strip('.txt.xmi.pkl')
        obj = load_obj(kinase_input_dir + "/" + filename)
        for canon_term in obj.set_of_hit_terms:
            try:
                results_dict[canon_term].append(pmcid)
            except KeyError:
                results_dict[canon_term] = [pmcid]


if __name__ == "__main__":

    k_inputs = [filename for filename in os.listdir(kinase_input_dir)]
    a_inputs = [filename for filename in os.listdir(axis_input_dir)]

    pool = mp.Pool(processes=8)
    kinase_list = pool.map(kinase_processor, k_inputs)
    print(kinase_list)

    axis_list = pool.map(axis_processor, a_inputs)
    print(axis_list)

    overlap_list = [elem for elem in axis_list if elem in kinase_list]

    ocount = 0

    for filename in overlap_list:
        overlap_processor(filename)
        ocount += 1
        if ocount % 1000 == 0:
            print(ocount)

    with open(output_file, 'wb') as output_file:
        pickle.dump(results_dict, output_file, pickle.HIGHEST_PROTOCOL)

    print(results_dict)

    current_file = axis_input_dir
    print(current_file)
