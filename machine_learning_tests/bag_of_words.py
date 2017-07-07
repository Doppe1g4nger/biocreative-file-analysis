from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from os import listdir
from timeit import default_timer
import os.path as path
import pickle


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]

if __name__ == "__main__":
    # Get file names of training and random sets, vectorizers can read these in themselves
    training_list_is_pickle = True if input(
        "Is training data input from pickle or directory? (pkl/dir): "
    ) == "pkl" else False
    if training_list_is_pickle:
        pkl = pickle.load(open(input("Give file path for pkl to open: "), "rb"))
        training_text_files = [item[1] for item in pkl]
    else:
        training_text_files = get_all_files(input("Input path to directory of training data: "))
    random_list_is_pickle = True if input(
        "Is random data input from pickle or directory? (pkl/dir): "
    ) == "pkl" else False
    if random_list_is_pickle:
        pkl = pickle.load(open(input("Give file path for pkl to open: "), "rb"))
        random_text_files = [item[1] for item in pkl]
    else:
        random_text_files = get_all_files(input("Input path to directory of random irrelevant data: "))
    all_files = training_text_files + random_text_files
    # Generate label group of 1's and 0's for training data
    labels = [1 for i in range(len(training_text_files))] + [0 for i in range(len(random_text_files))]
    # Basic vectorizer with accent stripping and stop word filters
    basic_vectorizer = CountVectorizer(input="filename", strip_accents="unicode", stop_words="english")
    features = basic_vectorizer.fit_transform(all_files).toarray()
    tfidf = TfidfTransformer()
    tf_idf_features = tfidf.fit_transform(features).toarray()
    clf = MultinomialNB()
    start = default_timer()
    scores = cross_val_score(clf, tf_idf_features, labels,
                             scoring="roc_auc", cv=5, n_jobs=-1,
                             )
    stop = default_timer()
    auc = sum(scores) / len(scores)
    print("Time elapsed for cross validation:", (stop - start) / 60)
    print("AUROC:", auc)
    start = default_timer()
    clf.fit(tf_idf_features, labels)
    stop = default_timer()
    print("Time elapsed for fit:", (stop - start) / 60)
    joblib.dump(clf, "/home/daniel/Downloads/PickleFiles/Sklearn_Classifiers/"
                + input("Give file name for desired pickle file name: "))
