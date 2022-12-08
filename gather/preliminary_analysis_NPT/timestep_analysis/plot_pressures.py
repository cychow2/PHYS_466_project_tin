import observables
import matplotlib.pyplot as plt
import numpy as np

phase = "alpha"
natom_per_cell = 8 if phase == "alpha" else 4
scale = 3
natom = 3**3 * natom_per_cell
# timestep_list = [0.01, 0.001, 0.0005, 0.0001]
timestep_list = [0.01, 0.005, 0.001, 0.0005]
temperature = 300


for timestep in timestep_list:
    nstep = round(50/timestep)
    energies, pressures, volumes, enthalpies = observables.read_observables(natom, phase, temperature, timestep)
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Measured pressure, T={temperature}")
    ax.set_xlabel("step")
    ax.set_ylabel("pressure (bar)")
    ax.plot(range(0, nstep+1, 100), pressures, label=f"timestep = {timestep}")
    ax.ticklabel_format(useOffset=False, style='plain')
    ax.legend()
    fig.savefig(f"pressure_vs_step_tstep={timestep}.png")