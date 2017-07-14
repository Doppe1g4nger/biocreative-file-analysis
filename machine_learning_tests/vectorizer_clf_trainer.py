import configparser
import copy
import multiprocessing
import pickle
import sys
from timeit import default_timer

from scipy.sparse import vstack
from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import helper_functions as helpers


def get_set_from_pickle(f_path):
    pkl = pickle.load(open(f_path, "rb"))
    return set([item[0] for item in pkl])


if __name__ == "__main__":
    # Read in ini formatted config file passed as command line argument
    config = configparser.ConfigParser()
    config.read(
        "/home/ddopp/biocreative-file-analysis/machine_learning_tests/config.ini"
    )
    arguments = config[sys.argv[1]]
    for key in arguments:
        arguments[key] = helpers.replace_pathvar_with_environ(arguments[key])
    if arguments["preexisting_fv_path"]:
        labels, tf_idf_features = joblib.load(arguments["preexisting_fv_path"])
        fv_path = arguments["preexisting_fv_path"]
    else:
        if not arguments["new_fv_path"]:
            raise ValueError(
                "No preexisting or new feature vector file paths have been given in {} config.".format(sys.argv[1])
            )
        fv_path = arguments["new_fv_path"]
        # Get file names of training and random sets, vectorizers can read these in themselves
        if arguments["training_type"] == "pkl":
            training_id_set = get_set_from_pickle(arguments["training_pkl"])
            training_text_files = [
                file for file in helpers.get_all_files(arguments["training_source"])
                if file.split("/")[-1].strip(".txt") in training_id_set
            ]
        else:
            training_text_files = helpers.get_all_files(arguments["training_source"])
        if arguments["random_type"] == "pkl":
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
        if arguments.getboolean('use_hashing'):
            vectorizer = HashingVectorizer(
                input="filename", strip_accents="unicode", stop_words="english", n_features=2**20,
                non_negative=True

            )
            start_h = default_timer()
            with multiprocessing.Pool() as p:
                feature_list = p.map(vectorizer.fit_transform, [[file] for file in all_files])
                features = vstack(feature_list)
            stop_h = default_timer()
            tfidf = TfidfTransformer()
            start = default_timer()
            tf_idf_features = tfidf.fit_transform(features)
            stop = default_timer()
            joblib.dump((vectorizer, tfidf), arguments["vectorizer"])
            joblib.dump((labels, tf_idf_features), arguments["new_fv_path"])
            time_to_hash = (stop_h - start_h) / 60
            time_to_tfidf = (stop - start) / 60
            helpers.send_email(
                sender="danieldopp@outlook.com",
                password=arguments["email_pass"],
                receivers=["danieldopp@outlook.com"],
                subject=fv_path.split("/")[-1] + " Finished Processing",
                message="Processing completed in {num_mins} minutes".format(num_mins=time_to_tfidf + time_to_hash)
                        + "\nTime to Hash: {hash_time}".format(hash_time=time_to_hash)
                        + "\nTime to TFIDF: {tfidf_time}".format(tfidf_time=time_to_tfidf),

            )
        else:
            vectorizer = TfidfVectorizer()
            start = default_timer()
            tf_idf_features = vectorizer.fit_transform(all_files)
            stop = default_timer()
            joblib.dump((vectorizer, None), arguments["vectorizer"])
            joblib.dump((labels, tf_idf_features), arguments["new_fv_path"])
            time_to_tfidf = (stop - start) / 60
            helpers.send_email(
                sender="danieldopp@outlook.com",
                password=arguments["email_pass"],
                receivers=["danieldopp@outlook.com"],
                subject=fv_path.split("/")[-1] + " Finished Processing",
                message="Processing completed in {num_mins} minutes".format(num_mins=time_to_tfidf)
                        + "\nTime to TFIDF: {tfidf_time}".format(tfidf_time=time_to_tfidf),

            )
        arguments["preexisting_fv_path"] = copy.deepcopy(arguments["new_fv_path"])
        arguments["new_fv_path"] = ""
        with open("/home/ddopp/biocreative-file-analysis/machine_learning_tests/config.ini", "w") as config_file:
            config.write(config_file)
    # for var in dir():
    #     exec('print(var, sys.getsizeof(' + var + ", -1))")
    classifiers = [
        ("MNNB", MultinomialNB()),
        ("SVM", SVC(probability=True)),
        ("KNN", KNeighborsClassifier()),
    ]
    for clf_name, clf in classifiers:
        start = default_timer()
        scores = cross_val_score(
            clf, tf_idf_features, labels,
            scoring="roc_auc", cv=5, n_jobs=-1,
        )
        stop = default_timer()
        cross_val_time = (stop - start) / 60
        auroc = sum(scores) / len(scores)
        start = default_timer()
        clf.fit(tf_idf_features, labels)
        stop = default_timer()
        fit_time = (stop - start) / 60
        joblib.dump(clf, arguments["new_" + clf_name + "_classifier_path"])
        helpers.send_email(
            sender="danieldopp@outlook.com",
            password=arguments["email_pass"],
            receivers=["danieldopp@outlook.com"],
            subject="{clf_name} Finished Processing for {vec}".format(clf_name=clf_name, vec=fv_path.split("/")[-1]),
            message="cross_val completed in {num_mins} minutes.\n".format(num_mins=cross_val_time)
                    + "fit completed in {num_mins} minutes.\n".format(num_mins=fit_time)
                    + "AUROC: {auroc}".format(auroc=auroc),
        )
