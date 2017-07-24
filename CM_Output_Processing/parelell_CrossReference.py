# parelell cross referecne
import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle
import multiprocessing as mp
import tqdm

kinase_input_dir = '/data/CM_output/Abst/Post-Processed/BandT/Kinase_BP_Train_RW'
axis_input_dir = '/data/CM_output/Abst/Post-Processed/BandT/GO-old'
output_file = '/data/CM_output/Abst/Post-Processed/IR/Abst_GO-old_Train_IR.pkl'
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
    try:
        obj = load_obj(kinase_input_dir + "/" + filename)
        if obj.number_of_hits > 0:
            return filename
    except EOFError:
        pass


def axis_processor(filename):
    try:
        obj = load_obj(axis_input_dir + "/" + filename)
        if obj.number_of_hits > 0:
            return filename
    except EOFError:
        pass


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

    pool = mp.Pool(processes=2)

    kinase_list = pool.map(kinase_processor, k_inputs)
    print("klist: " + str(len(kinase_list)))

    axis_list = pool.map(axis_processor, a_inputs)
    print("alist: " + str(len(axis_list)))

    kinase_set = set(kinase_list)
    print("kset: " + str(len(kinase_set)))

    hitcount = 0
    for elem in axis_list:
        if elem is not None and elem in kinase_set:
            overlap_list.append(elem)
        hitcount += 1
        if hitcount % 10000 == 0:
            print("ocbuild " + str(hitcount))

    print("olist: " + str(len(overlap_list)))

    ocount = 0

    for filename in overlap_list:
        overlap_processor(filename)
        ocount += 1
        if ocount % 10000 == 0:
            print("ovprcess " + str(ocount))

    with open(output_file, 'wb') as output_file:
        pickle.dump(results_dict, output_file, pickle.HIGHEST_PROTOCOL)

    print("dict length: " + str(len(results_dict)))

    current_file = axis_input_dir
    print(current_file)


if __name__ == "__main__":
    run_my_shit()
