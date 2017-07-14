from machine_learning_tests import helper_functions as h

if __name__ == "__main__":
    for file in h.get_all_files('/data/CM_input/Abst/Abst_Titles'):
        with open('/data/CM_input/Abst/Abst_BandT_new/' + file.split("/")[-1], "w") as out:
            with open(file) as title:
                for line in title:
                    out.write(line)
                out.write("\n")
            with open('/data/CM_input/Abst/Abst_Bodies/' + file.split("/")[-1]) as body:
                for line in body:
                    out.write(line)
