"""
Parser for the NCI Thesaurus flat file format.
Uses custom NCIConcept object type to represent each concept in the Thesaurus
"""

import csv
import random

from NCIConcept import NCIConcept

# Defines the field names used in the NCI Thesaurus flat format.
# Each concept in an NCI flat file contains these items separated by tabs
_fieldnames = (
    "code", "concept_name",
    "parents", "synonyms",
    "definition", "display_name",
    "concept_status", "semantic_type"
)


def get_desired_semantic_types(file_name):
    """
    Opens file of possible semantic types and returns those with an ! select marker.
    :param file_name: string, file path to file of semantic types
    :return: set of selected types from file
    """
    selected_types = set()
    with open(file_name) as f:
        for line in f:
            line = line.strip()  # Removes newline that confuses endswith in next statement
            if not line.startswith("!") and line.endswith(":"):
                selected_types.add(line[0:-1])
    return selected_types


def get_desired_concepts(concept_list, semantic_types):
    """
    Returns a list of concepts restrained to a desired subset of semantic types
    :param concept_list: list, of NCIConcept objects
    :param semantic_types: set, of desired semantic types
    :return: list, of concepts as a subset of the list passed as an argument
    """
    desired_concept_list = []
    for c in concept_list:
        for s_type in c.semantic_types:
            if s_type in semantic_types:
                desired_concept_list.append(c)
                break
    return desired_concept_list


def get_semantic_types(thesaurus_file):
    """
    Returns a list of all different semantic types in a given flat NCI Thesaurus file
    :param thesaurus_file: string, file path to NCI Thesaurus file in flat format
    :return: list of all different "semantic type" fields
    """
    type_list = set()
    with open(thesaurus_file) as f:
        reader = csv.DictReader(f, fieldnames=_fieldnames, delimiter="\t")
        for row in reader:
            for _item in row["semantic_type"].split("|"):
                type_list.add(_item)
    # Convert set to list at end because sets are better for building group of all
    # unique types, however lists are faster to iterate over and actually use
    return list(type_list)


def build_concept_list(thesaurus_file, restrict_semantic_types=False, sem_types=None):
    """
    Builds a list of NCIConcept objects, optionally restricted by
    :param thesaurus_file: string, path to thesaurus file
    :param sem_types: set or list, semantic types to restrict defined objects to
    :param restrict_semantic_types: bool, set true to restrict to only concepts with semantic type in sem_types
    :return: list of concepts a NCIConcept objects
    """
    concept_list = []
    with open(thesaurus_file) as f:
        reader = csv.DictReader(f, fieldnames=_fieldnames, delimiter="\t")
        if restrict_semantic_types:
            if sem_types is None:
                raise ValueError("Error: sem_types=None,"
                                 " sem_types must be a list or set of semantic_types")
            for row in reader:
                is_relevant = False
                for sem in row["semantic_type"].split("|"):
                    if sem in sem_types:
                        is_relevant = True
                        break
                if is_relevant:
                    _concept = NCIConcept(row)
                    concept_list.append(_concept)
        else:
            for row in reader:
                _concept = NCIConcept(row)
                concept_list.append(_concept)
    return concept_list


if __name__ == "__main__":
    # Keeps track of each semantic_type, and stores up to 10 example concept names within that type
    type_example_dict = {}
    thesaurus = r"C:\Users\Danie\Downloads\NCIThesauri\Thesaurus_17.04d.FLAT\Thesaurus.txt"
    # Build a list of all concepts and all semantic types
    concepts = build_concept_list(thesaurus)
    all_semantic_types = get_semantic_types(thesaurus)
    # write semantic types out to a file and build example for dictionary
    with open(r"C:\Users\Danie\Downloads\semantic_types.txt", "w") as types:
        sorted_types = sorted(all_semantic_types)
        for sem_type in sorted_types:
            types.write(sem_type)
            if sem_type != sorted_types[-1]:
                types.write("\n")
            type_example_dict[sem_type] = []
    # Build a file of each semantic type and examples for each
    for concept in concepts:
        # Because objects can have more than one semantic type, randomly choose one from list for example
        chosen_type = random.choice(concept.semantic_type)
        if len(type_example_dict[chosen_type]) < 10:
            type_example_dict[chosen_type].append(concept.concept_name)
    with open(r"C:\Users\Danie\Downloads\semantic_types_and_examples.txt", "w") as examples:
        for semantic_type in sorted(type_example_dict):
            examples.write(semantic_type + ":\n")
            for item in type_example_dict[semantic_type]:
                examples.write(item)
                if item != type_example_dict[semantic_type][-1]:
                    examples.write(",\n")
            examples.write("\n\n")
