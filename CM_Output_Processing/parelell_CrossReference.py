# parelell cross referecne
import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle
import multiprocessing as mp
import tqdm

kinase_input_dir = '/data/CM_output/Comparison_FT/Kinases/Combined/Post-Processed/DIS'
axis_input_dir = '/data/CM_output/Comparison_FT/Ontologies/Combined/Post-Processed/DIS/HP'
output_file = '/data/CM_output/FT/Post-Processed/All/juink.pkl'
# del axis_input_dirs[0]
kinase_list = []
axis_list = []
overlap_list = []
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


def overlap_creator(elem):
    if elem in kinase_list:
        return elem


def overlap_processor(filename):
    if filename is not None:
        pmcid = filename.strip('.txt.xmi.pkl')
        obj = load_obj(kinase_input_dir + "/" + filename)
        for canon_term in obj.set_of_hit_terms:
            try:
                results_dict[canon_term].append(pmcid)
            except KeyError:
                results_dict[canon_term] = [pmcid]


def run_my_shit():
    global kinase_list
    global output_file
    global axis_list
    global overlap_list

    k_inputs = [filename for filename in os.listdir(kinase_input_dir)]
    a_inputs = [filename for filename in os.listdir(axis_input_dir)]

    pool = mp.Pool(processes=16)

    kinase_list = pool.map(kinase_processor, k_inputs)
    print(kinase_list)

    axis_list = pool.map(axis_processor, a_inputs)
    print(axis_list)

    oc_inputs = [elem for elem in axis_list]

    print(oc_inputs)

    # overlap_list = pool.map(overlap_creator, oc_inputs)

    hitcount = 0
    for hit in oc_inputs:
        overlap_list.append(overlap_creator(hit))
        hitcount += 1
        if hitcount % 1000 == 0:
            print("ocbuild " + str(hitcount))

    print(overlap_list)

    ocount = 0

    for filename in overlap_list:
        overlap_processor(filename)
        ocount += 1
        if ocount % 1000 == 0:
            print("ovprcess " + str(ocount))

    with open(output_file, 'wb') as output_file:
        pickle.dump(results_dict, output_file, pickle.HIGHEST_PROTOCOL)

    print(results_dict)

    current_file = axis_input_dir
    print(current_file)


if __name__ == "__main__":
    run_my_shit()
