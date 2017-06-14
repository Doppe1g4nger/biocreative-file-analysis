import pickle
from lxml import etree


def write_to_xml(kinase_dict, f_name):
    """

    :param kinase_dict: dictionary, of kinase id mapped to list of kinase names
    :param f_name: string, file name
    :return: None
    """
    root = etree.Element("synonym")
    for key in kinase_dict:
        token = etree.SubElement(root, "token", id=key,
                                 canonical=kinase_dict[key][0]
                                 )
        token.append(etree.Element("variant", base=key))
        for synonym in kinase_dict[key]:
            if synonym is not None:
                token.append(etree.Element("variant", base=synonym))
    with open(f_name, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
        et = etree.ElementTree(root)
        et.write(f, pretty_print=True)


def load_obj(file_name):
    """
    Loads an object from pickle
    :param file_name: string, name of pckle file to be unpickled
    :return: unpickled object
    """
    with open(file_name, "rb") as f:
        return pickle.load(f)


def print_dict(dictionary):
    """
    Test function for internal use
    :param dictionary: dictionary
    :return: None
    """
    for key, value in dictionary.items():
        for item in value:
            if item is None:
                print(key, value)


if __name__ == "__main__":
    # Load the 8 dictionaries, assignments are fixing broken None items in the dictionaries
    bp_training_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\BP\BP_train_detail.pkl")
    bp_training_dict["NX_Q16654"][2] = r"[Pyruvate dehydrogenase (acetyl-transferring)] kinase isozyme 4, mitochondrial"
    bp_training_ft_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\BP\BP_train_detail_ft.pkl")
    bp_test_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\BP\BP_test_detail.pkl")
    bp_test_dict["NX_Q15349"][3] = r"Ribosomal protein S6 kinase alpha-2"
    bp_test_ft_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\BP\BP_test_detail_ft.pkl")
    dis_training_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\DIS\DIS_train_detail.pkl")
    dis_training_dict["NX_Q16654"][2] = r"[Pyruvate dehydrogenase (acetyl-transferring)] kinase isozyme 4, mitochondrial"
    dis_training_ft_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\DIS\DIS_train_detail_ft.pkl")
    dis_test_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\DIS\DIS_test_detail.pkl")
    dis_test_dict["NX_Q15119"][2] = r"[Pyruvate dehydrogenase (acetyl-transferring)] kinase isozyme 2, mitochondrial"
    dis_test_ft_dict = load_obj(
        r"C:\Users\Danie\Downloads\Training-Test Data Dictionaries\DIS\DIS_test_detail_ft.pkl")
    # Write each dictionary to its ConceptMapper XML format
    write_to_xml(bp_training_dict, r"C:\Users\Danie\Downloads\bp_training_abs.xml")
    write_to_xml(bp_training_ft_dict, r"C:\Users\Danie\Downloads\bp_training_ft.xml")
    write_to_xml(bp_test_dict, r"C:\Users\Danie\Downloads\bp_test_abs.xml")
    write_to_xml(bp_test_ft_dict, r"C:\Users\Danie\Downloads\bp_test_ft.xml")
    write_to_xml(dis_test_dict, r"C:\Users\Danie\Downloads\dis_test_abs.xml")
    write_to_xml(dis_test_ft_dict, r"C:\Users\Danie\Downloads\dis_test_ft.xml")
    write_to_xml(dis_training_dict, r"C:\Users\Danie\Downloads\dis_training_abs.xml")
    write_to_xml(dis_training_ft_dict, r"C:\Users\Danie\Downloads\dis_training_ft.xml")
    # Concatenate training dictionaries and write to XML
    all_training_dict = dict(bp_training_dict)
    all_training_dict.update(bp_training_ft_dict)
    all_training_dict.update(dis_training_ft_dict)
    all_training_dict.update(dis_training_dict)
    write_to_xml(all_training_dict, r"C:\Users\Danie\Downloads\all_training.xml")
    # Concatenate test dictionaries and write to XML
    all_test_dict = dict(bp_test_dict)
    all_test_dict.update(bp_test_ft_dict)
    all_test_dict.update(dis_test_ft_dict)
    all_test_dict.update(dis_test_dict)
    write_to_xml(all_test_dict, r"C:\Users\Danie\Downloads\all_test.xml")
    # Concatenate everything and write to XML
    all_kinases = dict(all_training_dict)
    all_kinases.update(all_test_dict)
    write_to_xml(all_kinases, r"C:\Users\Danie\Downloads\all_kinases.xml")
    # print(len(all_kinases))
    # print_dict(bp_training_ft_dict)
    # print_dict(bp_test_ft_dict)
    # print_dict(bp_test_dict)
    # print_dict(bp_training_dict)
    # print_dict(dis_training_dict)
    # print_dict(dis_training_ft_dict)
    # print_dict(dis_test_ft_dict)
    # print_dict(dis_test_dict)
