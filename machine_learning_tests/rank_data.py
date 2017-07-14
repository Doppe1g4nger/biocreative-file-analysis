import pickle
from sklearn.externals import joblib
import configparser
import sys
try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    arguments = config[sys.argv[2]]
    for key in arguments:
        arguments[key] = helpers.replace_pathvar_with_environ(arguments[key])
    canon_to_id = pickle.load(
        open(
            helpers.replace_pathvar_with_environ("$STORE/kinase_canonical_to_nxtprot_id.pkl"), "rb")
    )
    vectorizer, transformer = joblib.load(arguments["vectorizer"])
    classifier = joblib.load(arguments["classifier"])
    with open(arguments["out_path"], "w") as outfile:
        in_dict = pickle.load(open(arguments["possible_matches"], "rb"))
        for kinase, doc_set in in_dict.items():
            result = []
            for doc in doc_set:
                tf_idf_features = vectorizer.transform([arguments["doc_source"] + doc + ".txt"])
                if transformer is not None:
                    tf_idf_features = transformer.transform(tf_idf_features)
                result.append(
                    (doc, classifier.predict_proba(tf_idf_features)[0][1], classifier.predict(tf_idf_features))
                )
            result = sorted(result, reverse=True, key=lambda x: x[1])
            count = 0
            for item in result:
                if count == 30:
                    break
                count += 1
                outfile.write(" ".join(
                    map(
                        str, [canon_to_id[kinase], "dummy", item[0], count, item[1] * 100, arguments["runid"]]
                    )
                ) + "\n")
