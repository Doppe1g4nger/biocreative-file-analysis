import pickle
import numpy as np
import scipy.stats as stats
import pylab as pl
import matplotlib.pyplot as plt


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def plot_hist(h):
    h = sorted(h)
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))
    pl.plot(h, fit, '-o')
    pl.hist(h, normed=True, bins=50)
    pl.show()


def plot_scatter(x_points, y_points):
    plt.scatter(x_points,y_points)
    plt.show()


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


if __name__ == "__main__":
    feat_input = "/data/CM_output/Comparison/Feat/Abst_BP_Rel_Feat.pkl"
    feat_dict = load_obj(feat_input)

    k = []
    a = []
    ka = []
    p = []

    new_compile_lists()

    plot_hist(p)

