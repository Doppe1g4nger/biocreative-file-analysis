"""
Scratch script for writing first few lines of fulltext out to a file so we could actually see it
"""
if __name__ == "__main__":
    count = 0
    tot_len = 0
    writer = open(r"/home/daniel/Downloads/first_lines.xml", "w", encoding="utf8")
    with open(r"/home/daniel/Downloads/fulltexts_collection.xml", encoding="utf8") as data:
        for line in data:
            tot_len += len(line)
            writer.write(line)
            # print(line)
            count += 1
            if count >= 7:
                break
        print(tot_len / count)
