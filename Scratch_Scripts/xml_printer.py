"""
Simple script used to write first fulltext document to a file to view its structure
"""
import lxml.etree as etree

if __name__ == "__main__":
    cnt = 0
    with open("/home/daniel/Downloads/fulltexts_collection.xml", "rb") as file:
        fulltext = etree.iterparse(file, events=("end", ))
        for _, elem in fulltext:
            cnt += 1
            if elem.tag == "document":
                with open("/home/daniel/Downloads/test.txt", "w") as temp:
                    bytestring = etree.tostring(elem, pretty_print=True)
                    temp.write(bytestring.decode("utf8"))
                break
