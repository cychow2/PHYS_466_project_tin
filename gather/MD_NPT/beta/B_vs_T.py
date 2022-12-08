import observables
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

B_list = []

for temperature in range(1, 301):
    print(f"Caculating bulk modulus for T = {temperature}", end="\r")
    phase = "beta"
    natom_per_cell = 8 if phase == "alpha" else 4
    natom = 6**3 * natom_per_cell
    warmup = 20000

    energies, pressures, volumes, enthalpies = observables.read_observables(natom, phase, temperature)
    mean_volume, _ = observables.cal_mean_and_error(volumes, warmup)
    volume_var = observables.cal_variance(volumes, warmup)

    B_list.append(1.380649e-23 * temperature * mean_volume / (volume_var*1e-30) * 1e-9)
    

def plot():
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Bulk modulus of $\beta$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel(r"$B$ (GPa)")
    ax.plot(range(1, 301), B_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"B_vs_T.png")


def output():
    B_pd = []
    for temperature in range(1, 301):
        B_pd.append({"temperature": temperature, "B": B_list[temperature-1]})
        df = pd.DataFrame(B_pd)
        df.to_csv("B_vs_T.csv", index=False)


plot()
output()

