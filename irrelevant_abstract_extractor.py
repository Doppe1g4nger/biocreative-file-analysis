import pickle
import random

import training_abstract_extractor as abs_extract
from BioCObject import BioCObject


if __name__ == "__main__":
    dis_training_ids = abs_extract.get_training_set_pmid(
        r"/home/daniel/Downloads/task1trainingdata/task1trainingdata/DIS_train.qrel")
    print(len(dis_training_ids))
    num_abstracts = len(dis_training_ids)
    id_to_abstract = {}
    count = 0
    abstracts = BioCObject(r"/home/daniel/Downloads/abstracts_collection.xml").abstracts()
    temp = list(abstracts.keys())
    while count != num_abstracts:
        rand_abstract_id = random.choice(temp)
        if rand_abstract_id not in dis_training_ids and rand_abstract_id not in id_to_abstract:
            id_to_abstract[rand_abstract_id] = abstracts[rand_abstract_id]
            count += 1
    print(len(id_to_abstract))
    with open(r"/home/daniel/Downloads/dis_irrelevant_abstracts.pkl", "wb") as file:
        pickle.dump(id_to_abstract, file)
    print("done processing")
