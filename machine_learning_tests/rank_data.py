from sklearn.externals import joblib
import numpy as np
import pickle
import configparser
import sys
import math

try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers


def sigmoid_scale(x):
    return 1 / (1 + math.exp(-x))


def scale(result_list):
    scaled_result = []
    score_array = np.array([res[1] for res in result_list])
    scaled = (score_array-np.min(score_array))/np.ptp(score_array)
    scaled = scaled.tolist()
    for i in range(len(scaled)):
        scaled_result.append((result_list[i][0], scaled[i], result_list[i][2]))
    return scaled_result

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    arguments = config[sys.argv[2]]
    print(sys.argv[2], flush=True)
    for key in arguments:
        arguments[key] = helpers.replace_pathvar_with_environ(arguments[key])
    canon_to_id = pickle.load(
        open(helpers.replace_pathvar_with_environ("$STORE/kinase_canonical_to_nxtprot_id.pkl"), "rb")
    )
    classifier, transformer = joblib.load(arguments["classifier_path"])
    print(classifier, transformer, flush=True)
    with open(arguments["out_path"], "w") as outfile:
        in_dict = pickle.load(open(arguments["possible_matches"], "rb"))
        kin_count = 0
        for kinase, fvs in in_dict.items():
            kin_count += 1
            if arguments["training_method"] == "BOW":
                features = transformer.transform(
                    [arguments["document_path"] + doc_id + ".txt" for doc_id in fvs]
                )
                doc_ids = fvs.copy()
            else:
                doc_ids = [value[0] for value in fvs]
                features = [value[1:] for value in fvs]
                features = transformer.transform(np.array(features))
            confidence = classifier.decision_function(features)
            predictions = classifier.predict(features)
            result = [
                (doc_ids[i], sigmoid_scale(confidence[i]), predictions[i]) for i in range(predictions.shape[0])
            ]
            result = sorted(result, reverse=True, key=lambda x: x[1])
            count = 0
            for item in result:
                if count == 1000:
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
            if not kin_count % 10:
                print(kin_count, flush=True)
