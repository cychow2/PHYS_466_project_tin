import numpy as np
import matplotlib.pyplot as plt


def compute_bulk_modulus(volumes, pressures):
    m, c = np.polyfit(volumes, pressures, 1)
    mean_volume = np.mean(volumes)
    bulk_modulus = - mean_volume * m
    return m, c, bulk_modulus


alpha_pressures = []
alpha_volumes = []
beta_pressures = []
beta_volumes = []

alpha_file = "../../alpha/bulk_modulus_0K/output.bulk_modulus"
beta_file = "../../beta/bulk_modulus_0K/output.bulk_modulus"

start = 2
with open(alpha_file, "r") as f:
    for count, line in enumerate(f):
        if count >= start:
            line = line.split()
            alpha_volumes.append(float(line[2][:-1]))
            alpha_pressures.append(float(line[-1]))
with open(beta_file, "r") as f:
    for count, line in enumerate(f):
        if count >= start:
            line = line.split()
            beta_volumes.append(float(line[2][:-1]))
            beta_pressures.append(float(line[-1]))

alpha_volumes = np.array(alpha_volumes)
alpha_pressures = np.array(alpha_pressures)
beta_volumes = np.array(beta_volumes)
beta_pressures = np.array(beta_pressures)
alpha_m, alpha_c, alpha_bulk_modulus = compute_bulk_modulus(alpha_volumes, alpha_pressures)
beta_m, beta_c, beta_bulk_modulus = compute_bulk_modulus(alpha_volumes, alpha_pressures)

# output = f"The bulk modulus is {bulk_modulus:.3f} bar, or {bulk_modulus/1e4:.3f} GPa"
plt.rcParams.update({'font.size': 20})
fig = plt.figure(figsize=(16, 9))
ax = fig.gca()
ax.scatter(alpha_volumes, alpha_pressures, label=r'$\alpha$-tin simulation')
ax.scatter(beta_volumes, beta_pressures, label=r'$\beta$-tin simulation')
ax.plot(alpha_volumes, alpha_m*alpha_volumes+alpha_c, label=r'$\alpha$-tin line of best fit')
ax.plot(beta_volumes, beta_m*beta_volumes+beta_c, label=r'$\beta$-tin line of best fit')
ax.legend()
plt.xlabel("volume (cubic angstrom)")
plt.ylabel("pressure (bar)")
plt.title(r"Pressure-volume curve of $\alpha$ and $\beta$-tin")
plt.savefig("pressure-volume_0K.png")
    
    