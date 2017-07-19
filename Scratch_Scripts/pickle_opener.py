import pickle

if __name__ == "__main__":
    with open("/home/daniel/Downloads/FT_Sample_GO_FV.pkl", "rb") as f:
        unpacked = pickle.load(f)
        print(type(unpacked))
        print(unpacked)
