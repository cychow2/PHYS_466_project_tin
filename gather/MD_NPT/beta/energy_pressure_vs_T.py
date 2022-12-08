import observables
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

replot = True

if not replot:
    mean_energy_list, error_energy_list = [], []
    mean_pressure_list, error_pressure_list = [], []

    for temperature in range(1, 301):
        print(f"Caculating energy and pressure for T = {temperature}", end="\r")
        phase = "beta"
        natom_per_cell = 8 if phase == "alpha" else 4
        natom = 6**3 * natom_per_cell
        warmup = 20000

        energies, pressures, volumes, enthalpies = observables.read_observables(natom, phase, temperature)
        mean_energy, error_energy = observables.cal_mean_and_error(energies, warmup)
        mean_pressure, error_pressure = observables.cal_mean_and_error(pressures, warmup)

        mean_energy_list.append(mean_energy)
        error_energy_list.append(error_energy)
        mean_pressure_list.append(mean_pressure)
        error_pressure_list.append(error_pressure)
        
    print()
else:
    energy_pd = pd.read_csv("energy_vs_T.csv")
    pressure_pd = pd.read_csv("pressure_vs_T.csv")
    mean_energy_list = np.array(energy_pd["energy"])
    error_energy_list = np.array(energy_pd["error"])
    mean_pressure_list = np.array(pressure_pd["pressure"])
    error_pressure_list = np.array(pressure_pd["error"])


def plot():
    plt.rcParams.update({'font.size': 18})
    
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Mean internal energy per atom of $\beta$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("energy (eV)")
    ax.errorbar(range(1, 301), mean_energy_list, error_energy_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"energy_vs_T.png")

    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Measured mean pressure of $\beta$-tin at different temperatures")
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("pressure (bar)")
    ax.errorbar(range(1, 301), mean_pressure_list, error_pressure_list)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"pressure_vs_T.png")


def output():
    energy_pd = []
    for temperature in range(1, 301):
        energy_pd.append({"temperature": temperature, "energy": mean_energy_list[temperature-1], "error": error_energy_list[temperature-1]})
        df = pd.DataFrame(energy_pd)
        df.to_csv("energy_vs_T.csv", index=False)

    pressure_pd = []
    for temperature in range(1, 301):
        pressure_pd.append({"temperature": temperature, "pressure": mean_pressure_list[temperature-1], "error": error_pressure_list[temperature-1]})
        df = pd.DataFrame(pressure_pd)
        df.to_csv("pressure_vs_T.csv", index=False)


plot()
output()

