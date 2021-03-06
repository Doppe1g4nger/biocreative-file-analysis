import os
import pickle
import helper_functions as helpers

if __name__ == "__main__":
    # Change these to work on different axis/tasks
    AXIS = "DIS"
    TASK = "Task2"
    RUN = "Run18"
    FILEDIR = "/mnt/lustrefs/store/ddopp/CM_input/FullText/FullTexts_All/"
    MLRANKSPATH = '/mnt/lustrefs/store/ddopp/ML_Ranking_Output/run18_DIS_fulltexts.txt'

    with open(helpers.replace_pathvar_with_environ("$STORE/kinase_canonical_to_nxtprot_id.pkl"), "rb") as f:
        canon_to_nxt = pickle.load(f)
    nxt_to_cannon = {val: key for key, val in canon_to_nxt.items()}

    file_info_tuples = []
    with open(MLRANKSPATH) as ranks:
        for line in ranks:
            elems = line.split()
            file_info_tuples.append((nxt_to_cannon[elems[0]], elems[2], elems[3], elems[4]))

    for file in file_info_tuples:
        file_text = ""
        with open(FILEDIR + file[1] + ".txt") as infile:
            file_text = infile.read()
        kinase_subset = sorted(
            [item for item in file_info_tuples if item[0] == file[0]],
            key=lambda x: int(x[2])
        )
        # print(kinase_subset)
        dir_path = "/mnt/lustrefs/store/ddopp/ML_Ranking_Output/BioCreativeVI_Track2/" \
                   + "/".join([TASK, AXIS, RUN, file[0]]) + "/"
        os.makedirs(dir_path, exist_ok=True)
        # May god have mercy on my soul
        with open(dir_path + "rank" + "0" * (len(kinase_subset[-1][2]) - len(file[2])) + file[2]
                  + "_0." + "".join(file[3].split(".")) + "_" + file[1] + ".txt", "w") as outfile:
            outfile.write(file_text)
        with open(dir_path + "rank" + "0" * (len(kinase_subset[-1][2]) - len(file[2])) + file[2]
                  + "_0." + "".join(file[3].split(".")) + "_" + file[1] + ".ann", "w") as outfile:
            outfile.write("")
