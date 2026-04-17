import matplotlib.pyplot as plt
import json

with open("build/photon_intensity_core_emission.json", "r") as f:
    photon_intensity_core = json.load(f)

with open("build/photon_intensity_background_emission.json", "r") as f:
    photon_intensity_bg = json.load(f)

photon_intensity_total = []
    
plt.figure(figsize=(10, 5))
plt.title("Intensity of 185.7 keV Photons for Different Configurations")

for key in photon_intensity_bg:
    photon_intensity_total.append(photon_intensity_core[key] + photon_intensity_bg[key])
photon_intensity_bg_list = list(photon_intensity_bg.values())

plt.scatter(photon_intensity_bg_list, [1.01]*len(photon_intensity_bg_list), label="Emission without Core", color="blue")
plt.scatter(photon_intensity_total, [0.99]*len(photon_intensity_total), label="Emission with Core", color="orange")
plt.legend()

plt.xlabel("Photon Intensity (kBq)")
plt.yticks([])
plt.ylim(0.9, 1.1)

plt.savefig("plot.png", dpi=300)

X = []
Y = []
Z = []
for key in photon_intensity_core:
    core_thickness = float(key.split("_")[1])
    radCase_thickness = float(key.split("_")[3])
    X.append(core_thickness)
    Y.append(radCase_thickness)
    Z.append(photon_intensity_core[key]+photon_intensity_bg[key])

ax = plt.figure(figsize=(10, 5)).add_subplot(projection='3d')

ax.scatter(X, Y, Z, color='blue', label='Core Emission')

X = []
Y = []
Z = []
for key in photon_intensity_core:
    core_thickness = float(key.split("_")[1])
    radCase_thickness = float(key.split("_")[3])
    X.append(core_thickness)
    Y.append(radCase_thickness)
    Z.append(photon_intensity_bg[key])


ax.scatter(X, Y, Z, color='orange', label='Background Emission')


plt.xlabel("Core Thickness (cm)")
plt.ylabel("Radiation Case Thickness (cm)")
ax.set_zlabel("Photon Intensity (kBq)")
plt.title("Photon Intensity for Different Configurations")
plt.legend() 
plt.savefig("3d_plot.png", dpi=300)