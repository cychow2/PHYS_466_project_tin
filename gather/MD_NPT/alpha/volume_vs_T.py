import observables
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mean_volume_list, error_volume_list = [], []

for temperature in range(1, 301):
    print(f"Caculating volume for T = {temperature}", end="\r")
    phase = "alpha"
    natom_per_cell = 8 if phase == "alpha" else 4
    natom = 5**3 * natom_per_cell
    warmup = 20000

    energies, pressures, volumes, enthalpies = observables.read_observables(natom, phase, temperature)
    mean_volume, error_volume = observables.cal_mean_and_error(volumes, warmup)

    mean_volume_list.append(mean_volume)
    error_volume_list.append(error_volume)

print()

def plot():
    plt.rcParams.update({'font.size': 18})
    
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Mean volume of $\alpha$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("volume (cubic Angstrom)")
    ax.errorbar(range(1, 301), mean_volume_list, error_volume_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"volume_vs_T.png")


def output():
    volume_pd = []
    for temperature in range(1, 301):
        volume_pd.append({"temperature": temperature, "volume": mean_volume_list[temperature-1], "error": error_volume_list[temperature-1]})
        df = pd.DataFrame(volume_pd)
        df.to_csv("volume_vs_T.csv", index=False)



plot()
output()

