import lxml.etree as etree


class BioCObject:
    # Keeps track of different types of infon, XML tag, and document section
    infon_types = set()
    tag_types = set()
    section_types = set()
    # Used to compute stats on average abstract or abstract title length
    total_abstract_length = 0
    total_abstract_title_length = 0
    filename = ""
    # keeps track of total doc number, needed for avg. abstract length
    doc_count = 0
    tree = None

    # Constructor; takes a bioc formatted xml path
    def __init__(self, filename):
        self.filename = filename
        # Create iterative parser over XML file, fire an event at the end of each tag
        self.tree = etree.iterparse(self.filename, events=("end", ))

    # Iteratively parse tree, one element at a time
    def run_analytics(self, output_file="Analytics.txt"):
        for _, element in self.tree:
            # Keep track of different XML tag types
            self.tag_types.add(element.tag)
            # Keeps track of different infon types and document section info
            for infon in element.iter("infon"):
                self.infon_types.add(infon.attrib["key"])
                if infon.attrib["key"] == "type":
                    self.section_types.add(infon.text)
            # Iterate over fully read in documents
            if element.tag == "document":
                # Keep track of document count
                self.doc_count += 1
                if self.doc_count % 1000 == 0:
                    print(self.doc_count)
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
        with open(output_file, "w") as file:
            file.write("Number of documents in file:\n" + str(self.doc_count) + "\n\n")
            file.write("Sorted list of available infon types:\n")
            for inf_type in sorted(self.infon_types):
                file.write(inf_type + "\n")
            file.write("\n")
            file.write("Sorted list of available tags:\n")
            for tag in sorted(self.tag_types):
                file.write(tag + "\n")
            file.write("\n")
            file.write("Sorted list of available document subsections:\n")
            for section in sorted(self.section_types):
                file.write(section + "\n")
            # file.write("\n")
            # file.write("Average abstract title length: "
            #            + str(total_abstract_title_length / doc_count) + "\n")
            # file.write("Average abstract length: "
            #            + str(total_abstract_length / doc_count) + "\n")

    # Returns a dictionary with {(PMID: Abstract), ...}
    def collect_abstracts(self):
        currentID = ""
        abstracts_dict = {}
        collect_passage = False

        for _, element in self.tree:

            if element.tag == "id":
                currentID = element.text

            elif element.text == "AbstractPassage":
                collect_passage = True

            elif collect_passage and element.tag == "text":
                abstracts_dict[currentID] = element.text
                collect_poassage = False

        return abstracts_dict

    # Returns a dictionary with {(PMID: Title), ...}
    def collect_titles(self):
        current_id = ""
        title_dict = {}
        collect_passage = False

        for _, element in self.tree:

            if element.tag == "id":
                current_id = element.text

            elif element.text == "TitlePassage":
                collect_passage = True

            elif collect_passage and element.tag == "text":
                title_dict[current_id] = element.text
                collect_passage = False

        return title_dict

    # Returns a dictionary with {(PMID: [infon1, infon2, infon3, ...]), ...}
    def collect_infons(self):
        current_id = ""
        infon_dict = {}

        for _, element in self.tree:

            if element.tag == "id":
                current_id = element.text

            elif element.tag == "infon":
                try:
                    infon_dict[current_id].append(element.text)
                except KeyError:
                    infon_dict[current_id] = [element.text]

        return infon_dict
