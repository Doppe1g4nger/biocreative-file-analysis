import lxml.etree as etree
from collections import defaultdict
from os import listdir
import os.path as path


def get_all_files(fpath):
    return [path.join(fpath, f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]


def get_names(term_tags, superset, node):
    term_list = []
    for it in node.iter("{http://uniprot.org/uniprot}" + superset):
        for tag in it.iter():
            if tag.tag[len("{http://uniprot.org/uniprot}"):] in term_tags and tag.text.strip() != "":
                term_list.append(tag.text.strip())
    return term_list


if __name__ == "__main__":
    path_to_alter = "/home/daniel/Downloads/ConMapDictionaries/Protein Dictionaries/Original_Dictionaries/"
    synonym_dict = defaultdict(list)
    name_tags = {
        "fullName",
        "name",
        "shortName",
        "alternativeName",
        "recommendedName",
    }
    root = etree.parse("/home/daniel/Downloads/uniprot-kinase.xml")
    for entry in root.iter("{http://uniprot.org/uniprot}entry"):
        all_terms = []
        all_terms += get_names(name_tags, "protein", entry)
        all_terms += get_names(name_tags, "gene", entry)
        for term in all_terms:
            for temp in all_terms:
                synonym_dict[term].append(temp)
        entry.clear()
    for file in get_all_files(path_to_alter):
        root_to_mod = etree.parse(file)
        for token in root_to_mod.iter("token"):
            found_tokens = []
            names = [variant.attrib["base"] for variant in token.iter("variant")]
            for name in names:
                if name in synonym_dict:
                    for item in synonym_dict[name]:
                        if item not in names and item not in found_tokens:
                            found_tokens.append(item)
                    break
            for variant in found_tokens:
                new_variant = etree.Element("variant", base=variant)
                token.append(new_variant)
        with open(file.replace("/Original_Dictionaries/", "/Uniprot_Extended_Dictionaries/"), "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
            root_to_mod.write(f, pretty_print=True)
