import observables
import matplotlib.pyplot as plt
import numpy as np

phase = "alpha"
natom_per_cell = 8 if phase == "alpha" else 4
natom_list = np.arange(1, 7)**3 * natom_per_cell
temperature = 300
warmup = 20000

mean_energy_list, error_energy_list = [], []
mean_pressure_list, error_pressure_list = [], []
mean_volume_list, error_volume_list = [], []
mean_enthalpy_list, error_enthalpy_list = [], []

for natom in natom_list:
    energies, pressures, volumes, enthalpies = observables.read_observables(natom, phase, temperature)
    enthalpies /= natom # enthalpies per atom
    mean_energy, error_energy = observables.cal_mean_and_error(energies, warmup)
    mean_pressure, error_pressure = observables.cal_mean_and_error(pressures, warmup)
    mean_volume, error_volume = observables.cal_mean_and_error(volumes, warmup)
    mean_enthalpy, error_enthalpy = observables.cal_mean_and_error(enthalpies, warmup)

    mean_energy_list.append(mean_energy)
    error_energy_list.append(error_energy)
    mean_pressure_list.append(mean_pressure)
    error_pressure_list.append(error_pressure)
    mean_volume_list.append(mean_volume)
    error_volume_list.append(error_volume)
    mean_enthalpy_list.append(mean_enthalpy)
    error_enthalpy_list.append(error_enthalpy)
    

plt.rcParams.update({'font.size': 18})
fig = plt.figure(figsize = (16, 9))
ax = fig.gca()
ax.set_title(rf"Energy per atom vs cell size")
ax.set_xlabel("natom")
ax.set_ylabel("energy (eV)")
ax.errorbar(natom_list, mean_energy_list, error_energy_list, marker='o')
ax.ticklabel_format(useOffset=False, style='plain')
fig.savefig(f"energy_size_{phase}.png")

fig = plt.figure(figsize = (16, 9))
ax = fig.gca()
ax.set_title(rf"Volume vs cell size")
ax.set_xlabel("natom")
ax.set_ylabel("volume (cubic Angstrom)")
ax.errorbar(natom_list, mean_volume_list, error_volume_list, marker='o')
ax.ticklabel_format(useOffset=False, style='plain')
fig.savefig(f"volume_size_{phase}.png")

plt.rcParams.update({'font.size': 18})
fig = plt.figure(figsize = (16, 9))
ax = fig.gca()
ax.set_title(rf"Enthalpy per atom vs cell size")
ax.set_xlabel("natom")
ax.set_ylabel("enthalpy (eV)")
ax.errorbar(natom_list, mean_enthalpy_list, error_enthalpy_list, marker='o')
ax.ticklabel_format(useOffset=False, style='plain')
fig.savefig(f"enthalpy_size_{phase}.png")

fig = plt.figure(figsize = (16, 9))
ax = fig.gca()
ax.set_title(rf"Measured pressure vs cell size")
ax.set_xlabel("natom")
ax.set_ylabel("measured pressure (bar)")
ax.errorbar(natom_list, mean_pressure_list, error_pressure_list, marker='o')
ax.ticklabel_format(useOffset=False, style='plain')
fig.savefig(f"pressure_size_{phase}.png")