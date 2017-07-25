import lxml.etree as etree
import os


def remove_white_space(dict_dirs):

    token = etree.Element("token")

    for dict in os.listdir(dict_dirs):
        root = etree.parse(dict_dirs + "/" + dict)

        for elem in root.iter():
            if elem.tag == "token":
                token = elem
            elif elem.tag == "variant":
                base = elem.attrib.values()[0]
                if " " in base and len(base.split(" ")) < 4:
                    print("base: " + str(elem.attrib.values()[0]))
                    print(base.replace(" ", ""))
                    new_variant = etree.Element("variant", base=base.replace(" ", ""))
                    print(new_variant.attrib)
                    token.append(new_variant)
                    print("")

        with open(dict_dirs + "/" + dict, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
            root.write(f, pretty_print=True)


def roman_numerals_to_numbers(dict_dirs):
    token = etree.Element("token")

    for CMdict in os.listdir(dict_dirs):
        root = etree.parse(dict_dirs + "/" + CMdict)
        print("FILE " + CMdict)

        for elem in root.iter():
            if elem.tag == "token":
                token = elem
            elif elem.tag == "variant":
                base = elem.attrib.values()[0]
                # print(base)
                if " I" in base and base.index(" I") + 2 == len(base):
                    new_base = base[:-1] + "1"
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
                elif " I " in base:
                    index = base.index(" I ")
                    new_base = base[:index + 1] + "1" + base[index - len(base) + 2:]
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
                elif " II" in base and base.index(" II") + 3 == len(base):
                    new_base = base[:-2] + "2"
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
                elif " II " in base:
                    index = base.index(" II ")
                    new_base = base[:index + 1] + "2" + base[index - len(base) + 3:]
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
                elif "III" in base and base.index("III") + 3 == len(base):
                    new_base = base[:-3] + "3"
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
                elif "III" in base:
                    index = base.index("III")
                    new_base = base[:index] + "3" + base[index - len(base) + 3:]
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
                elif " IV" in base and base.index(" IV") + 3 == len(base):
                    new_base = base[:-2] + "4"
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
                elif " IV" in base and base.index(" IV") + 3 == len(base):
                    index = base.index(" IV")
                    new_base = base[:index + 1] + "4" + base[index - len(base) + 3:]
                    new_variant = etree.Element("variant", base=new_base)
                    token.append(new_variant)
                    print(base + "\t" + new_base)
        with open(dict_dirs + "/" + CMdict, "wb") as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
            root.write(f, pretty_print=True)

if __name__ == "__main__":
    dict_dirs = "/data/ConMapDictionaries/Protein Dictionaries/RW_Ext"

    roman_numerals_to_numbers(dict_dirs)
    remove_white_space(dict_dirs)
