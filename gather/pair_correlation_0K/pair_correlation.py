import numpy as np
import matplotlib.pyplot as plt


def minimum_image_disp(dr, lbox):
    """ 
    Impose minimum image condition on displacement vector dr

    Args:
        dr (np.array): (array of) displacement vector ri-rj
        lbox (np.array): side lengths of simulation box
    Returns:
        np.array: pos under MIC
    """
    for i in range(3):
        dr[:,:,i] = dr[:,:,i] - lbox[i] * np.round(dr[:,:,i] / lbox[i])
    return dr


def dist_table(pos, lbox):
    """
    Compute the distance and displacement tables

    Args:
        pos (np.array): particle positions, array of shape (natom, 3)
        lbox (np.array): side lengths of simulation box
    Returns:
        rij (np.array): distance table, rij = distance between particle i and j, array of shape (natom, natom)
        drij (np.array): displacement table, rvij = displacement vector ri - rj, array of shape (natom, natom, 3)
    """
    drij = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
    drij = minimum_image_disp(drij, lbox)
    rij = np.sqrt(np.sum(drij**2, axis=-1))
    return rij, drij


def pair_correlation(dists, natom, nbins, dr, lbox):
    """ Calculate the pair correlation function g(r).

    Args:
        dists (np.array): 1d array of pair distances
        natom (int): number of atoms
        nbins (int): number of bins to histogram
        dr (float): size of bins
        lbox (np.array): side lengths of simulation box
    Return:
        array of shape (nbins,): the pair correlation g(r)
    """
    histogram = np.histogram(dists, bins=nbins, range=(0, nbins*dr))
    r = (histogram[1] + dr/2)[:-1] # centers of the bins
    h = (2/natom) * histogram[0]
    hi = (natom/(lbox[0]*lbox[1]*lbox[2])) * (4*np.pi/3) * dr * (3*r**2 + dr**2/4)
    return h / hi


def read_atom_pos(natom, phase):
    if phase == "beta":
        file = f"../../{phase}/lattice_constant_G_0K/trj.lattice_constant_G_{natom}"
    else:
        file = f"../../{phase}/lattice_constant_G_0K/trj.lattice_constant_{natom}"
    with open(file, "r") as f:
        content = f.read()
        content = content[content.rfind("ITEM: BOX BOUNDS"):]
        content = content.split("\n")
        lbox = np.zeros(3)
        for count, line in enumerate(content[1:4]):
            a, b = line.split()
            a = float(a)
            b = float(b)
            lbox[count] = b - a
        pos = []
        for line in content[5:-1]:
            line = line.split()
            pos.append([float(line[2]), float(line[3]), float(line[4])])
        pos = np.array(pos) * lbox
    return pos, lbox


def plot_g_r(g_r, g_r_axis, filename, phase):
    plt.rcParams.update({'font.size': 20})
    fig = plt.figure(figsize = (16,9))
    ax = fig.gca()
    ax.plot(g_r_axis, g_r)
    max = np.max(g_r)
    if phase == "alpha":
        ax.vlines(2.84965659, 0, max, colors='orange', label=r"NN ($\frac{\sqrt{3}}{4}$ a)", linestyles ='dashed')
    else:
        ax.vlines(np.sqrt((3.18987/4)**2 + (5.873/2)**2), 0, max, colors='orange', label=r"NN ($\sqrt{\left( \frac{c}{4} \right)^2 + \left( \frac{a}{2} \right)^2}$)", linestyles ='dashed')
        ax.vlines(5.873, 0, max, colors='green', label="a", linestyles ='dashed')
    ax.set_title(rf"Pair-correlation function ($\{phase}$, T = 0)")
    ax.set_xlabel("r (Angstrom)")
    ax.set_ylabel("g(r)")
    ax.legend(loc="upper left")
    fig.savefig(filename)


natom = 4000
phase = "beta"
pos, lbox = read_atom_pos(natom=natom, phase=phase)
rij, drij = dist_table(pos, lbox)
flat_triu_rij = np.ndarray.flatten(np.triu(rij, 1))
dists = flat_triu_rij[flat_triu_rij != 0]

nbins = 600
dr = 0.01
g_r = pair_correlation(dists, natom=natom, nbins=nbins, dr=dr, lbox=lbox)
print("Peaks: ", np.nonzero(g_r)[0]*dr+dr/2)
g_r_axis = (np.linspace(0, nbins*dr, nbins+1) + dr/2)[:-1]
plot_g_r(g_r, g_r_axis, f"pair_correlation_{phase}.png", phase=phase)