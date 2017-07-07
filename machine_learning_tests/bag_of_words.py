from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from os import listdir
from timeit import default_timer
import os.path as path
import pickle


def pickle_or_doc_input(prompt):
    return True if input(prompt) == "pkl" else False


def get_list_from_pickle():
    pkl = pickle.load(open(input("Give file path for pkl to open: "), "rb"))
    return [item[1] for item in pkl]


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]


if __name__ == "__main__":
    # Get file names of training and random sets, vectorizers can read these in themselves
    training_list_is_pickle = pickle_or_doc_input(
        "Is training data input from pickle or directory? (pkl/dir): "
    )
    if training_list_is_pickle:
        training_text_files = get_list_from_pickle()
    else:
        training_text_files = get_all_files(input("Input path to directory of training data: "))
    random_list_is_pickle = pickle_or_doc_input(
        "Is random data input from pickle or directory? (pkl/dir): "
    )
    if random_list_is_pickle:
        random_text_files = get_list_from_pickle()
    else:
        random_text_files = get_all_files(input("Input path to directory of random irrelevant data: "))

    print(training_text_files[:5], len(training_text_files))
    print(random_text_files[:5], len(random_text_files))

    # ACTUAL MACHINE LEARNING CODE STARTS HERE
    all_files = training_text_files + random_text_files
    # Generate label group of 1's and 0's for training data
    labels = [1 for i in range(len(training_text_files))] + [0 for i in range(len(random_text_files))]
    # Basic vectorizer with accent stripping and stop word filters
    basic_vectorizer = TfidfVectorizer(input="filename", strip_accents="unicode", stop_words="english")
    print("start tfidf vectorizer")
    start = default_timer()
    tf_idf_features = basic_vectorizer.fit_transform(all_files)
    stop = default_timer()
    print("end tfidf vectorizer")
    print("'Time to vectorize:", (stop - start) / 60)
    joblib.dump(tf_idf_features, "/home/daniel/Downloads/PickleFiles/Sklearn_FeatureVectors/"
                + input("Give file name for desired fv pickle file name: "))
    clf = MultinomialNB()
    clf_svm = SVC()
    clf_knn = KNeighborsClassifier()
    start = default_timer()
    print("start cross validation")
    scores = cross_val_score(clf, tf_idf_features, labels,
                             scoring="roc_auc", cv=5, n_jobs=-1,
                             )
    stop = default_timer()
    print("stop cross validation")
    auc = sum(scores) / len(scores)
    print("Time elapsed for cross validation:", (stop - start) / 60)
    print("AUROC:", auc)
    start = default_timer()
    print("start fit")
    clf.fit(tf_idf_features, labels)
    stop = default_timer()
    print("end fit")
    print("Time elapsed for fit:", (stop - start) / 60)
    joblib.dump(clf, "/home/daniel/Downloads/PickleFiles/Sklearn_Classifiers/"
                + input("Give file name for desired clf pickle file name: "))
