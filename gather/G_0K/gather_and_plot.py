import numpy as np
import matplotlib.pyplot as plt

alpha_e = []
beta_e = []
n = np.arange(1, 11)

alpha_file = "../../alpha/lattice_constant_G_0K/output.lattice_constant_G"
beta_file = "../../beta/lattice_constant_G_0K/output.lattice_constant_G"
with open(alpha_file, "r") as f:
    for line in f:
        line = line.split()
        alpha_e.append(float(line[-8]))
with open(beta_file, "r") as f:
    for line in f:
        line = line.split()
        beta_e.append(float(line[-8]))

plt.rcParams.update({'font.size': 20})
fig1 = plt.figure(figsize=(16, 9))
ax1 = fig1.gca()
ax1.plot(n, alpha_e, marker='o', label=r'$\alpha$-tin')
ax1.plot(n, beta_e, marker='o', label=r'$\beta$-tin')
ax1.legend()
plt.xlabel("n")
plt.ylabel("G/N (eV)")
plt.title(r"Gibbs free energy per atom for $\alpha$- and $\beta$-tin")
plt.savefig("G_0K.png")
