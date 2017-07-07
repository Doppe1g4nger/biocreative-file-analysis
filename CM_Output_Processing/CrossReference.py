# AA_to_F1Score
import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle

kinase_input_dir = '/data/CM_output/Comparison_FT/Kinases/Combined/Post-Processed/BP'
axis_input_dirs = ['/data/CM_output/Comparison_FT/Ontologies/Combined/Post-Processed/BP/GO']
output_file = '/data/CM_output/FT/Post-Processed/All/test.pkl'
#del axis_input_dirs[0]
kinase_list = []
axis_list = []
total_positives = 0


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

kcount = 0

for filename in os.listdir(kinase_input_dir):
    obj = load_obj(kinase_input_dir + "/" + filename)
    if obj.number_of_hits > 0:
        kinase_list.append(filename)
    kcount += 1
    if kcount % 10 == 0:
        print("kinase " + str(kcount))


for i in range(0, len(axis_input_dirs)):
    axis_list = []
    pred_positives = {}
    counter = 0
    print("\n\n")
    temp_count = 0
    for filename in os.listdir(axis_input_dirs[i]):
        counter += 1
        if counter % 10 == 0:
            print("axis " + str(counter))
        obj = load_obj(axis_input_dirs[i] + "/" + filename)
        if obj.number_of_hits > 0:
            axis_list.append(filename)


    print("TEMP: " + str(temp_count))

    overlap_list = [elem for elem in axis_list if elem in kinase_list]
    print(overlap_list)

    results_dict = {}
    ocount = 0
    for filename in overlap_list:
        ocount += 1
        if ocount % 10 == 0:
            print("overlap " + str(ocount))
        pmcid = filename.strip('.txt.xmi.pkl')
        obj = load_obj(kinase_input_dir + "/" + filename)
        for canon_term in obj.set_of_hit_terms:
            try:
                results_dict[canon_term].append(pmcid)
            except KeyError:
                results_dict[canon_term] = [pmcid]

    with open(output_file, 'wb') as output_file:
        pickle.dump(results_dict, output_file, pickle.HIGHEST_PROTOCOL)

    print(results_dict)

    current_file = axis_input_dirs[i]
    print(current_file)
