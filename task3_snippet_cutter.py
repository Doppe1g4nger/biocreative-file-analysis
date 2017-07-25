import os.path as path
import lxml.etree as etree
import pickle


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def get_prox_endpoints(rel_kinase, axis_AA, kinase_AA):
    axis_tokens = []
    kinase_tokens = []
    axis_attribs = axis_AA.list_of_attrib_dicts
    min_axis = (0, 0, 0)
    min_kinase = (0, 0, 0)
    nextprot_dict = load_obj(r"C:\Users\Adam\Documents\MSU REU\kinase_canonical_to_nxtprot_id.pkl")
    kinase_attribs = [kin for kin in kinase_AA.list_of_attrib_dicts if nextprot_dict[kin['DictCanon']] == rel_kinase]
    for attrib in axis_attribs:
        for token in attrib['matchedTokens'].split(" "):
            axis_tokens.append((int(token), attrib["begin"], attrib["end"]))
    for attrib in kinase_attribs:
        for token in attrib['matchedTokens'].split(" "):
            kinase_tokens.append((int(token), attrib["begin"], attrib["end"]))
    min_proximity = 999999
    for k in kinase_tokens:
        for a in axis_tokens:
            dist = abs(k[0] - a[0]) / 10
            if dist < min_proximity:
                min_proximity = dist
                min_kinase = k
                min_axis = a

    endpoints = [min_kinase[1], min_kinase[2], min_axis[1], min_axis[2]]
    begin = min(endpoints)
    end = max(endpoints)

    return begin, end


def build_dictionary(xml_path):
    xmi = etree.iterparse(xml_path, events=("end",))

    task3_dict = {}
    current_id = ""
    for event, elem in xmi:
        if elem.tag == "id":
            current_id = elem.text
        elif elem.tag == "fulltext":
            task3_dict[current_id] = elem.text
    return task3_dict


def cut_snippet(start_char, end_char, fulltext):
    snippet = ""

    first_half = fulltext[:start_char].split()
    gap = fulltext[start_char:end_char].split()
    second_half = fulltext[end_char:].split()

    segment_length = (500 - len(gap) - 2) // 2

    if len(first_half) < segment_length:
        for word in first_half:
            snippet += word + " "

    else:
        words = range(len(first_half) - segment_length, len(first_half))
        for i in words:
            snippet += first_half[i] + " "

    gap_counter = 0
    for word in gap:
        if gap_counter < 499:
            snippet += word + " "
        gap_counter += 1

    if len(second_half) < segment_length:
        for word in second_half:
            snippet += word + " "

    else:
        words = range(0, segment_length)
        for i in words:
            snippet += second_half[i] + " "

    snippet = snippet[snippet.index(". ") + 2:snippet.rfind(". ") + 1]

    return snippet


if __name__ == "__main__":
    fulltext_dir = r"C:\Users\Adam\Documents\MSU REU\cft"
    kinase_AA_dir = r"C:\Users\Adam\Documents\MSU REU\Comparison_FT\Kinases\Relevant\Post-Processed\BP"
    axis_AA_dir = r"C:\Users\Adam\Documents\MSU REU\FT_Post-Processed\GO"
    input_xml_file = r'C:\Users\Adam\Documents\MSU REU\Task3\task3testdata\BP_test_topics.xml'

    kinase_dict = build_dictionary(input_xml_file)

    for kinase in kinase_dict:
        axis_AA = load_obj(path.join(axis_AA_dir, kinase_dict[kinase] + ".txt.xmi.pkl"))
        kinase_AA = load_obj(path.join(kinase_AA_dir, kinase_dict[kinase] + ".txt.xmi.pkl"))
        start_char, end_char = get_prox_endpoints(kinase, axis_AA, kinase_AA)

        with open(path.join(fulltext_dir, kinase_dict[kinase] + ".txt"), 'r') as f:
            fulltext = f.read().replace('\n', "")

        snip = cut_snippet(start_char, end_char, fulltext)

        print(kinase + "\tBP\t" + kinase_dict[kinase] + "\t" + snip)
