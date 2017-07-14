import pickle

from helper_functions import get_all_files

if __name__ == "__main__":
    full_training = set()
    set_of_tups_tr = set()
    set_of_tups_irr = set()
    labeled_positives_dir = '/data/TrainingCanonicalNames_ToDocID_dicts/DIS_ft_train_canon_to_docid_dict.pkl'
    dict_of_sets = pickle.load(open(labeled_positives_dir, "rb"))
    for s in dict_of_sets.values():
        full_training.update(s)
    for file in get_all_files("/data/CM_input/FullText/FullText_All_Combined_DIS"):
        if file.split("/")[-1].strip(".txt") in full_training:
            set_of_tups_tr.add((file.split("/")[-1].strip(".txt"), file))
        else:
            set_of_tups_irr.add((file.split("/")[-1].strip(".txt"), file))
    print(len(set_of_tups_tr), set_of_tups_tr)
    print(len(set_of_tups_irr), set_of_tups_irr)
    while len(set_of_tups_irr) != len(set_of_tups_tr):
        set_of_tups_irr.pop()
    with open("/home/daniel/Downloads/PickleFiles/set_of_docid_filepath_tuples/"
              + "ft_training_dis_relevant" + ".pkl", "wb") as f:
        pickle.dump(set_of_tups_tr, f)
    with open("/home/daniel/Downloads/PickleFiles/set_of_docid_filepath_tuples/"
                      + "ft_training_dis_irrelevant" + ".pkl", "wb") as f:
        pickle.dump(set_of_tups_irr, f)
