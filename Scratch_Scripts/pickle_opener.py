import pickle

if __name__ == "__main__":
    with open("/data/CM_output/FT/Post-Processed/FV/FT_GO_Train_FV.pkl", "rb") as f:
        unpacked = pickle.load(f)
        print(type(unpacked))
        print(unpacked[0][:5])
        print(unpacked[1][:5])
