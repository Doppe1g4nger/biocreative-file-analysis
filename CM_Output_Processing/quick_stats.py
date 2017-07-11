import pickle
import statistics

path = '/data/CM_output/FT/Post-Processed/All/FT_All_TestSet_NCIT-Restricted.pkl'


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

    base = "This is a test IV"
    index = base.index(" IV")
    new_base = base[index - len(base) + 3:]
    print(new_base)

    count = 0
    while count < 44000000:
        count += 1
    print(count)