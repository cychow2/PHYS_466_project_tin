import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

natom_alpha = 5**3 * 8
natom_beta = 6**3 * 4

maxT = 300

S_alpha_pd = pd.read_csv("alpha/S_vs_T.csv")
S_beta_pd = pd.read_csv("beta/S_vs_T.csv")
S_alpha = np.array(S_alpha_pd["S"])
S_beta = np.array(S_beta_pd["S"])

U_alpha_pd = pd.read_csv("alpha/energy_vs_T.csv")
U_beta_pd = pd.read_csv("beta/energy_vs_T.csv")
U_alpha = np.insert(np.array(U_alpha_pd["energy"]), 0, -3.135)
U_beta = np.insert(np.array(U_beta_pd["energy"]), 0, -3.102)

V_alpha_pd = pd.read_csv("alpha/volume_vs_T.csv")
V_beta_pd = pd.read_csv("beta/volume_vs_T.csv")
V_alpha = np.insert(np.array(V_alpha_pd["volume"]), 0, (6.581*5)**3)
V_beta = np.insert(np.array(V_beta_pd["volume"]), 0, (5.873*6)**2 * (3.190*6))
# volume per particle
V_alpha /= natom_alpha
V_beta /= natom_beta

def G(S, U, V, T):
    return U - T * S + V * 6.242e-6

G_alpha_list, G_beta_list = [], []
for T in range(maxT+1):
    G_alpha_list.append(G(S_alpha[T], U_alpha[T], V_alpha[T], T))
    G_beta_list.append(G(S_beta[T], U_beta[T], V_beta[T], T))


def plot():
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Gibbs free energy per atom at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel(r"G/N (eV)")
    ax.plot(range(maxT+1), G_alpha_list, label=r'$\alpha$-tin')
    ax.plot(range(maxT+1), G_beta_list, label=r'$\beta$-tin')
    ax.legend()
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"G_vs_T.png")


def output():
    G_pd = []
    for T in range(maxT+1):
        G_pd.append({"temperature": T, "G alpha": G_alpha_list[T], "G beta": G_beta_list[T]})
        df = pd.DataFrame(G_pd)
        df.to_csv(f"G_vs_T.csv", index=False)

plot()
output()

