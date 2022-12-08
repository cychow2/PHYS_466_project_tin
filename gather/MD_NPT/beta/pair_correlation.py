import numpy as np
import matplotlib.pyplot as plt
import observables


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


def read_atom_pos(natom, temperature, phase, warmup):
    file = f"../../../{phase}/MD_NPT/main_calculation/T={temperature}/trj.MD_{natom}_{temperature}"
    pos_list = []
    lbox_list = []
    with open(file, "r") as f:
        content = f.readlines()
        start_indices = [i for i, line in enumerate(content) if line == "ITEM: BOX BOUNDS pp pp pp\n"]
        for i in range(warmup+1, len(start_indices)):
            if i != len(start_indices)-1:
                current_block = content[start_indices[i]:start_indices[i+1]]
            else:
                current_block = content[start_indices[i]:]

            lbox = np.zeros(3)
            for count, line in enumerate(current_block[1:4]):
                a, b = line.split()
                a = float(a)
                b = float(b)
                lbox[count] = b - a
            pos = []
            for line in current_block[5:-4]:
                line = line.split()
                pos.append([float(line[2]), float(line[3]), float(line[4])])
            pos = np.array(pos) * lbox
            pos_list.append(pos)
            lbox_list.append(lbox)
    return pos_list, lbox_list


def plot_g_r(mean_g_r_list, error_g_r_list, g_r_axis, filename, phase, temperature):
    plt.rcParams.update({'font.size': 20})
    fig = plt.figure(figsize = (16,9))
    ax = fig.gca()
    ax.errorbar(g_r_axis, mean_g_r_list, error_g_r_list)
    max = np.max(g_r)
    ax.vlines(np.sqrt((3.223/4)**2 + (5.866/2)**2), 0, max, colors='orange', label=r"NN ($\sqrt{\left( \frac{c}{4} \right)^2 + \left( \frac{a}{2} \right)^2}$) (cell size)", linestyles ='dashed')
    ax.vlines(5.866, 0, max, colors='green', label="a (cell size)", linestyles ='dashed')
    ax.set_title(rf"Pair-correlation function ($\{phase}$, T = {temperature})")
    ax.set_xlabel("r (Angstrom)")
    ax.set_ylabel("g(r)")
    ax.legend(loc="upper left")
    fig.savefig(filename)


natom = 6**3 * 4
temperature=150
phase = "beta"
warmup = 200
pos_list, lbox_list = read_atom_pos(natom, temperature, phase, warmup)
g_r_list = []

for pos, lbox in zip(pos_list, lbox_list):
    rij, drij = dist_table(pos, lbox)
    flat_triu_rij = np.ndarray.flatten(np.triu(rij, 1))
    dists = flat_triu_rij[flat_triu_rij != 0]

    nbins = 600
    dr = 0.01
    g_r = pair_correlation(dists, natom=natom, nbins=nbins, dr=dr, lbox=lbox)
    g_r_list.append(g_r)
g_r_list = np.array(g_r_list)

mean_g_r_list = []
error_g_r_list = []
for i in range(len(g_r_list[0])):
    mean_g_r, error_g_r = observables.cal_mean_and_error(g_r_list[:,i], 0)
    mean_g_r_list.append(mean_g_r)
    error_g_r_list.append(error_g_r)

g_r_axis = (np.linspace(0, nbins*dr, nbins+1) + dr/2)[:-1]

plot_g_r(mean_g_r_list, error_g_r_list, g_r_axis, f"pair_correlation_{phase}.png", phase, temperature)


