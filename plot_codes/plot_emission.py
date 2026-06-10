import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import json
import numpy as np


with open("../run/data/metadata.json", "r") as f:
    metadata = json.load(f)


def core_case_emission_detection_plot(metadata):
    photon_intensity_core_185_emittied = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_core_1001_emittied = []  # Array consists of values of the form detected_core_emission_185.7keV
    photon_intensity_case_185_emittied = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_case_1001_emittied = []  # Array consists of values of the form detected_core_emission_185.7keV
    for geometry in metadata.values():
        photon_intensity_core_185_emittied.append(geometry["core_activity_185.7keV"])
        photon_intensity_core_1001_emittied.append(geometry["core_activity_1001.0keV"])
        photon_intensity_case_185_emittied.append(geometry["background_activity_185.7keV"])
        photon_intensity_case_1001_emittied.append(geometry["background_activity_1001.0keV"])


    # Create alpha array: True → 1.0, False → 0.1

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Emitted photons from the case and the core")

    

    plt.scatter(photon_intensity_core_185_emittied, photon_intensity_core_1001_emittied, marker='x', label="Emission from the core", color="black")
    plt.scatter(photon_intensity_case_185_emittied, photon_intensity_case_1001_emittied, marker='+', label="Emission from the case", color="black")



    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Emission from the case',
            color='black', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Emission from the core',
            color='black', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Photon Intensity ($s^{-1}$)")
    plt.ylabel("1001 keV Photon Intensity ($s^{-1}$)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"emission.png", dpi=300)


if __name__ == "__main__":
    core_case_emission_detection_plot(metadata)
    

