import pickle
from sklearn.externals import joblib

if __name__ == "__main__":
    canon_to_id = pickle.load(open("/home/daniel/Downloads/PickleFiles/kinase_canonical_to_nxtprot_id.pkl", "rb"))
    basic_vectorizer = joblib.load(input("Give vectorizer file path: "))
    classifier = joblib.load(input("Give classifier file path: "))
    with open(input("Give filepath for desired ranking file: "), "w") as outfile:
        runid = input("Give run id: ")
        in_dict = pickle.load(open(input("Give cross reference file path: "), "rb"))
        cnt = 0
        for kinase, doc_set in in_dict.items():
            cnt += 1
            result = []
            for doc in doc_set:
                tf_idf_features = basic_vectorizer.transform(["/data/CM_input/FullText/FullTexts_All/" + doc + ".txt"])
                result.append((doc, classifier.predict_proba(tf_idf_features)[0][1], classifier.predict(tf_idf_features)))
            result = sorted(result, reverse=True, key=lambda x: x[1])
            count = 0
            for item in result:
                if count == 1000:
                    break
                count += 1
                outfile.write(" ".join(map(str, [canon_to_id[kinase], "dummy", item[0], count, item[1] * 100, runid])) + "\n")
            print(len(in_dict) - cnt)
