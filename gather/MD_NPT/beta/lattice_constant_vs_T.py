import observables
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

replot = True

if not replot:
    mean_a_list, error_a_list = [], []
    mean_c_list, error_c_list = [], []

    for temperature in range(1, 301):
        print(f"Caculating lattice constant for T = {temperature}", end="\r")
        phase = "beta"
        natom_per_cell = 8 if phase == "alpha" else 4
        natom = 6**3 * natom_per_cell
        warmup = 20000

        axs, ays, azs = observables.read_a(natom, phase, temperature)
        mean_a, error_a = observables.cal_mean_and_error(axs, warmup)
        mean_c, error_c = observables.cal_mean_and_error(azs, warmup)
        mean_a_list.append(mean_a)
        error_a_list.append(error_a)
        mean_c_list.append(mean_c)
        error_c_list.append(error_c)

    print()

else:
    lattice_constant_pd = pd.read_csv("lattice_constant_vs_T.csv")
    mean_a_list = np.array(lattice_constant_pd["a"])
    error_a_list = np.array(lattice_constant_pd["a error"])
    mean_c_list = np.array(lattice_constant_pd["c"])
    error_c_list = np.array(lattice_constant_pd["c error"])


def plot():
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Lattice constant $a$ of $\beta$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("a (Angstrom)")
    ax.errorbar(range(1, 301), mean_a_list, error_a_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"lattice_constant_a_vs_T.png")

    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Lattice constant $c$ of $\beta$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("a (Angstrom)")
    ax.errorbar(range(1, 301), mean_c_list, error_c_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"lattice_constant_c_vs_T.png")

def output():
    lattice_constant_pd = []
    for temperature in range(1, 301):
        lattice_constant_pd.append({"temperature": temperature, "a": mean_a_list[temperature-1], "a error": error_a_list[temperature-1], \
            "c": mean_c_list[temperature-1], "c error": error_c_list[temperature-1]})
        df = pd.DataFrame(lattice_constant_pd)
        df.to_csv("lattice_constant_vs_T.csv", index=False)

plot()
output()