import numpy as np

# a = 5.908, c = 3.246 from materials project
# a = 5.851, c = 3.215 from energy minimization
# a = 5.8318, c = 3.1819 from Acta Crystallographica
a = 5.851
c = 3.215

scale = 6
pos_unit_cell = np.array([
    [0, 0, 0],
    [a/2, 0, c/4],
    [a/2, a/2, c/2],
    [a, a/2, 3*c/4]
])

N = scale**3 * 4

content = f"""
{N:6} atoms
{0:6} bonds
{0:6} angles
{0:6} dihedrals
{0:6} impropers

{1:6} atom types
{0:6} bond types
{0:6} angle types
{0:6} dihedral types

{0:6}{np.round(a*scale,6):10} xlo xhi
{0:6}{np.round(a*scale,6):10} ylo yhi
{0:6}{np.round(c*scale,6):10} zlo zhi

Atoms
"""

id = 1
for xi in range(scale):
    for yi in range(scale):
        for zi in range(scale):
            pos = np.round(pos_unit_cell + np.array([xi, yi, 0]) * a + np.array([0, 0, zi]) * c, 6)
            for atom_pos in pos:
                content += f"\n{id:6}{1:6}{atom_pos[0]:10} {atom_pos[1]:10} {atom_pos[2]:10}"
                id += 1

with open(f"init_datafiles/Sn_beta_{N}.dat", "w") as data_file:
    data_file.write(content)