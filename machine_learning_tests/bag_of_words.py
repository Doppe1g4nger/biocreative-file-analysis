from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.svm import SVC
from timeit import default_timer
import helper_functions as helpers
import configparser
import pickle
import sys


def get_set_from_pickle(f_path):
    pkl = pickle.load(open(f_path, "rb"))
    return set([item[0] for item in pkl])


if __name__ == "__main__":
    # Read in ini formatted config file passed as command line argument
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    arguments = config["DEFAULT"]
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
    print(training_text_files[:5], len(training_text_files))
    print(random_text_files[:5], len(random_text_files))

    all_files = training_text_files + random_text_files
    # Generate label group of 1's and 0's for training data
    labels = [1 for i in range(len(training_text_files))] + [0 for i in range(len(random_text_files))]
    if arguments["preexisting_fv_path"]:
        tf_idf_features = joblib.load(arguments["preexisting_fv_path"])
        fv_path = arguments["preexisting_fv_path"]
    else:
        if not arguments["new_fv_path"]:
            raise ValueError(
                "No preexisting or new feature vector file paths have been given in {} .".format(sys.argv[1])
            )
        fv_path = arguments["new_fv_path"]
        basic_vectorizer = TfidfVectorizer(
            input="filename", strip_accents="unicode", stop_words="english"
        )
        start = default_timer()
        tf_idf_features = basic_vectorizer.fit_transform(all_files)
        stop = default_timer()
        joblib.dump(basic_vectorizer, arguments["vectorizer"])
        joblib.dump(tf_idf_features, arguments["new_fv_path"])
        time_to_vectorize = (stop - start) / 60
        helpers.send_email(
            sender="danieldopp@outlook.com",
            password=arguments["email_pass"],
            receivers=["danieldopp@outlook.com"],
            subject=fv_path.split("/")[-1] + " Finished Processing",
            message="Processing completed in {num_mins} minutes".format(num_mins=time_to_vectorize),
        )
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
