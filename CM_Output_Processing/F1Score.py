# AA_to_F1Score
import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle

kinase_input_dir = '/data/CM_output/Comparison_FT/Kinases/Combined/Post-Processed/DictCompare/DIS_W_SAMAO'
axis_input_dirs = ['/data/CM_output/Comparison_FT/Ontologies/Combined/Post-Processed/DIS/NCIT-Restricted', '/data/CM_output/Comparison_FT/Ontologies/Combined/Post-Processed/DIS/HP']
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

temp_count = 0
temp = ''
for filename in os.listdir(kinase_input_dir):
    obj = load_obj(kinase_input_dir + "/" + filename)
    if obj.number_of_hits > 0:
        kinase_list.append(filename)


for i in range(0, len(axis_input_dirs)):
    axis_list = []
    pred_positives = {}
    counter = 0
    print("\n\n")
    temp_count = 0
    for filename in os.listdir(axis_input_dirs[i]):
        counter += 1
        obj = load_obj(axis_input_dirs[i] + "/" + filename)
        if obj.number_of_hits > 0:
            axis_list.append(filename)
        pmcid = filename.strip('.txt.xmi.pkl')
        if pmcid in temp:
            temp_count += 1

    print("TEMP: " + str(temp_count))

    overlap_list = [elem for elem in axis_list if elem in kinase_list]

    current_file = axis_input_dirs[i]
    print(current_file)

    TP = 0
    FP = 0

    for filename in overlap_list:
        pmcid = filename.strip('.txt.xmi.pkl')
        TP_found = False
        obj = load_obj(kinase_input_dir + "/" + filename)
        for canon_term in obj.set_of_hit_terms:
            try:
                if pmcid in labeled_positives[canon_term]:
                    TP += 1
                    TP_found = True
                    break
            except KeyError:
                pass
        if not TP_found:
            FP += 1

    num_articles = counter // 2
    print("TP:\tFN:\tFP:\tTN:")
    print(str(TP) + "\t" + str(num_articles - TP) + "\t" + str(FP) + "\t" + str(num_articles - FP))
