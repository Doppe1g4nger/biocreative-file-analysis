import configparser
import pickle
import sys
from timeit import default_timer
import numpy as np

from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_val_score, KFold
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline

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
    print(labels[:10])
    print(features[:10])
    features = np.array(features)
    if arguments["classifier"] == "SVM":
        clf = SVC(probability=True)
        parameters = {
            # "clf__C": [0.01, 0.1, 1.0, 10.0, 100.0],
            # "clf__degree": [1, 2, 3, 4, 5],
            # "clf__kernel": ["rbf", "sigmoid", "poly"],
            # "clf__coef0": [0.0, 0.1, 0.5, 0.7, 1.0],
            # "clf__shrinking": [True, False],
            # "clf__class_weight": ["balanced", None]
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
    pipe = Pipeline([
        ("pre", Normalizer(norm="l1")),
        ("clf", clf)
    ])
    start = default_timer()
    grid_search = None
    inner_cv = KFold(n_splits=4, shuffle=True)
    outer_cv = KFold(n_splits=4, shuffle=True)
    grid_search = GridSearchCV(
        estimator=pipe,
        param_grid=parameters,
        cv=inner_cv,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=2,
    )
    grid_search.fit(features, labels)
    nested_score = cross_val_score(estimator=clf, X=features, y=labels, cv=outer_cv).mean()
    end = default_timer()
    print(grid_search)
    print(grid_search.best_estimator_)
    print(str((end - start) / 60))
    print(grid_search.best_score_, nested_score, grid_search.best_score_ - nested_score)
    print(grid_search.best_params_)
    print(grid_search.n_splits_)
    joblib.dump(grid_search, arguments["classifier_path"])
