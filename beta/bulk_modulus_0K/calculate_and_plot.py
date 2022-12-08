import numpy as np
import matplotlib.pyplot as plt


def compute_bulk_modulus(volumes, pressures):
    m, c = np.polyfit(volumes, pressures, 1)
    mean_volume = np.mean(volumes)
    bulk_modulus = - mean_volume * m
    return m, c, bulk_modulus


def plot(volumes, pressures, m, c):
    plt.rcParams.update({'font.size': 20})
    fig = plt.figure(figsize=(16, 9))
    ax = fig.gca()
    ax.scatter(volumes, pressures, label='simulation results')
    ax.plot(volumes, m*volumes+c, label='line of best fit')
    ax.legend()
    plt.xlabel("volume (cubic angstrom)")
    plt.ylabel("pressure (bar)")
    plt.title(r"Pressure-volume curve of $\beta$-tin")
    plt.savefig("pressure-volume.png")


if __name__ == "__main__":
    pressures = []
    volumes = []
    start = 2
    with open("output.bulk_modulus", "r") as f:
        for count, line in enumerate(f):
            if count >= start:
                line = line.split()
                pressures.append(float(line[2][:-1]))
                volumes.append(float(line[-1]))
    volumes = np.array(volumes)
    pressures = np.array(pressures)
    m, c, bulk_modulus = compute_bulk_modulus(volumes, pressures)
    output = f"The bulk modulus is {bulk_modulus:.3f} bar, or {bulk_modulus/1e4:.3f} GPa"
    print(output)
    with open("bulk_modulus", "w") as f:
        f.write(output)
    plot(volumes, pressures, m, c)
    
    