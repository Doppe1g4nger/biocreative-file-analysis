"""
Test file for counting num docs, this library does not suite our needs
Gives memory blowup because of bad etree management
"""
import bioc

if __name__ == "__main__":
    file_name = r"/home/daniel/Downloads/abstracts_collection.xml"
    # dtd = r"C:\Users\Danie\Downloads\BioC.dtd"
    with bioc.iterparse(file_name) as parser:
        count = 0
        # collection_info = parser.get_collection_info()
        # print(collection_info.source)
        # print(collection_info.date)
        # print(collection_info.key)
        for document in parser:
            # print(document.id)
            # for key in document.infons:
            #     print(key + "\n" + document.infons[key])
            # for passage in document.passages:
            #     print(passage.infons)
            #     print(passage.text)
            # if count > 0:
            #     break
            count += 1
            if count % 1000 == 0:
                print(count)
    print(count)
