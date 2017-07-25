import configparser
import pickle
import sys
from timeit import default_timer
import numpy as np

from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers

if __name__ == "__main__":
    # Read in ini formatted config file passed as command line argument, replace path shortening variables
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    arguments = config[sys.argv[2]]
    for key in arguments:
        arguments[key] = helpers.replace_pathvar_with_environ(arguments[key])
    # Extract triple of arrays from pickled docs, use doc_id for bag of words, fv_array for doc_prop vector    
    labels, fv_array, doc_ids = pickle.load(open(arguments["feature_vector"], "rb"))
    parameters = {}
    pipeline_input = []
    # Select between training method, set parameters and pipeline input for each option
    if arguments["training_method"] == "BOW":
        features = [arguments["document_path"] + idx + ".txt" for idx in doc_ids]
        pipeline_input.append(("tfidf_vect", TfidfVectorizer()))
        parameters.update({
            "tfidf_vect__input": ["filename"],
            "tfidf_vect__strip_accents": [None, "unicode"],
            "tfidf_vect__ngram_range": [(1, 1), (1, 2), (1, 3)],
            "tfidf_vect__stop_words": [None, "english"],
            "tfidf_vect__max_df": [x / 10 for x in range(2, 11, 2)],
            "tfidf_vect__norm": ["l1", "l2", None],
            "tfidf_vect__sublinear_tf": [True]
        })
    elif arguments["training_method"] == "DOCPROP":
        features = np.array(fv_array)
        pipeline_input.append(("pre", Normalizer()))
        parameters.update({
            "pre__norm": ["l1", "l2", "max"]
        })
    else:
        raise ValueError("Invalid training_method argument specified in config")
    # Select among classifiers and set their parameters for GridSearchCV
    if arguments["classifier"] == "SVM":
        clf = SVC()
        parameters = {
            "clf__probability": [True],
            "clf__coef0": [0.5],
            "clf__cache_size": [5000.0],
            "clf__C": [0.01, 0.1, 1.0, 10.0, 100.0],
            "clf__degree": [1, 2, 3],
            "clf__kernel": ["rbf", "poly"],
            "clf__class_weight": ["balanced", None],
        }
    elif arguments["classifier"] == "MNNB":
        clf = MultinomialNB()
        parameters = {
            "clf__alpha": [0, 1.0, 0.1, 10.0, 5.0],
            "clf__fit_prior": [True, False],
        }
    elif arguments["classifier"] == "KNN":
        clf = KNeighborsClassifier()
        parameters = {
            "clf__n_neighbors": [3, 5, 10],
            "clf__weights": ["uniform", "distance"],
            "clf__algorithm": ["ball_tree", "kd_tree", "brute"],
            "clf__p": [1, 2, 3, 4],
            "clf__n_jobs": [-1],
        }
    else:
        raise ValueError("unsupported classifier argument given")
    pipeline_input.append(("clf", clf))
    pipe = Pipeline(pipeline_input)
    start = default_timer()
    inner_cv = StratifiedKFold(shuffle=True)
    outer_cv = StratifiedKFold(shuffle=True)
    grid_search = GridSearchCV(
        estimator=pipe,
        param_grid=parameters,
        cv=inner_cv,
        scoring="roc_auc",
        n_jobs=-1,
        verbose=2,
        pre_dispatch=20,
    )
    grid_search.fit(features, labels)
    nested_score = cross_val_score(
        estimator=clf,
        X=features,
        y=labels,
        cv=outer_cv,
        scoring="roc_auc",
        n_jobs=-1,
    )
    end = default_timer()
    print(grid_search)
    print(grid_search.best_estimator_)
    print(str((end - start) / 60))
    print(grid_search.best_score_, nested_score.mean(), grid_search.best_score_ - nested_score)
    print(grid_search.best_params_)
    joblib.dump(grid_search, arguments["classifier_path"])
