"""
Script to pull desired concepts out of NCI Thesaurus and either:
1. Annotate BioC data directly with NCBO Annotator Web API
2. Convert concepts to appropriate XML file to be fed into Concept Mapper
"""

import NCI_flat_file_parser as NCIt

if __name__ == "__main__":
    thesaurus_path = "/home/daniel/Downloads/Thesaurus.txt"
    sem_type_path = "/home/daniel/Downloads/semantic_types_and_examples_v2.txt"
    semantic_types = NCIt.get_desired_semantic_types(sem_type_path)
    ncit_concepts = NCIt.build_concept_list(thesaurus_path, restrict_semantic_types=True,
                                            sem_types=semantic_types)
