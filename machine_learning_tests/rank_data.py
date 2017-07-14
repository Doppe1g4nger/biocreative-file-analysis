import pickle
from sklearn.externals import joblib
import configparser
import sys
from multiprocessing import Pool

try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers


def run_ranking(param_tup):
    features = param_tup[1].transform([arguments["doc_source"] + param_tup[0] + ".txt"])
    if param_tup[2] is not None:
        features = param_tup[2].transform(features)
    return param_tup[0], param_tup[3].predict_proba(features)[0][1], param_tup[3].predict(features)

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
    vectorizer, transformer = joblib.load(arguments["vectorizer"])
    classifier = joblib.load(arguments["classifier"])
    with open(arguments["out_path"], "w") as outfile:
        in_dict = pickle.load(open(arguments["possible_matches"], "rb"))
        for kinase, doc_set in in_dict.items():
            with Pool() as p:
                result = p.map(run_ranking, [(doc, vectorizer, transformer, classifier) for doc in doc_set])
            result = sorted(result, reverse=True, key=lambda x: x[1])
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
                            str(item[1] * 100),
                            arguments["runid"],
                            "\n"
                        ]
                    )
                )
