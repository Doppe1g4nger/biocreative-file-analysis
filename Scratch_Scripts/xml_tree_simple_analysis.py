"""
File used to run analysis on fulltext and abstracts, counted num docs, infon types, etc
BioCObject is a more flexible expansion based off this file
"""
import lxml.etree as etree

if __name__ == "__main__":
    # Keeps track of different types of infon, XML tag, and document section
    infon_types = set()
    tag_types = set()
    section_types = set()
    # Used to compute stats on average abstract or abstract title length
    total_abstract_length = 0
    total_abstract_title_length = 0
    # keeps track of total doc number, needed for avg. abstract length
    doc_count = 0
    # Create iterative parser over XML file, fire an event at the end of each tag
    tree = etree.iterparse("/home/daniel/Downloads/fulltexts_collection.xml",
                           events=("end", ))
    # Iteratively parse tree, one element at a time
    for _, element in tree:
        # Keep track of different XML tag types
        tag_types.add(element.tag)
        # Keeps track of different infon types and document section info
        for infon in element.iter("infon"):
            infon_types.add(infon.attrib["key"])
            if infon.attrib["key"] == "type":
                section_types.add(infon.text)
        # Iterate over fully read in documents
        if element.tag == "document":
            # Keep track of document count
            doc_count += 1
            if doc_count % 1000 == 0:
                print(doc_count)
            # For passages, calculate total title and abstract passage length
            # for passage in element.iter("passage"):
            #     passage_type = ""
            #     for infon in passage.iter("infon"):
            #             if infon.attrib["key"] == "type":
            #                 passage_type = infon.text
            #     if passage_type == "TitlePassage":
            #         for text in passage.iter("text"):
            #             total_abstract_title_length += len(text.text.split())
            #     elif passage_type == "AbstractPassage":
            #         for text in passage.iter("text"):
            #             total_abstract_length += len(text.text.split())
            # Flush document to avoid memory blowup
            element.clear()

    # Write relevant data to file
    with open("/home/daniel/Downloads/fulltexts_collection_data1.txt", "w") as file:
        file.write("Number of documents in file:\n" + str(doc_count) + "\n\n")
        file.write("Sorted list of available infon types:\n")
        for inf_type in sorted(infon_types):
            file.write(inf_type + "\n")
        file.write("\n")
        file.write("Sorted list of available tags:\n")
        for tag in sorted(tag_types):
            file.write(tag + "\n")
        file.write("\n")
        file.write("Sorted list of available document subsections:\n")
        for section in sorted(section_types):
            file.write(section + "\n")
        # file.write("\n")
        # file.write("Average abstract title length: "
        #            + str(total_abstract_title_length / doc_count) + "\n")
        # file.write("Average abstract length: "
        #            + str(total_abstract_length / doc_count) + "\n")