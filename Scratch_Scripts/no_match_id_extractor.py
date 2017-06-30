import pickle
from AnnotatedArticle import AnnotatedArticle
from os import listdir
import os.path as path


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]

if __name__ == "__main__":
    count = 0
    for file in get_all_files(input("Input path to Annotated Article pickles: ")):
        with open(file, "rb") as infile:
            article = AnnotatedArticle.copy(pickle.load(infile))
            if not article.number_of_hits:
                count += 1
                print(file.split("/")[-1].strip(".txt.xmi.pkl"))
    print(count)
