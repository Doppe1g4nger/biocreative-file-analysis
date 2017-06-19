def get_unique_annotations(file_name):
    ann_id = ""
    id_to_annotations = {}
    with open(file_name) as file:
        for line in file:
            if line.startswith("PMID: "):
                ann_id = line[6:].strip()
                id_to_annotations[ann_id] = set()
            elif line.startswith("SYN") or line.startswith("PREF"):
                line = line.split()
                id_to_annotations[ann_id].add(line[1])
    return id_to_annotations

if __name__ == "__main__":
    terms_to_be_compared_to = get_unique_annotations(r"C:\Users\Danie\Downloads\dis_training_set_NCBO_test.txt")
    ontologies = ["DOID", "HP", "IDO", "ORDO", "PDO", "MESH", "SNOMEDCT", "RCD", "OAE", "ICD10CM"]
    with open(r"C:\Users\Danie\Downloads\ontology_comparison_results.txt") as f:
        for ontology in ontologies:
            num_unique_terms = 0
            terms_to_compare = get_unique_annotations(
                r"C:\Users\Danie\Downloads\dis_training_set_NCBO_test_" + ontology + ".txt")
            for _id in terms_to_be_compared_to:
                if _id in terms_to_compare:
                    for annotation in terms_to_compare[_id]:
                        if annotation not in terms_to_be_compared_to[_id]:
                            num_unique_terms += 1
            average_unique_terms = num_unique_terms / len(terms_to_compare)
            f.write("Compared to NCIT, "
                    + ontology + " had an average of:\n"
                    + str(average_unique_terms) + "unique terms per abstract that both ontologies annotated.\n")
