import pickle
from os import listdir

from AnnotatedArticle import AnnotatedArticle
from machine_learning_tests.helper_functions import get_all_files

if __name__ == "__main__":
    for directory in listdir("/data/GeneTag_over90_canonical/Pickled/"):
        for file in get_all_files("/data/GeneTag_over90_canonical/Pickled/" + directory):
            lingpipe_ann = AnnotatedArticle.copy(pickle.load(open(file, "rb")))
            with open(file.replace(".pkl", ".txt").replace("Pickled", "Text Files"), "w") as outfile:
                for key, value in lingpipe_ann.counter_of_hit_terms.items():
                    outfile.write((key + " ") * value)
