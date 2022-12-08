import observables
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

replot = True
warmup = 20000

if not replot:
    heat_capacity_list = []

    for temperature in range(1, 301):
        print(f"Caculating heat capacity for T = {temperature}", end="\r")
        phase = "beta"
        natom_per_cell = 8 if phase == "alpha" else 4
        natom = 6**3 * natom_per_cell
        

        energies, pressures, volumes, enthalpies = observables.read_observables(natom, phase, temperature)
        enthalpies = energies * natom + volumes * 6.242e-6
        cp = observables.cal_variance(enthalpies, warmup)
        cp /= 8.617333e-5 * temperature**2
        cp *= 1.602176e-19 / (natom / 6.02214e23 * 118.71)

        heat_capacity_list.append(cp)
else:
    heat_capacity_pd = pd.read_csv("heat_capacity_vs_T.csv")
    heat_capacity_list = np.array(heat_capacity_pd["Cp"])

error_heat_capacity_list = heat_capacity_list * np.sqrt(2/(50000-warmup-1))


def plot():
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Constant-pressure heat capacity of $\beta$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel(r"$C_p$ (J K$^{-1}$ g$^{-1}$)")
    ax.errorbar(range(1, 301), heat_capacity_list, error_heat_capacity_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"heat_capacity_vs_T.png")


def output():
    heat_capacity_pd = []
    for temperature in range(1, 301):
        heat_capacity_pd.append({"temperature": temperature, "Cp": heat_capacity_list[temperature-1], "error": error_heat_capacity_list[temperature-1]})
        df = pd.DataFrame(heat_capacity_pd)
        df.to_csv("heat_capacity_vs_T.csv", index=False)


plot()
output()

