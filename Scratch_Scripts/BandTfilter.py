from shutil import copyfile
import os

origin_path = '/data/CM_input/Abst/Abst_BandT'
completed_path = '/data/CM_output/Abst/Post-Processed/BandT/Kinase_DIS_Train_RW'
new = '/data/CM_input/Abst/Partial'
complete = set(filename.strip(".xmi.pkl") for filename in os.listdir(completed_path))
print("I")
origin = [filename for filename in os.listdir(origin_path)]
print("II")

count = 0
copied = 0

for item in origin:
    count += 1
    if count % 1000 == 0:
        print(count)

    if item not in complete:
        copied += 1
        if copied % 10000 == 0:
            print("COPIED: " + str(copied))

        copyfile(origin_path + '/' + item, new + '/' + item)
