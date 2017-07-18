import configparser
import pickle
import sys
from timeit import default_timer

from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers


def get_set_from_pickle(f_path):
    pkl = pickle.load(open(f_path, "rb"))
    return set([item[0] for item in pkl])

if __name__ == "__main__":
    # Read in ini formatted config file passed as command line argument
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    arguments = config[sys.argv[2]]
    for key in arguments:
        arguments[key] = helpers.replace_pathvar_with_environ(arguments[key])
    # Get file names of training and random sets, vectorizers can read these in themselves
    if arguments["training_pkl"]:
        training_id_set = get_set_from_pickle(arguments["training_pkl"])
        training_text_files = [
            file for file in helpers.get_all_files(arguments["training_source"])
            if file.split("/")[-1].strip(".txt") in training_id_set
        ]
    else:
        training_text_files = helpers.get_all_files(arguments["training_source"])
    if arguments["random_pkl"]:
        random_id_set = get_set_from_pickle(arguments["random_pkl"])
        random_text_files = [
            file for file in helpers.get_all_files(arguments["random_source"])
            if file.split("/")[-1].strip(".txt") in random_id_set
        ]
    else:
        random_text_files = helpers.get_all_files(arguments["random_source"])

    # random_text_files = [file for file in random_text_files if file not in training_text_files]
    # print(len(random_text_files))
    # print(training_text_files[:5], len(training_text_files))
    # print(random_text_files[:5], len(random_text_files))

    all_files = training_text_files + random_text_files
    # Generate label group of 1's and 0's for training data
    labels = [1 for i in range(len(training_text_files))] + [0 for i in range(len(random_text_files))]

    vect = CountVectorizer(input="filename")
    transf = TfidfTransformer()
    parameters = {
        "vect__strip_accents": [None, "unicode", "ascii"],
        "vect__ngram_range": [(1, 1), (1, 2), (2, 2), (1, 3), (2, 3), (3, 3)],
        "vect__stop_word": [None, "english"],
        "vect__lowercase": [True, False],
        "vect__max_df": [x / 10 for x in range(1, 11)],
        "vect__binary": [True, False],
        "transf__norm": ["l1", "l2", None],
        "transf__use_idf": [True, False],
        "transf__smooth_idf": [True, False],
        "transf__sublinear_tf": [True, False]
    }
    if arguments["classifier"] == "SVM":
        clf = SVC()
        parameters.update({
            "clf__C": [0.1, 1.0, 10.0],
            "clf__kernel": ["linear", "poly", "rbf", "sigmoid", "precomputed"],
            "clf__probability": [True],
            "clf__degree": [1, 2, 3, 4, 5],
            "clf__coef0": [0.0, 0.1, 0.5, 0.7, 1.0],
            "clf__shrinking": [True, False],
        })
    elif arguments["classifier"] == "MNNB":
        clf = MultinomialNB()
        parameters.update({
            "clf__alpha": [0, 1.0, 0.1, 10.0, 5.0],
            "clf__fit_prior": [True, False]
        })
    elif arguments["classifier"] == "KNN":
        clf = KNeighborsClassifier()
        parameters.update({
            "clf__n_neighbors": [3, 5, 10],
            "clf__weights": ["uniform", "distance"],
            "clf__algorithm": ["ball_tree", "kd_tree", "brute"],
            "clf__p": [1, 2, 3, 4],
            "clf_n_jobs": [-1]
        })
    else:
        raise ValueError("unsupported classifier argument given")
    pipe = Pipeline([
        ("vect", vect),
        ("transf", transf),
        ("clf", clf)
    ])
    start = default_timer()
    grid_search = GridSearchCV(pipe, parameters, scoring="roc_auc", n_jobs=-1, refit=True, cv=5)
    grid_search.fit(all_files, labels)
    end = default_timer()
    print(grid_search.cv_results_, grid_search, str((end - start) / 60))
    joblib.dump(grid_search.best_estimator_, arguments["classifier"])
