from os import listdir
import os.path as path
from collections import defaultdict
from AnnotatedArticle import AnnotatedArticle
import pickle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter


def to_percent(x, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    return str(x) + "%"


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
            ann_obj = AnnotatedArticle.copy(obj_data)
            for annotation in ann_obj.set_of_hit_terms:
                inverted_index[annotation].append(id_counter)
    occurrence_rates = []
    for key, val in inverted_index.items():
        appearance_percentage = (len(val) / id_counter) * 100
        occurrence_rates.append((key, appearance_percentage))
    occurrence_rates.sort(key=lambda x: x[1], reverse=True)
    # word_list = []
    percent_list = []
    stop_percent = int(input("Input decimal percentage of desired term frequency: "))
    stop_word_file = input("Input file path to stop word output: ")
    # percent_categories = [0 for i in range(10)]
    with open(stop_word_file, "w") as outfile:
        for item in occurrence_rates:
            if item[1] < stop_percent:
                pass
            else:
                outfile.write(item[0] + "\n")
                # print(item)
            # percent_categories[int(item[1] // 10)] += 1  # Probably hella unsafe
            # word_list.append(item[0])
            percent_list.append(item[1])
    # percent_categories = np.array(percent_categories)
    # word_list = np.array(word_list)
    percent_list = np.array(percent_list)
    plt.hist(percent_list, bins=50, range=(0, 100))
    formatter = FuncFormatter(to_percent)
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.show()
