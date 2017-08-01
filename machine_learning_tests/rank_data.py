import pickle
from sklearn.externals import joblib
import configparser
import sys
from multiprocessing import Pool
import numpy as np
import math

try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers


def docprop_ranking(param_tup):
    doc_id = param_tup[0][0]
    doc_features = param_tup[0][1]
    transf = param_tup[1]
    clf = param_tup[2]
    print(doc_features)
    features = transf.transform(np.array(doc_features))
    features = features.reshape(1, -1)
    print(features)
    if clf.predict(features)[0] == 1:
        print("!!!", flush=True)
    if arguments["classifier_type"] == "SVM":
        print(doc_id, clf.predict_proba(features), clf.predict(features), flush=True)
        return doc_id, clf.predict_proba(features)[0][1], clf.predict(features)
    else:
        print(doc_id, clf.decision_function(features), clf.predict(features), flush=True)
        return doc_id, clf.decision_function(features)[0], clf.predict(features)


def bow_ranking(param_tup):
    doc_id = param_tup[0]
    transf = param_tup[1]
    clf = param_tup[2]
    print(transf, clf.classes_)
    features = transf.transform([arguments["document_path"] + doc_id + ".txt"])
    if clf.predict(features) == 1:
        print("!!!", flush=True)
    if arguments["classifier_type"] == "SVM":
        return doc_id, clf.predict_proba(features)[0][1], clf.predict(features)
    else:
        return doc_id, clf.decision_function(features)[0], clf.predict(features)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def scale(result_list):
    return [(x[0], sigmoid(x[1]), x[2]) for x in result_list]
    # scaled_result = []
    # score_array = np.array([res[1] for res in result_list])
    # scaled = (score_array-np.min(score_array))/np.ptp(score_array)
    # scaled = scaled.tolist()
    # for i in range(len(scaled)):
    #     scaled_result.append((result_list[i][0], scaled[i], result_list[i][2]))
    # return scaled_result

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    arguments = config[sys.argv[2]]
    for key in arguments:
        arguments[key] = helpers.replace_pathvar_with_environ(arguments[key])
    canon_to_id = pickle.load(
        open(
            helpers.replace_pathvar_with_environ("$STORE/kinase_canonical_to_nxtprot_id.pkl"), "rb"
        )
    )
    classifier, transformer = joblib.load(arguments["classifier_path"])
    print(classifier, transformer)
    with open(arguments["out_path"], "w") as outfile:
        in_dict = pickle.load(open(arguments["possible_matches"], "rb"))
        if arguments["training_method"] == "BOW":
            for kinase, doc_set in in_dict.items():
                print(kinase, doc_set[:5])
                with Pool() as p:
                    result = p.map(bow_ranking, [(doc, transformer, classifier) for doc in doc_set])
                    print(result[:5], flush=True)
                if arguments["classifier_type"] != "SVM":
                    result = scale(result)
                    print(result[:5], flush=True)
                result = sorted(result, reverse=True, key=lambda x: x[1])
                print(result[:5], flush=True)
                count = 0
                for item in result:
                    if count == 30:
                        break
                    count += 1
                    outfile.write(
                        " ".join(
                            [
                                canon_to_id[kinase],
                                "dummy",
                                item[0],
                                str(count),
                                str(round(item[1] * 100, 2)),
                                arguments["run_id"],
                                "\n"
                            ]
                        )
                    )
                break
        else:
            for kinase, values in in_dict.items():
                print(values[:5], flush=True)
                doc_set = [(value[0], value[1:]) for value in values]
                print(doc_set[:5], flush=True)
                fvs = [x[1] for x in values]
                fvs = transformer.transform(np.array(fvs))
                print(classifier.predict(fvs))
                print(classifier.predict_proba(fvs))
                with Pool() as p:
                    result = p.map(docprop_ranking, [(val, transformer, classifier) for val in doc_set])
                    print(result[:5], flush=True)
                if arguments["classifier_type"] != "SVM":
                    result = scale(result)
                    print(result[:5], flush=True)
                result = sorted(result, reverse=True, key=lambda x: x[1])
                print(result[:5], flush=True)
                count = 0
                for item in result:
                    if count == 30:
                        break
                    count += 1
                    outfile.write(
                        " ".join(
                            [
                                canon_to_id[kinase],
                                "dummy", item[0],
                                str(count),
                                str(round(item[1] * 100, 2)),
                                arguments["run_id"],
                                "\n"
                            ]
                        )
                    )
                    print(" ".join(
                        [
                            canon_to_id[kinase],
                            "dummy", item[0],
                            str(count),
                            str(round(item[1] * 100, 2)),
                            arguments["run_id"],
                            "\n"
                        ]
                    ), flush=True)
                break
