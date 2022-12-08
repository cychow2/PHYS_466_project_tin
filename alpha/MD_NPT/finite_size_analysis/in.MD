# Run energy minimzation to get lattice constants with different N

# Variables
variable run_id loop 6
variable scale index 1 2 3 4 5 6 
variable natom equal (${scale}^3)*8
variable temperature equal 300
variable datafile string init_datafiles/Sn_alpha_${natom}.dat
variable simname string MD_${natom}_${temperature}
log log.${simname}

# Initialization
# print "Running molecular dynamics with scale = ${scale}, N = ${N}, temperature = 300, pressure = 1, datafile = ${datafile}"
units metal
dimension 3
atom_style atomic
pair_style kim MEAM_LAMMPS_KoKimKwon_2018_Sn__MO_129364204512_001
boundary p p p

# System definition
read_data ${datafile}

# Simulation settings
mass 1 118.71
pair_coeff * * Sn
neigh_modify every 1 delay 0 check yes
fix 1 all npt iso 1.0 1.0 5 temp ${temperature} ${temperature} 0.01

# Output settings
variable ax equal lx/${scale}
variable ay equal ly/${scale}
variable az equal lz/${scale}
variable e_per_atom equal etotal/${natom}
variable h equal etotal+press*vol*6.242e-6
thermo 100
thermo_style custom step temp press ke pe etotal vol v_ax v_ay v_az v_e_per_atom v_h
# dump mydmp all atom 100 trj.${simname}

# Run
run 50000
# if "${run_id} == 1" then &
# 'print "The lattice constants are ${ax} ${ay} ${az}; energy per atom is ${e_per_atom} for scale = ${scale}, N = ${N}" file output.lattice_constant_G' &
# else &
# 'print "The lattice constants are ${ax} ${ay} ${az}; energy per atom is ${e_per_atom} for scale = ${scale}, N = ${N}" append output.lattice_constant_G'

# Repeat
clear
next run_id
next scale
jump in.MD