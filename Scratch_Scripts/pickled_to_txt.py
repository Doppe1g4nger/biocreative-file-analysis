import pickle

if __name__ == "__main__":
    file_names = [
        "/home/daniel/Downloads/PickleFiles/"
        "Irrelevant Abstracts/bp_irrelevant_abstracts.pkl",
        "/home/daniel/Downloads/PickleFiles/"
        "Irrelevant Abstracts/dis_irrelevant_abstracts.pkl",
        "/home/daniel/Downloads/PickleFiles/"
        "Training Abstracts/bp_training_abstracts.pkl",
        "/home/daniel/Downloads/PickleFiles/"
        "Training Abstracts/dis_training_abstracts.pkl"
    ]
    for file in file_names:
        with open(file, "rb") as f:
            data = pickle.load(f)
            file_path = ""
            if file.split("/")[-1].startswith("bp_irrelevant"):
                file_path = "/home/daniel/Downloads/Training&IrrelevantAbstracts/Irrelevant Abstracts/BP/"
            elif file.split("/")[-1].startswith("dis_irrelevant"):
                file_path = "/home/daniel/Downloads/Training&IrrelevantAbstracts/Irrelevant Abstracts/DIS/"
            elif file.split("/")[-1].startswith("bp_training"):
                file_path = "/home/daniel/Downloads/Training&IrrelevantAbstracts/Training Abstracts/BP/"
            else:
                file_path = "/home/daniel/Downloads/Training&IrrelevantAbstracts/Training Abstracts/DIS/"
            for item in data:
                with open(file_path + item + ".txt", "w") as outfile:
                    outfile.write(data[item])
