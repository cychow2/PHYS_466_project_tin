import numpy as np

content = ""
for a in range(1, 9):
    Tmax = 300 - 38*(a-1)
    Tmin = 300 - 38*a + 1
    if Tmin < 0:
        Tmin = 1

    batch_size = 12
    T = Tmax
    Tstop = T - batch_size + 1
    content = ""
    
    while not T < Tmin:
        content += f"echo \"running T={T} to T={Tstop}\" \n"
        while not T < Tstop:
            content += f"sh T={T}/run &>> T={T}/out.MD & \n"
            T -= 1
        Tstop -= 12
        if Tstop < Tmin:
            Tstop = Tmin
        content += "sleep 2160 \n \n"

    with open(f"master_run_0{a-1}", "w") as f:
        f.write(content)
