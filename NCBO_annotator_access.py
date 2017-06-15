import requests

import NCI_flat_file_parser as NCIt
from BioCObject import BioCObject


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
        for item in concept.synonyms:
            restricted_terms.add(item.strip().lower())
    return restricted_terms

if __name__ == "__main__":
    all_terms = get_restricted_ncit_terms()
    base_url = "http://data.bioontology.org/annotator"
    api_key = get_api_key(r"C:\Users\Danie\PycharmProjects\biocreative-file-analysis\NCBO_API_KEY")
    parameters = {
        "ontologies": ["NCIT"],
        "apikey": api_key,
        "text": "Melanoma is a malignant tumor of melanocytes "
                "which are found predominantly in skin but also in the bowel and the eye."
    }
    abstracts = BioCObject(r"C:\Users\Danie\Downloads\TaskData\abstracts_collection.xml")
    count = 0
    for _, elem in abstracts.manual_iterator():
        if elem.tag == "document" and count == 4:
            for passage in elem.iter("passage"):
                passage_type = ""
                for infon in passage.iter("infon"):
                    if infon.attrib["key"] == "type":
                        passage_type = infon.text
                if passage_type == "AbstractPassage":
                    for item in passage.iter("text"):
                        parameters["text"] = item.text
                        break
                    break
            break
        if elem.tag == "document":
            count += 1
            elem.clear()
    r = requests.get(base_url, params=parameters)
    print(r.url)
    json_response = r.json()
    count = 0
    for item in json_response:
        for annotation in item["annotations"]:
            # print(annotation["matchType"], annotation["text"])
            if annotation["text"].strip().lower() in all_terms:
                print(annotation["matchType"], annotation["text"])
                count += 1
    print(count)
