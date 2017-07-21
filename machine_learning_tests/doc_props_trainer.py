import configparser
import pickle
import sys
from timeit import default_timer
import numpy as np

from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
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
    labels, features = pickle.load(open(arguments["feature_vector"], "rb"))
    print(labels, features)
    features = np.array(features)
    if arguments["classifier"] == "SVM":
        clf = SVC()
        parameters = {
            "probability": [True],
            "C": [0.01, 0.1, 1.0, 10.0, 100.0],
            # "kernel": ["poly", "rbf", "sigmoid"],
            # "degree": [1, 2, 3, 4, 5],
            "kernel": ["rbf", "sigmoid"],
            "coef0": [0.0, 0.1, 0.5, 0.7, 1.0],
            "shrinking": [True, False],
            "class_weight": ["balanced", None]
        }
    elif arguments["classifier"] == "MNNB":
        clf = MultinomialNB()
        parameters = {
            "clf__alpha": [0, 1.0, 0.1, 10.0, 5.0],
            "clf__fit_prior": [True, False]
        }
    elif arguments["classifier"] == "KNN":
        clf = KNeighborsClassifier()
        parameters = {
            "clf__n_neighbors": [3, 5, 10],
            "clf__weights": ["uniform", "distance"],
            "clf__algorithm": ["ball_tree", "kd_tree", "brute"],
            "clf__p": [1, 2, 3, 4],
            "clf__n_jobs": [-1]
        }
    else:
        raise ValueError("unsupported classifier argument given")
    start = default_timer()
    grid_search = GridSearchCV(
        estimator=clf,
        param_grid=parameters,
        scoring="roc_auc",
        n_jobs=-1,
        refit=True,
        verbose=2,
        error_score=0
    )
    grid_search.fit(features, labels)
    end = default_timer()
    print(grid_search)
    print(grid_search.best_estimator_)
    print(str((end - start) / 60))
    print(grid_search.cv_results_)
    print(grid_search.best_score_)
    print(grid_search.best_params_)
    print(grid_search.scorer_)
    print(grid_search.n_splits_)
    joblib.dump(grid_search, arguments["classifier_path"])
