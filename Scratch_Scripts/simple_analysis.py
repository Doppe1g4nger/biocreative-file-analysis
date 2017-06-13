"""
Simple file analysis script, used to count umber of abstracts in abstract collection
"""
if __name__ == "__main__":
    count = 0
    with open("/home/daniel/Downloads/abstracts_collection.xml") as file:
        for line in file:
            cur_index = line.find("<document>")
            while cur_index != -1:
                count += 1
                cur_index = line.find("<document>", cur_index + 1)
            if count % 1000 == 0:
                print(count)
        print(count)
