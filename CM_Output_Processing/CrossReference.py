# AA_to_F1Score
import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle

kinase_input_dir = '/data/CM_output/FT/Post-Processed/All/Kinase_BP_Test'
axis_input_dirs = ['/data/CM_output/FT/Post-Processed/All/GO-old']
output_file = '/data/CM_output/FT/Post-Processed/All/FT_All_TestSet_GO.pkl'
labeled_positives_dir = '/data/TrainingCanonicalNames_ToDocID_dicts/DIS_ft_train_canon_to_docid_dict.pkl'
#del axis_input_dirs[0]
kinase_list = []
axis_list = []
total_positives = 0


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

labeled_positives = load_obj(labeled_positives_dir)
print("LP:" + str(labeled_positives))

kcount = 0

for filename in os.listdir(kinase_input_dir):
    obj = load_obj(kinase_input_dir + "/" + filename)
    if obj.number_of_hits > 0:
        kinase_list.append(filename)
    kcount += 1
    if kcount % 1000 == 0:
        print("kinase " + str(kcount))


for i in range(0, len(axis_input_dirs)):
    axis_list = []
    pred_positives = {}
    counter = 0
    print("\n\n")
    temp_count = 0
    for filename in os.listdir(axis_input_dirs[i]):
        counter += 1
        if counter % 1000 == 0:
            print("axis " + str(counter))
        obj = load_obj(axis_input_dirs[i] + "/" + filename)
        if obj.number_of_hits > 0:
            axis_list.append(filename)


    print("TEMP: " + str(temp_count))

    overlap_list = [elem for elem in axis_list if elem in kinase_list]

    results_dict = {}
    for hit in overlap_list:



    with open(output_file, 'wb') as output_file:
        pickle.dump(overlap_list, output_file, pickle.HIGHEST_PROTOCOL)

    current_file = axis_input_dirs[i]
    print(current_file)

