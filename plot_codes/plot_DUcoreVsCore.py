import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import json
import numpy as np


with open("../run/data/metadata_DUcore.json", "r") as f:
    metadata = json.load(f)


def core_case_emission_detection_plot(metadata):
    photon_intensity_core_185 = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_core_1001 = []  # Array consists of values of the form detected_core_emission_185.7keV
    photon_intensity_DUcore_185 = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_DUcore_1001 = []  # Array consists of values of the form detected_core_emission_185.7keV
    for geometry in metadata.values():
        photon_intensity_core_185.append(geometry["detected_core_emission_185.7keV"])
        photon_intensity_core_1001.append(geometry["detected_core_emission_1001.0keV"])
        photon_intensity_DUcore_185.append(geometry["detected_DUcore_emission_185.7keV"])
        photon_intensity_DUcore_1001.append(geometry["detected_DUcore_emission_1001.0keV"])
    photon_intensity_core_185 = np.array(photon_intensity_core_185)
    photon_intensity_core_1001 = np.array(photon_intensity_core_1001)
    photon_intensity_DUcore_185 = np.array(photon_intensity_DUcore_185)
    photon_intensity_DUcore_1001 = np.array(photon_intensity_DUcore_1001)
    

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Detected 185.7 keV photons from a HEU core and a DU core")

    bins_core = np.logspace(np.log10(photon_intensity_core_185.min()), np.log10(photon_intensity_core_185.max()), 50)
    plt.hist(photon_intensity_core_185, 
             bins=bins_core, 
             alpha=0.5,
             edgecolor='black',
             linewidth=0.8,
             histtype='stepfilled',
             label='HEU Core',
             color='orange')
    bins_case = np.logspace(np.log10(photon_intensity_DUcore_185.min()), np.log10(photon_intensity_DUcore_185.max()), 50)
    plt.hist(photon_intensity_DUcore_185, 
             edgecolor='black',
             linewidth=0.8,
             alpha=0.5,
             bins=bins_case, 
             histtype='stepfilled',
             label='DU Core',
             color='blue')

    plt.legend()

    plt.xlabel("185.7 keV Photon Intensity ($s^{-1}$)")
    plt.ylabel("Count")
    ax.set_xscale('log')

    plt.savefig(f"coreVsDucore_185_hist.png", dpi=300)


    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Detected 1001 keV photons from a HEU core and a DU core")

    bins_core = np.logspace(np.log10(photon_intensity_core_1001.min()), np.log10(photon_intensity_core_1001.max()), 50)
    plt.hist(photon_intensity_core_1001, 
             bins=bins_core, 
             alpha=0.5,
             edgecolor='black',
             linewidth=0.8,
             histtype='stepfilled',
             label='HEU Core',
             color='orange')
    bins_case = np.logspace(np.log10(photon_intensity_DUcore_1001.min()), np.log10(photon_intensity_DUcore_1001.max()), 50)
    plt.hist(photon_intensity_DUcore_1001, 
             edgecolor='black',
             linewidth=0.8,
             alpha=0.5,
             bins=bins_case, 
             histtype='stepfilled',
             label='DU Core',
             color='blue')

    plt.legend()

    plt.xlabel("1001 keV Photon Intensity ($s^{-1}$)")
    plt.ylabel("Count")
    ax.set_xscale('log')

    plt.savefig(f"coreVsDucore_1001_hist.png", dpi=300)


if __name__ == "__main__":
    core_case_emission_detection_plot(metadata)
    

