from os import listdir
import os.path as path
from AnnotatedArticle import AnnotatedArticle
from collections import defaultdict
import pickle


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]

if __name__ == "__main__":
    file_path = input("Input folder path: ")
    files = get_all_files(file_path)
    inverted_index = defaultdict(list)
    id_counter = 0
    for file in files:
        id_counter += 1
        with open(file, "rb") as infile:
            obj_data = pickle.load(infile)
            ann_art = AnnotatedArticle.copy(obj_data)
            for annotation in ann_art.set_of_hit_terms:
                inverted_index[annotation].append(id_counter)
    occurrence_rates = []
    for key, val in inverted_index.items():
        appearance_precentage = (len(val) / id_counter) * 100
        occurrence_rates.append((key, appearance_precentage))
    occurrence_rates.sort(key=lambda x: x[1])
    for item in occurrence_rates:
        print(item)
