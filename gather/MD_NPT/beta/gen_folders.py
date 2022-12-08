import numpy as np
import subprocess

for T in range(1, 301):
    subprocess.run(["mkdir", f"T={T}"])