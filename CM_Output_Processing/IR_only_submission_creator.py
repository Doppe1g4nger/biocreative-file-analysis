import pickle


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def rank_aggregate_score(doc_list):
    scores = []

    for doc in doc_list:
        score = doc[1] * 900 + doc[2] * 40 - doc[4] * 0.03 + doc[5] * 0.25 + doc[6] * 0.04 / 3
        scores.append((doc[0], score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


def rank_rel_score(doc_list):
    scores = []

    for doc in doc_list:
        score = doc[3] * 100000
        scores.append((doc[0], score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


def rank_prox_score(doc_list):
    scores = []

    for doc in doc_list:
        score = -(doc[4] * 0.03) + doc[5] * 0.25 + doc[6] * 0.04
        scores.append((doc[0], score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


def rank_K_score(doc_list):
    scores = []

    for doc in doc_list:
        score = doc[1] * 900
        scores.append((doc[0], score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


def rank_A_score(doc_list):
    scores = []

    for doc in doc_list:
        score = doc[2] * 40
        scores.append((doc[0], score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


def rank_prx50_score(doc_list):
    scores = []

    for doc in doc_list:
        score = doc[6] * 0.04
        scores.append((doc[0], score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


def print_ranked(ranked_dict, identifier):
    counter = 0

    with open(output_tsv_file, 'a') as out_file:
        for i in range(0, 1000):
            try:
                output_text = nextprot_dict[kinase] + " dummy " + str(ranked_dict[i][0]) + " " + str(i + 1) + " " + str(round(ranked_dict[i][1], 3)) + " " + identifier
                print(output_text)
                print(output_text, file=out_file)
            except IndexError:
                break


if __name__ == "__main__":
    ir_feature_vector_input = "/data/CM_output/Abst/Post-Processed/Features/Final/Abst_HP_Test_Feat.pkl"
    output_tsv_file = "/data/Team392_Track2_Addendum/run7_Abst_HPO_DIS_Rel.txt"

    ir_dict = load_obj(ir_feature_vector_input)
    nextprot_dict = load_obj(r"/data/Task3/kinase_canonical_to_nxtprot_id.pkl")

    kins = []
    axis = []
    prox = []
    prox10 = []
    prox50 = []

    for kinase in ir_dict:
        ranked = rank_rel_score(ir_dict[kinase])
        print_ranked(ranked, "team392run19")





