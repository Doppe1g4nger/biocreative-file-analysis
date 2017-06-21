from os import listdir
import os.path as path
import lxml.etree as etree
import csv
import sys


def get_all_files(fpath):
    return [(path.join(fpath, f), f) for f in listdir(fpath) if path.isfile(path.join(fpath, f))]

if __name__ == "__main__":
    csv.field_size_limit(sys.maxsize)  # Thank god for stack overflow
    filepaths = get_all_files("/home/daniel/Downloads/OntologyCSVs/")
    base_output_path = "/home/daniel/Downloads/ConMapDictionaries/DISDictionaries/"
    for file, fname in filepaths:
        with open(base_output_path + fname.strip(".csv") + ".xml", "wb") as outfile:
            root = etree.Element("synonym")
            with open(file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    concept_url = row["Class ID"]
                    concept_code = concept_url.split("/")[-1]
                    if "#" in concept_code:
                        concept_code = concept_code.split("#")[-1]
                    concept_name = row["Preferred Label"]
                    synonyms = row["Synonyms"]
                    token = etree.SubElement(root, "token", id=concept_code, canonical=concept_name)
                    for syn in synonyms.split("|"):
                        if syn:
                            token.append(etree.Element("variant", base=syn))
            outfile.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
            et = etree.ElementTree(root)
            et.write(outfile, pretty_print=True)
