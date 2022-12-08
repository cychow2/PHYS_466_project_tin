import observables
import matplotlib.pyplot as plt
import numpy as np

phase = "beta"
natom_per_cell = 8 if phase == "alpha" else 4
natom = 6**3 * natom_per_cell

for temperature in range(282, 301):
    print(f"Plotting energies, pressures and volumes for T={temperature}", end="\r")

    energies, pressures, volumes, enthalpies = observables.read_observables(natom, phase, temperature)
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Energy per atom")
    ax.set_xlabel("step")
    ax.set_ylabel("energy (eV)")
    ax.plot(range(0, 50001), energies)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"T={temperature}/energies.png")
    plt.close(fig)

    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Measured pressure")
    ax.set_xlabel("step")
    ax.set_ylabel("pressure (bar)")
    ax.plot(range(0, 50001), pressures)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"T={temperature}/pressures.png")
    plt.close(fig)

    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Volume")
    ax.set_xlabel("step")
    ax.set_ylabel("volume (cubic angstrom)")
    ax.plot(range(0, 50001), volumes)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"T={temperature}/volumes.png")
    plt.close(fig)

    enthalpies = energies * natom + volumes * 6.242e-6

    fig = plt.figure(figsize = (16, 9))
    ax = fig.gca()
    ax.set_title(rf"Enthalpy")
    ax.set_xlabel("step")
    ax.set_ylabel("energy (eV)")
    ax.plot(range(0, 50001), enthalpies)
    ax.ticklabel_format(useOffset=False, style='plain')
    fig.savefig(f"T={temperature}/enthalpies.png")
    plt.close(fig)

print()