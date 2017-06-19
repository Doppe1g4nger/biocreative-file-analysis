"""
Extracts the abstracts (Not including titles) from a given training set; places them into an id to abstract
dictionary and pickles it.
"""
import pickle

from BioCObject import BioCObject


def get_training_set_pmid(file_name):
    """
    Opens file containing training set document ids and extracts PMID of each document
    :param file_name: path to dis or bp training set file
    :return: set, of PMIDs
    """
    all_training_ids = set()
    with open(file_name) as infile:
        for line in infile:
            line = line.split()
            all_training_ids.add(line[2])
    return all_training_ids


def get_id(etree_element):
    """
    Pulls id from aa given etee element
    :param etree_element: element type from lxml.etree
    :return: string, document id from the etree element passed as an argument
    """
    doc_id = ""
    for _id in etree_element.iter("id"):
        doc_id = _id.text
    return doc_id


def get_abstract(etree_element):
    """
    Gets abstract from document etree element
    :param etree_element: etree element from lxml.etree, must have passage child element
    :return: string, abstract body text
    todo: Generalize to a "get element" style function for abstract title etc.
    """
    abstract_text = ""
    for passage in etree_element.iter("passage"):
        passage_type = ""
        for infon in passage.iter("infon"):
            if infon.attrib["key"] == "type":
                passage_type = infon.text
        if passage_type == "AbstractPassage":
            for text in passage.iter("text"):
                abstract_text += text.text
    return abstract_text


if __name__ == "__main__":
    dis_training_ids = get_training_set_pmid(
        r"C:\Users\Danie\Downloads\TaskData\task1trainingdata\task1trainingdata\BP_train.qrel")
    print(len(dis_training_ids))
    id_to_abstract = {}
    abstracts = BioCObject(r"C:\Users\Danie\Downloads\TaskData\abstracts_collection.xml")
    doc_count = 0
    for _, elem in abstracts.manual_iterator():
        if elem.tag == "document":
            doc_count += 1
            if not doc_count % 10000:
                print(doc_count)
            elem_id = get_id(elem)
            if elem_id in dis_training_ids:
                id_to_abstract[elem_id] = get_abstract(elem)
            elem.clear()
    with open(r"C:\Users\Danie\Downloads\dis_training_abstracts.pkl", "wb") as file:
        pickle.dump(id_to_abstract, file)
    print("done processing")
