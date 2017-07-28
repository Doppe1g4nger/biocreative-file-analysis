import pickle


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    FV_input = "/data/CM_output/Abst/Post-Processed/FV/Abst_GO_Train_FV.pkl"
    FV_proxcout_input = "/data/CM_output/Abst/Post-Processed/FV/Abst_GO_Train_FV_proxcount.pkl"
    FV_combined_output = "/data/CM_output/Abst/Post-Processed/FV/Abst_GO_Train_FV_combined.pkl"

    fv_dict = load_obj(FV_input)
    fv_proxcount_dict = load_obj(FV_proxcout_input)

    for i in range(0, len(fv_dict[1])):
        fv_dict[1][i].append(fv_proxcount_dict[1][i][1])
        fv_dict[1][i].append(fv_proxcount_dict[1][i][3])
        print(i)

    with open(FV_combined_output, 'wb') as output_file:
        pickle.dump(fv_dict, output_file, pickle.HIGHEST_PROTOCOL)
