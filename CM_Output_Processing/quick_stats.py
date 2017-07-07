import pickle
import statistics

path = '/data/CM_output/FT/Post-Processed/All/FT_All_TestSet_NCIT-Restricted.pkl'


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

dict = load_obj(path)

sum = []

for item in dict:
    sum.append(len(dict[item]))
    print(str(item) + " " + str(len(dict[item])))

print("average: " + str(statistics.mean(sum)))
print("median: " + str(statistics.median(sum)))