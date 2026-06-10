import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import json
import numpy as np


with open("../run/data/metadata.json", "r") as f:
    metadata = json.load(f)


def core_case_emission_detection_plot(metadata):
    photon_detection_core_185 = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_detection_core_1001 = []  # Array consists of values of the form detected_core_emission_185.7keV
    photon_detection_case_185 = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_detection_case_1001 = []  # Array consists of values of the form detected_core_emission_185.7keV
    for geometry in metadata.values():
        photon_detection_core_185.append(geometry["detected_core_emission_185.7keV"])
        photon_detection_core_1001.append(geometry["detected_core_emission_1001.0keV"])
        photon_detection_case_185.append(geometry["detected_background_emission_185.7keV"])
        photon_detection_case_1001.append(geometry["detected_background_emission_1001.0keV"])


    plt.figure(figsize=(10, 5))
    plt.title("Detected 185.7 keV photons from a core and a DU core")
    photon_detection_core_185 = np.array(photon_detection_core_185)
    photon_detection_case_185 = np.array(photon_detection_case_185)

    bins_core = np.logspace(np.log10(photon_detection_core_185.min()), np.log10(photon_detection_core_185.max()), 50)
    plt.hist(photon_detection_core_185, 
             bins=bins_core, 
             edgecolor='black',
             linewidth=0.8,
             histtype='stepfilled',
             label='Core',
             color='orange')
    bins_case = np.logspace(np.log10(photon_detection_case_185.min()), np.log10(photon_detection_case_185.max()), 50)
    plt.hist(photon_detection_case_185, 
             edgecolor='black',
             linewidth=0.8,
             bins=bins_case, 
             histtype='stepfilled',
             label='Case',
             color='blue')
    
    plt.legend()

    plt.xlabel("185.7 keV Photon Intensity ($s^{-1}$)")
    plt.ylabel("Count")
    plt.xscale('log')

    plt.savefig(f"Detection_185keV.png", dpi=300)

    plt.figure(figsize=(10, 5))
    plt.title("Detected 1001 keV photons from a core and a DU core")
    photon_detection_core_1001 = np.array(photon_detection_core_1001)
    photon_detection_case_1001 = np.array(photon_detection_case_1001)

    bins_core = np.logspace(np.log10(photon_detection_core_1001.min()), np.log10(photon_detection_core_1001.max()), 50)
    plt.hist(photon_detection_core_1001, 
             bins=bins_core, 
             edgecolor='black',
             linewidth=0.8,
             histtype='stepfilled',
             label='Core',
             color='orange')
    bins_case = np.logspace(np.log10(photon_detection_case_1001.min()), np.log10(photon_detection_case_1001.max()), 50)
    plt.hist(photon_detection_case_1001, 
             edgecolor='black',
             linewidth=0.8,
             bins=bins_case, 
             histtype='stepfilled',
             label='Case',
             color='blue')
    
    plt.legend()

    plt.xlabel("1001 keV Photon Intensity ($s^{-1}$)")
    plt.ylabel("Count")
    plt.xscale('log')

    plt.savefig(f"Detection_1001keV.png", dpi=300)


if __name__ == "__main__":
    core_case_emission_detection_plot(metadata)
    

