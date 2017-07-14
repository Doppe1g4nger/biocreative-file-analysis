import pickle
from lxml import etree
from collections import defaultdict


def write_to_xml(kinase_dict, f_name):
    """
    :param kinase_dict: dictionary, of kinase id mapped to list of kinase names
    :param f_name: string, file name
    :param canonical: string, canonical name
    :return: None
    """
    root = etree.Element("synonym")
    for key in kinase_dict:
        token = etree.SubElement(
            root, "token", id=key,
            canonical=kinase_dict[key][0]
        )
        token.append(etree.Element("variant", base=key))
        for synonym in kinase_dict[key]:
            if synonym is not None:
                token.append(etree.Element("variant", base=synonym))
    with open(f_name, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
        et = etree.ElementTree(root)
        et.write(f, pretty_print=True)


def load_obj(file_name):
    """
    Loads an object from pickle
    :param file_name: string, name of pckle file to be unpickled
    :return: unpickled object
    """
    with open(file_name, "rb") as f:
        return pickle.load(f)


def print_dict(dictionary):
    """
    Test function for internal use
    :param dictionary: dictionary
    :return: None
    """
    for key, value in dictionary.items():
        for item in value:
            if item is None:
                print(key, value)

if __name__ == "__main__":
    kinase_map = defaultdict(list)
    f = input("Give path to xml kinase synonym file: ")
    while f != "q":
        root = etree.parse(f)
        for topic in root.iter("topic"):
            syns = set()
            kinase_id = ""
            primary = ""
            count = 0
            prim_cnt = 0
            if not topic.iter("id"):
                raise ValueError("OOPS")
            for idx in topic.iter("id"):
                kinase_id = idx.text
                count += 1
            if count != 1:
                raise ValueError("OOPS")
            for gene in topic.iter("gene"):
                if gene.attrib["form"] == "primary":
                    primary = gene.text
                    prim_cnt += 1
            if prim_cnt != 1:
                raise ValueError("OOPS")
            if not kinase_map[kinase_id]:
                kinase_map[kinase_id].append(primary)
            for syn in topic.iter():
                if syn.tag in {"gene", "protein", "id"} and syn.text not in {primary, kinase_id} and syn.text not in kinase_map[kinase_id]:
                    kinase_map[kinase_id].append(syn.text)
                    syns.add(syn.text)
        f = input("Give path to xml kinase synonym file: ")
    write_to_xml(kinase_map, input("Give file name: "))








