# XMI_to_AA

import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle
import multiprocessing as mp


input_path = '/data/CM_output/Comparison/Kinases/Relevant/BP'
output_path = '/data/CM_output/Comparison/Kinases/Relevant/Post-Processed/Test_BP'
delete_input_files = False


def processes_xmi(filename):
    xmi = etree.iterparse(input_path + "/" + filename, events=("end",))

    hit_count = 0
    zero_counter = 0
    all_hit_terms_list = []
    all_hit_attributes = []
    list_of_hit_counts = []

    for _, elem in xmi:
        if str(elem).__contains__('DictTerm'):
            hit_count += 1
            all_hit_terms_list.append(elem.attrib['DictCanon'])
            all_hit_attributes.append(dict(elem.attrib))

    hit_terms_count = Counter(all_hit_terms_list)
    all_hit_terms_set = set(all_hit_terms_list)

    article_obj = aa.AnnotatedArticle("TestDict", hit_count, all_hit_terms_set, hit_terms_count, all_hit_attributes)
    list_of_hit_counts.append(hit_count)
    if hit_count == 0:
        zero_counter += 1

    if delete_input_files:
        os.remove(input_path + "/" + filename)

    with open(output_path + "/" + filename + '.pkl', 'wb') as output_file:
        pickle.dump(article_obj, output_file, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    inputs = [filename for filename in os.listdir(input_path)]

    pool = mp.Pool(processes=8)
    pool.map(processes_xmi, inputs)
