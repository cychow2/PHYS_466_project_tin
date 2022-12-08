import numpy as np
import matplotlib.pyplot as plt

alpha_a = []
beta_a = []
beta_c = []
n = np.arange(1, 11)

alpha_file = "../../alpha/lattice_constant_G_0K/output.lattice_constant_G"
beta_file = "../../beta/lattice_constant_G_0K/output.lattice_constant_G"
with open(alpha_file, "r") as f:
    for line in f:
        line = line.split()
        alpha_a.append(float(line[4]))
with open(beta_file, "r") as f:
    for line in f:
        line = line.split()
        beta_a.append(float(line[4]))
        beta_c.append(float(line[6][:-1]))

plt.rcParams.update({'font.size': 20})
fig1 = plt.figure(figsize=(16, 9))
ax1 = fig1.gca()
ax1.plot(n, alpha_a, marker='o', label=r'$\alpha$-tin')
ax1.plot(n, beta_a, marker='o', label=r'$\beta$-tin')
ax1.legend()
plt.xlabel("n")
plt.ylabel("a (angstrom)")
plt.title(r"Lattice constant $a$ for $\alpha$- and $\beta$-tin")
plt.savefig("lattice_constant_0K_a.png")

fig2 = plt.figure(figsize=(16, 9))
ax2 = fig2.gca()
ax2.plot(n, beta_c, marker='o', label=r'$\beta$-tin')
ax2.legend()
plt.xlabel("n")
plt.ylabel("a (angstrom)")
plt.ylim((3, 3.5))
plt.title(r"Lattice constant $c$ for $\beta$-tin")
plt.savefig("lattice_constant_0K_c.png")
