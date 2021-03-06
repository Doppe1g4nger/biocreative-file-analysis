import pickle
import numpy as np
import scipy.stats as stats
import pylab as pl
import matplotlib.pyplot as pp
import matplotlib.patches as mpatches


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def plot_hist(h):
    h = sorted(h)
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))
    pl.plot(h, fit, '-o')
    pl.hist(h, normed=True, bins='auto')
    pl.xlabel("Kinase Score")
    pl.ylabel("Number of Documents")
    pl.show()


def scatter(x1, y1, title="Proximity vs. Relevancy Score", x2=0, y2=0,):
    pp.plot(x1, y1, 'bs', x2, y2, 'r^')
    pp.xlabel('Proximity')
    pp.ylabel('Relevancy Score')
    rel = mpatches.Patch(color='blue', label='Relevant')
    irr = mpatches.Patch(color='red', label='Irrelevant')
    pp.legend(handles=[rel, irr])
    pp.title(title)
    pp.show()


def plot_feature_vector(path, title=""):
    fv = load_obj(path)
    features = fv[1]
    labels = fv[0]
    x_rel = []
    x_irr = []
    y_rel = []
    y_irr = []

    for i in range(0, len(labels) - 1):
        if labels[i] == 0:
            x_irr.append(features[i][0])
            y_irr.append(features[i][3])
        else:
            x_rel.append(features[i][0])
            y_rel.append(features[i][3])
    print(len(x_rel))

    plot_hist(x_rel)
    plot_hist(x_irr)
    pp.plot(x_irr, y_irr, 'r^', x_rel, y_rel, 'bs')
    pp.xlabel('Proximity')
    pp.ylabel('Relevancy Score')
    rel = mpatches.Patch(color='blue', label='Relevant')
    irr = mpatches.Patch(color='red', label='Irrelevant')
    pp.legend(handles=[rel, irr])
    pp.title(title)
    pp.show()


def old_compile_lists():
    for kinase in feat_dict:
        for doc in feat_dict[kinase]:
            k.append(doc[1][0])
            a.append(doc[1][1])
            ka.append(doc[1][2])
            p.append(doc[2][0])


def new_compile_lists():
    for kinase in feat_dict:
        for doc in feat_dict[kinase]:
            k.append(doc[1])
            a.append(doc[2])
            ka.append(doc[3])
            p.append(doc[4])

    for kinase in dict2:
        for doc in dict2[kinase]:
            k2.append(doc[1])
            a2.append(doc[2])
            ka2.append(doc[3])
            p2.append(doc[4])


if __name__ == "__main__":
    feat_input = r"/data/CM_output/FT/Post-Processed/FV/FT_GO_Train_FV.pkl"
    #input2 = r"C:\Users\Adam\Documents\MSU REU\Comparison_Abst\Feat\Abst_Sample_HP_Rel_Feat.pkl"
    feat_dict = load_obj(feat_input)
    #dict2 = load_obj(input2)

    k = []
    a = []
    ka = []
    p = []

    k2 = []
    a2 = []
    ka2 = []
    p2 = []

    plot_feature_vector(feat_input)
    # scatter(p2, ka2, "HP Relevant vs. Irrelevant FullText Samples", p, ka)

