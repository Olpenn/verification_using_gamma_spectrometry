import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import numpy as np


U_photon_energy = []
U_attenuation = []
Be_photon_energy = []
Be_attenuation = []

with open("U_attenuation.txt", "r") as f:
    in_data = False
    for line in f:
        if line == "\n":
            in_data = True
            continue
        if not in_data:
            continue
        data = line.split("|")[:2]
        U_photon_energy.append(float(data[0]))
        U_attenuation.append(float(data[1]))

with open("Be_attenuation.txt", "r") as f:
    in_data = False
    for line in f:
        if line == "\n":
            in_data = True
            continue
        if not in_data:
            continue
        data = line.split("|")[:2]
        Be_photon_energy.append(float(data[0]))
        Be_attenuation.append(float(data[1]))

plt.figure(figsize=(10,5))
ax = plt.gca()

plt.title('Attenuation coefficient for U and Be')
ax.set_xscale('log')
ax.set_yscale('log')
plt.xlabel('Photon Energy (MeV)')
plt.ylabel(r'Attenuation Coefficient (cm$^2$/g)')
plt.plot(U_photon_energy, U_attenuation, label="U (z=92)", color="g")
plt.plot(Be_photon_energy, Be_attenuation, label="Be (z=4)", color="k")



plt.legend()
plt.savefig("Attenuation_coeff.png")


