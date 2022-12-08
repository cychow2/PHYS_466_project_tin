import numpy as np

# a = 6.646 from materials project
# a = 6.581 from energy minimization
# a = 6.46 from nature paper
a = 6.58142372598779

pos_unit_cell = np.array([
    [0, 0, 0],
    [a/4, a/4, a/4],
    [a/2, 0, a/2],
    [3*a/4, a/4, 3*a/4],
    [a/2, a/2, 0],
    [3*a/4, 3*a/4, a/4],
    [0, a/2, a/2],
    [a/4, 3*a/4, 3*a/4]
])

scale = 10
N = scale**3 * 8

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
{0:6}{np.round(a*scale,6):10} zlo zhi

Atoms
"""

id = 1
for xi in range(scale):
    for yi in range(scale):
        for zi in range(scale):
            pos = np.round(pos_unit_cell + np.array([xi, yi, zi]) * a, 6)
            for atom_pos in pos:
                content += f"\n{id:6}{1:6}{atom_pos[0]:10} {atom_pos[1]:10} {atom_pos[2]:10}"
                id += 1

with open(f"init_datafiles/Sn_alpha_{N}.dat", "w") as data_file:
    data_file.write(content)
