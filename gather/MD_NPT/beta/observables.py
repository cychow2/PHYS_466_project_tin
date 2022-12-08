import numpy as np
import helper

def read_observables(natom, phase, temperature):
    file = f"../../../{phase}/MD_NPT/main_calculation/T={temperature}/log.MD_{natom}_{temperature}"
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


def read_a(natom, phase, temperature):
    file = f"../../../{phase}/MD_NPT/main_calculation/T={temperature}/log.MD_{natom}_{temperature}"
    with open(file, "r") as f:
        content = f.read()
        start = content.find("Step Temp Press KinEng PotEng TotEng Volume v_ax v_ay v_az v_e_per_atom v_h")
        end = content.find("Loop time of")
        content = content[start:end].split("\n")
        axs, ays, azs = [], [], []
        for line in content[1:-1]:
            axs.append(float(line.split()[7]))
            ays.append(float(line.split()[8]))
            azs.append(float(line.split()[9]))
        axs = np.array(axs)
        ays = np.array(ays)
        azs = np.array(azs)
    return axs, ays, azs


def cal_mean_and_error(data, warmup, dump_freq=1):
    warmup = warmup // dump_freq
    data = data[warmup+1:]
    mean = np.mean(data)
    error = helper.stand_error(data)
    return mean, error

def cal_variance(data, warmup, dump_freq=1):
    warmup = warmup // dump_freq
    data = data[warmup+1:]
    var = np.var(data)
    return var





