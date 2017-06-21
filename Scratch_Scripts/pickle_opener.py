import pickle

if __name__ == "__main__":
    with open("/home/daniel/Downloads/PickleFiles/NCITerms.pkl", "rb") as f:
        unpacked = pickle.load(f)
        print(type(unpacked))
        print(unpacked)