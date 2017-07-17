import pickle
import statistics
from shutil import copyfile

path1 = '/data/CM_output/Abst/Post-Processed/BandT/Abst_DIS_ORDO_IR.pkl'
path2 = '/data/CM_output/Abst/Post-Processed/BandT/Abst_DIS_HP_IR.pkl'
path3 = '/data/CM_output/Abst/Post-Processed/BandT/Abst_DIS_NCIT-Restricted_IR.pkl'
path4 = '/data/CM_output/Abst/Post-Processed/BandT/Abst_BP_GO_IR.pkl'
path5 = '/data/CM_output/Abst/Post-Processed/BandT/Abst_BP_GO-old_IR.pkl'


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def get_stats(path):
    dict = load_obj(path)

    sums = []
    doc_set = set()

    for item in dict:
        sums.append(len(dict[item]))
        print(str(item) + " " + str(len(dict[item])))

        for doc in dict[item]:
            doc_set.add(doc)

    print("average: " + str(statistics.mean(sums)))
    print("median: " + str(statistics.median(sums)))
    print("sum: " + str(sum(sums)))
    print("num docs: " + str(len(doc_set)))
    return doc_set


if __name__ == "__main__":
    s1 = get_stats(path1)
    s2 = get_stats(path2)
    s3 = get_stats(path3)
    s4 = get_stats(path4)
    s5 = get_stats(path5)

    su = set.union(s1, s2, s3, s4, s5)

    count = 0

    for doc in su:
        count += 1
        if count % 1000 == 0:
            print(count)
        copyfile("/data/CM_input/Abst/Abst_BandT/" + doc + ".txt", "/data/CM_input/Abst/Abst_BandT_IR/" + doc + ".txt")

