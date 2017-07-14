import pickle
import statistics

path = '/data/CM_output/Abst/Post-Processed/BandT/Abst_DIS_HP_IR.pkl'


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    dict = load_obj(path)

    sum = []

    for item in dict:
        sum.append(len(dict[item]))
        print(str(item) + " " + str(len(dict[item])))

    print("average: " + str(statistics.mean(sum)))
    print("median: " + str(statistics.median(sum)))

