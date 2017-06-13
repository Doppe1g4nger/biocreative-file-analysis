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

    # Prints a data analytics sheet to output_file
    # Iterative, so only a small amount of RAM used
    def run_analytics(self, ouput_file="Analytics.txt"):
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
        with open(ouput_file, "w") as file:
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

    # Returns a dictionary with {(PMID: QUANTITY), ...}
    # tag_text  argument represents the desired keyword for whatever QUANTITY you need
    # examples are, "AbstractPassage", "Title Passage", etc
    # Primary use with abstracts_collection
    def collect_all(self, tag_text):
        currentID = ""
        dict = {}
        collect_passage = False

        for _, element in self.tree:

            if element.tag == "id":
                currentID = element.text

            elif element.text == tag_text:
                collect_passage = True

            elif collect_passage and element.tag == "text":
                dict[currentID] = element.text
                collect_passage = False
            element.clear()

        return dict

    # Returns a specific quantity based on tag_text (the desired type) and document_index, where it is stored.
    # To return the 140th Abstract, for example, call collect_by_index("AbstractPassage", 140)
    def collect_by_index(self, tag_text, document_index):
        correct_index = False
        correct_passage = False
        doc_count = -1

        for _, element in self.tree:

            if not correct_index and element.tag == "document":
                doc_count += 1

                if doc_count == document_index:
                    correct_index = True

            elif correct_index and element.text == tag_text:
                correct_passage = True

            elif correct_passage and correct_index and element.tag == "text":
                return element.text
            element.clear()

    # Returns a specific quantity based on tag_text (the desired type) and PMID
    # To return the Abstract of PMID 18183754, for example, call collect_by_index("AbstractPassage", 18183754)
    # PMID can be entered with or without quotes
    def collect_by_id(self, tag_text, PMID):
        correct_index = False
        correct_passage = False

        for _, element in self.tree:

            if not correct_index and element.tag == "id":
                if element.text == str(PMID):
                    correct_index = True

            elif correct_index and element.text == tag_text:
                correct_passage = True

            elif correct_passage and correct_index and element.tag == "text":
                return element.text
            element.clear()

    # Returns a dictionary with {(PMID: Title), ...}
    # This is a title specific shortcut of the collect_all function
    # primarily for abstacts_collection
    def titles(self):
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
            element.clear()

        return title_dict

    # Returns a dictionary with {(PMID: Abstract), ...}
    # This is an abstract specific shortcut of the collect_all function
    # primarily for abstacts_collection
    def abstracts(self):
        current_id = ""
        dict = {}
        collect_passage = False

        for _, element in self.tree:

            if element.tag == "id" :
                current_id = element.text

            elif element.text == "AbstractPassage" or element.text == "abstract":
                collect_passage = True

            elif collect_passage and element.tag == "text":
                dict[current_id] = element.text
                collect_passage = False
            element.clear()

        return dict

    # Returns a dictionary with {(PMID: [infon1, infon2, infon3, ...]), ...}
    # Designed and testes with abstacts_collection
    def infons(self):
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
            element.clear()

        return infon_dict
    
    # Counts total number of documents using <document> tags 
    # Testes with both abstracts and fulltext
    def number_of_documents(self):
        count = 0

        for _, element in self.tree:
            if element.tag == "document":
                count += 1

            element.clear()

        return count

    # returns a dictionary of {(PMID: ParagraphText), ...}
    # Where ParagraphText text represents all paragraphs associated with that PMID concatenated together 
    # designed for fulltext
    def paragraphs_text(self):
        current_id = ""
        dict = {}
        collect_text = False

        for _, element in self.tree:

            if not collect_text and element.tag == "id":
                current_id = element.text[3:]

            elif not collect_text and element.text == "paragraph":
                collect_text = True;

            elif collect_text and element.tag == "text":
                try:
                    dict[current_id] += element.text
                except KeyError:
                    dict[current_id] = element.text
                collect_text = False;
            element.clear()

        return dict

    # accepts a list of desired tags to include (list_of_relevant_tags),
    # and a boolean value or whether or not to include the keywords text for each document
    # returns a dictionary of {(PMID: BagOfText), ...}
    # Where BagOfText text represents all texts from all desires and keywords iff include_keywords = True
    # designed for fulltext
    def full_docs_parser(self, list_of_relevant_tags, include_keywords):
        current_id = ""
        dict = {}
        collect_text = False

        for _, element in self.tree:

            if not collect_text and element.tag == "id":
                current_id = element.text[3:]

            elif not collect_text and element.text in list_of_relevant_tags:
                collect_text = True;

            elif collect_text and element.tag == "text":
                try:
                    dict[current_id] += element.text
                except KeyError:
                    dict[current_id] = element.text
                collect_text = False;
            elif include_keywords and element.attrib == {'key': 'kwd'}:
                try:
                    dict[current_id] += element.text
                except KeyError:
                    dict[current_id] = element.text

            element.clear()

        return dict

    # returns dictionary of {(PMID: keywords), ...} 
    # where keywords is the group of text associated with the "kwd" infon tag 
    # designed for fulltext
    def keywords(self):
        current_id = ""
        dict = {}

        for _, element in self.tree:

            if element.tag == "id":
                current_id = element.text[3:]

            elif element.attrib == {'key': 'kwd'}:
                dict[current_id] = element.text

            element.clear()

        return dict
