import pickle
from sklearn.externals import joblib
import configparser
import sys
import numpy as np
import math

try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers


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
        open(helpers.replace_pathvar_with_environ("$STORE/kinase_canonical_to_nxtprot_id.pkl"), "rb")
    )
    classifier, transformer = joblib.load(arguments["classifier_path"])
    with open(arguments["out_path"], "w") as outfile:
        in_dict = pickle.load(open(arguments["possible_matches"], "rb"))
        if arguments["training_method"] == "BOW":
            for kinase, doc_set in in_dict.items():
                features = transformer.transform(
                    [arguments["document_path"] + doc_id + ".txt" for doc_id in doc_set]
                )
                print(features)
                predictions = classifier.decision_function(features)
                print(predictions)
                for i in range(predictions.shape[0]):
                    print(doc_set[i], features[i], predictions[i])
                result = [(doc_set[i], features[i], predictions[i]) for i in range(predictions.shape[0])]
                print(result[:5], flush=True)
                result = scale(result)
                print(result[:5], flush=True)
                result = sorted(result, reverse=True, key=lambda x: x[1])
                print(result[:5], flush=True)
                count = 0
                for item in result:
                    if count == 100:
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
                features = [x[1] for x in doc_set]
                print(features)
                features = transformer.transform(np.array(features))
                print(features)
                predictions = classifier.decision_function(features)
                print(predictions)
                for i in range(predictions.shape[0]):
                    print(doc_set[i], features[i], predictions[i])
                result = [(doc_set[i], features[i], predictions[i]) for i in range(predictions.shape[0])]
                print(result[:5], flush=True)
                result = scale(result)
                print(result[:5], flush=True)
                result = sorted(result, reverse=True, key=lambda x: x[1])
                print(result[:5], flush=True)
                count = 0
                for item in result:
                    if count == 100:
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
