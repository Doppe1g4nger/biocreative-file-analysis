import AnnotatedArticle as aa
import pickle
import numpy as np
import scipy.stats as stats
import pylab as pl


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    prox_dictionary_loc = r"/data/CM_output/Abst/Post-Processed/Features/Abst_NCIT_Train_Feat.pkl"
    labeled_positives_loc = r'/data/TrainingCanonicalNames_ToDocID_dicts/DIS_abs_train_canon_to_docid_dict.pkl'
    output_pickle = r"/data/CM_output/Abst/Post-Processed/FV/Abst_NCIT_Train_FV.pkl"
    prox_dict = load_obj(prox_dictionary_loc)
    labeled_pos_dict = load_obj(labeled_positives_loc)
    features = []
    labels = []

    for kinase in prox_dict:
        for doc in prox_dict[kinase]:
            try:
                doc_id = doc[0][4:]
                if doc_id in labeled_pos_dict[kinase]:
                    labels.append(1)
                else:
                    labels.append(0)
                if len(labels) % 10000 == 0:
                    print(len(labels))
                features.append([doc[1], doc[2], doc[3], doc[4]])
            except KeyError:
                print("KeyError")

    fl_tuple = (labels, features)
    with open(output_pickle, 'wb') as output_file:
        pickle.dump(fl_tuple, output_file, pickle.HIGHEST_PROTOCOL)
