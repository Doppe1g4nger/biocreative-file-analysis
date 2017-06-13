import csv
import pickle

from NCIConcept import NCIConcept

if __name__ == "__main__":
    fieldnames = (
        "code", "concept_name",
        "parents", "synonyms",
        "definition", "display_name",
        "concept_status", "semantic_type"
    )
    # comprehensive_concept_dict = {}
    # type_set = set()
    concept_list = []
    with open(r"/home/daniel/Downloads/Thesaurus.txt") as file:
        reader = csv.DictReader(file, fieldnames=fieldnames, delimiter="\t")
        for row in reader:
            # for item in row["semantic_type"].split("|"):
                # type_set.add(item)
            concept = NCIConcept(row)
            concept_list.append(concept)
        # with open("/home/daniel/Downloads/semantic_types.txt", "w") as types:
        #     for concept_type in sorted(type_set):
        #         types.write(concept_type + "\n")
            # comprehensive_concept_dict[concept.concept_name] = list(concept.synonyms)
    with open("/home/daniel/Downloads/NCIFullConcepts.p", "wb") as file:
        pickle.dump(concept_list, file)
        # pickle.dump(comprehensive_concept_dict, file)
