import numpy as np
import helper

def read_observables(natom, phase, temperature, timestep):
    file = f"../../../{phase}/MD_NPT/time_step_analysis/log.MD_{natom}_{temperature}_{timestep}"
    with open(file, "r") as f:
        content = f.read()
        start = content.find("Step Temp Press KinEng PotEng TotEng Volume v_ax v_ay v_az v_e_per_atom v_h")
        end = content.find("Loop time of")
        content = content[start:end].split("\n")
        energies, pressures, volumes, enthalpies = [], [], [], []
        for line in content[1:-1]:
            energies.append(float(line.split()[10]))
            pressures.append(float(line.split()[2]))
            volumes.append(float(line.split()[6]))
            enthalpies.append(float(line.split()[11]))
        energies = np.array(energies)
        pressures = np.array(pressures)
        volumes = np.array(volumes)
        enthalpies = np.array(enthalpies)
    return energies, pressures, volumes, enthalpies


def cal_mean_and_error(data, warmup, dump_freq=100):
    warmup = warmup // dump_freq
    data = data[warmup+1:]
    mean = np.mean(data)
    error = helper.stand_error(data)
    return mean, error





