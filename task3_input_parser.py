import lxml.etree as etree
import pickle
import shutil as sh
import os

if __name__ == "__main__":

    input_file = r'/data/task3testdata/DIS_test_topics.xml'
    output_pkl_file = r'/data/task3testdata/task3_DIS_test_dict.pkl'
    move_files_from = r"/data/CM_output/FT/Post-Processed/All/NCIT-Restricted"
    move_files_to = r"/data/Task3/FT_T3/NCIT"

    xmi = etree.iterparse(input_file, events=("end", ))

    task3_dict = {}
    current_id = ""
    id_count = 0
    doc_count = 0
    for event, elem in xmi:
        if elem.tag == "id":
            current_id = elem.text
            id_count += 1
        elif elem.tag == "fulltext":
            task3_dict[current_id] = elem.text
            sh.copyfile(os.path.join(move_files_from, elem.text + ".txt.xmi.pkl"),
                        os.path.join(move_files_to, elem.text + ".txt.xmi.pkl"))
            doc_count += 1

    print("Dict Len: " + str(len(task3_dict)))
    print("Num ids: " + str(id_count))
    print("Num docs: " + str(doc_count))

    with open(output_pkl_file, 'wb') as pkl:
        pickle.dump(task3_dict, pkl, pickle.HIGHEST_PROTOCOL)
