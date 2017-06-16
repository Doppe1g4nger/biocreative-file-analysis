import pickle

from BioCObject import BioCObject


def get_training_set_pmid(file_name):
    all_training_ids = set()
    with open(file_name) as infile:
        for line in infile:
            line = line.split()
            all_training_ids.add(line[2])
    return all_training_ids


def get_id(etree_element):
    doc_id = ""
    for _id in etree_element.iter("id"):
        doc_id = _id.text
    return doc_id


def get_abstract(etree_element):
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
