import requests
import time
import pickle

import NCI_flat_file_parser as NCIt


def get_api_key(key_path):
    with open(key_path) as f:
        return f.read()


def get_restricted_ncit_terms():
    thesaurus_path = r"C:\Users\Danie\Downloads\NCIThesauri\Thesaurus_17.04d.FLAT\Thesaurus.txt"
    sem_type_path = r"C:\Users\Danie\Downloads\semantic_types_and_examples_v2.txt"
    semantic_types = NCIt.get_desired_semantic_types(sem_type_path)
    ncit_concepts = NCIt.build_concept_list(thesaurus_path, restrict_semantic_types=True,
                                            sem_types=semantic_types)
    restricted_terms = set()
    for concept in ncit_concepts:
        restricted_terms.add(concept.concept_name.strip().lower())
        for _item in concept.synonyms:
            restricted_terms.add(_item.strip().lower())
    return restricted_terms


if __name__ == "__main__":
    ontologies = ["GO"]
    # all_terms = get_restricted_ncit_terms()
    base_url = "http://data.bioontology.org/annotator"
    api_key = get_api_key(r"C:\Users\Danie\PycharmProjects\biocreative-file-analysis\NCBO_API_KEY")
    parameters = {
        "ontologies": [],
        "apikey": api_key,
        "text": "Melanoma is a malignant tumor of melanocytes "
                "which are found predominantly in skin but also in the bowel and the eye."
    }
    for ontology in ontologies:
        with open(r"C:\Users\Danie\Downloads\bp_training_set_NCBO_test_" + ontology + ".txt", "w") as file:
            parameters["ontologies"] = [ontology]
            num_calls = 0
            num_zero_annotations = 0
            num_annotations = 0
            tot_annotations = 0
            id_to_abstract = {}
            with open(r"C:\Users\Danie\Downloads\bp_training_abstracts.pkl", "rb") as f:
                id_to_abstract = pickle.load(f)
            for abs_id in id_to_abstract:
                num_annotations = 0
                annotation_type_and_name = []
                parameters["text"] = id_to_abstract[abs_id]
                r = requests.get(base_url, params=parameters)
                num_calls += 1
                json_response = r.json()
                for item in json_response:
                    for annotation in item["annotations"]:
                        num_annotations += 1
                        annotation_type_and_name.append((annotation["matchType"], annotation["text"]))
                tot_annotations += num_annotations
                if not num_annotations:
                    num_zero_annotations += 1
                if not num_calls % 10:
                    print(num_calls)
                    time.sleep(1)
                file.write("PMID: " + abs_id + "\n")
                file.write("Num Matches: " + str(num_annotations) + "\n")
                for ann_type, text in annotation_type_and_name:
                    file.write(ann_type + " " + text + "\n")
                file.write("\n")
            print("average annotations: " + str(tot_annotations // len(id_to_abstract)))
            print("num zero annotations: " + str(num_zero_annotations))
            print(str(num_zero_annotations / len(id_to_abstract) * 100) + " percent of articles pulled no annotations")
        # with open(r"C:\Users\Danie\Downloads\bp_training_set_NCBO_test_restricted.txt", "w") as f:
        #     num_calls = 0
        #     num_zero_annotations = 0
        #     tot_annotations = 0
        #     num_annotations = 0
        #     with open(r"C:\Users\Danie\Downloads\bp_training_abstracts.pkl", "rb") as f:
        #     id_to_abstract = pickle.load(f)
        #     for abs_id in id_to_abstract:
        #         num_annotations = 0
        #         annotation_type_and_name = []
        #         parameters["text"] = id_to_abstract[abs_id]
        #         r = requests.get(base_url, params=parameters)
        #         num_calls += 1
        #         json_response = r.json()
        #         for item in json_response:
        #             for annotation in item["annotations"]:
        #                 if annotation["text"].strip().lower() in all_terms:
        #                     num_annotations += 1
        #                     annotation_type_and_name.append((annotation["matchType"], annotation["text"]))
        #         tot_annotations += num_annotations
        #         if not num_annotations:
        #             num_zero_annotations += 1
        #         if not num_calls % 10:
        #             time.sleep(1)
        #             print(num_calls)
        #         f.write("PMID: " + abs_id + "\n")
        #         f.write("Num Matches: " + str(num_annotations) + "\n")
        #         for ann_type, text in annotation_type_and_name:
        #             f.write(ann_type + " " + text + "\n")
        #         f.write("\n")
        #     print("average annotations: " + str(tot_annotations // len(id_to_abstract)))
        #     print("num zero annotations: " + str(num_zero_annotations))
        #     print(str(num_zero_annotations / len(id_to_abstract) * 100) + " percent of articles pulled no annotations")
