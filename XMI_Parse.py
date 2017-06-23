import lxml.etree as etree
from collections import Counter
import os
from AnnotatedArticle import AnnotatedArticle
import pickle

input_path = '/data/CM_output/Comparison/Kinases/Relevant/BP/'
output_path = '/data/CM_output/Comparison/Kinases/Relevant/Post-Processed/BP/'
list_of_hit_counts = []
zero_counter = 0
delete_input_files = False

for filename in os.listdir(input_path):

    xmi = etree.iterparse(input_path + filename, events=("end", ))

    hit_count = 0
    all_hit_terms_list = []
    all_hit_attributes = []

    for _, elem in xmi:
        if 'DictTerm' in str(elem):
            hit_count += 1
            all_hit_terms_list.append(elem.attrib['DictCanon'])
            all_hit_attributes.append(dict(elem.attrib))

    hit_terms_count = Counter(all_hit_terms_list)
    all_hit_terms_set = set(all_hit_terms_list)

    article_obj = AnnotatedArticle("TestDict", hit_count, all_hit_terms_set, hit_terms_count, all_hit_attributes)
    list_of_hit_counts.append(hit_count)
    if hit_count == 0:
        zero_counter += 1

    if delete_input_files:
        os.remove(input_path + filename)

    with open(output_path + filename + '.pkl', 'wb') as output_file:
        pickle.dump(article_obj, output_file, pickle.HIGHEST_PROTOCOL)


print("Average hits: " + str(sum(list_of_hit_counts) / len(list_of_hit_counts)))
print("Num with no hits: " + str(zero_counter))
print("Percent hits: " + str(1 - zero_counter/1616))
