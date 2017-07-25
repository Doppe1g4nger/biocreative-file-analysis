import pickle
import lxml.etree as etree

if __name__ == "__main__":
    canon_to_id = {}
    root = etree.parse("/data/ConMapDictionaries/Protein Dictionaries/Original_Dictionaries/all_kinases.xml")
    for token in root.iter("token"):
        canon_to_id[token.attrib["canonical"]] = token.attrib["id"]
    with open(input("Gib pkl: "), "wb") as out:
        pickle.dump(canon_to_id, out)
