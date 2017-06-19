import pickle
import random

import training_abstract_extractor as abs_extract
from BioCObject import BioCObject


if __name__ == "__main__":
    dis_training_ids = abs_extract.get_training_set_pmid(
        r"C:\Users\Danie\Downloads\TaskData\task1trainingdata\task1trainingdata\DIS_train.qrel")
    num_abstracts = len(dis_training_ids)
    id_to_abstract = {}
    count = 0
    abstracts = BioCObject(r"C:\Users\Danie\Downloads\TaskData\abstracts_collection.xml").abstracts()
    while count < num_abstracts:
        rand_abstract_id = random.choice(abstracts.keys())
        if rand_abstract_id in dis_training_ids:
            pass
        else:
            id_to_abstract[rand_abstract_id] = abstracts[rand_abstract_id]
            count += 1
    print(len(id_to_abstract))
    with open(r"C:\Users\Danie\Downloads\dis_irrelevant_abstracts.pkl", "wb") as file:
        pickle.dump(id_to_abstract, file)
    print("done processing")
