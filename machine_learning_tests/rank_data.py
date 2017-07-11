import pickle
from sklearn.externals import joblib

if __name__ == "__main__":
    basic_vectorizer = joblib.load(input("Give vectorizer file path: "))
    classifier = joblib.load(input("Give classifier file path: "))
    for kinase, doc_set in pickle.load(open(input("Give cross reference file path: "), "rb")).items():
        result = []
        for doc in doc_set:
            tf_idf_features = basic_vectorizer.transform(["/data/CM_input/FullText/FullTexts_All/" + doc + ".txt"])
            result.append((doc, classifier.predict_proba(tf_idf_features)[0][1], classifier.predict(tf_idf_features)))
        print(kinase, sorted(result, reverse=True, key=lambda x: x[1]))
