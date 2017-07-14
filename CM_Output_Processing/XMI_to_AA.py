# XMI_to_AA

import lxml.etree as etree
from collections import Counter
import os
import AnnotatedArticle as aa
import pickle


if __name__ == "__main__":

    # input_list = [x[0] for x in os.walk('/data/CM_output/Comparison_FT/Kinases/Combined/DictCompare/')]
    # output_list = [x[0] for x in os.walk('/data/CM_output/Comparison_FT/Kinases/Combined/Post-Processed/DictCompare/')]
    # del input_list[0], output_list[0]

    input_list = ['/data/CM_output/FT/All/Kinase_BP_Test']
    output_list = ['/data/CM_output/FT/Post-Processed/All/Kinase_BP_Test']
    wc_output = '/data/CM_output/Abst/Post-Processed/BandT/FT_wordcount.pkl'



    for i in range(0, len(input_list)):

        input_path = input_list[i]
        output_path = output_list[i]
        list_of_hit_counts = []
        zero_counter = 0
        delete_input_files = False
        doc_count = 0
        word_count_dict = {}

        for filename in os.listdir(input_path):
            wordcount = 0
            doc_count += 1
            if doc_count % 10000 == 0:
                print(doc_count)

            xmi = etree.iterparse(input_path + "/" + filename, events=("end", ))

            hit_count = 0
            all_hit_terms_list = []
            all_hit_terms_set = set()
            all_hit_attributes = []
            hit_terms_count = Counter()


            for _, elem in xmi:
                if 'TokenAnnotation' in str(elem):
                    wordcount += 1
                if str(elem).__contains__('DictTerm'):
                    hit_count += 1
                    all_hit_terms_list.append(elem.attrib['DictCanon'])
                    all_hit_attributes.append(dict(elem.attrib))

            word_count_dict[filename.strip('.txt.xmi')] = wordcount
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

        print(input_path)

        with open(wc_output, 'wb') as output_file:
            pickle.dump(word_count_dict, output_file, pickle.HIGHEST_PROTOCOL)
