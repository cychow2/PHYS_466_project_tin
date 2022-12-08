import observables
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


cp_pd = pd.read_csv("heat_capacity_vs_T.csv")
cp_list = np.array(cp_pd["Cp"])


def S(cp_list, T):
    # trapezoidal rule
    integrand = cp_list / np.arange(1, 301)
    integrand = np.insert(np.array(integrand), 0 , 0)
    entropy = np.sum(integrand[:T+1]) - integrand[T] / 2
    # convert from J K^-1 g^-1 to eV K^-1 per atom
    entropy *= 118.71 / 6.02214e23 / 1.602176e-19
    return entropy

S_list = []
for T in range(301):
    S_list.append(S(cp_list, T))

# print(S_list)

def plot():
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Entropy per atom of $\beta$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel(r"S/N (eV K$^{-1}$)")
    ax.plot(range(301), S_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"S_vs_T.png")


def output():
    S_pd = []
    for T in range(301):
        S_pd.append({"temperature": T, "S": S_list[T]})
        df = pd.DataFrame(S_pd)
        df.to_csv("S_vs_T.csv", index=False)

plot()
output()

