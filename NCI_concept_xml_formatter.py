"""
Script to pull desired concepts out of NCI Thesaurus and either:
1. Annotate BioC data directly with NCBO Annotator Web API
2. Convert concepts to appropriate XML file to be fed into Concept Mapper
"""

import NCI_flat_file_parser as NCIt
from lxml import etree

if __name__ == "__main__":
    thesaurus_path = "/home/daniel/Downloads/Thesaurus.txt"
    sem_type_path = "/home/daniel/Downloads/semantic_types_and_examples_v2.txt"
    semantic_types = NCIt.get_desired_semantic_types(sem_type_path)
    ncit_concepts = NCIt.build_concept_list(thesaurus_path, restrict_semantic_types=True,
                                            sem_types=semantic_types)
    root = etree.Element("synonym")
    for concept in ncit_concepts:
        token = etree.SubElement(root, "token", id=concept.code,
                                 canonical=concept.concept_name
                                 )
        token.append(etree.Element("variant", base=concept.concept_name))
        for synonym in concept.synonyms:
            token.append(etree.Element("variant", base=synonym))
    with open("/home/daniel/Downloads/DIS_concept_dictionary.xml", "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
        et = etree.ElementTree(root)
        et.write(f, pretty_print=True)
