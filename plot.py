import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import json
import numpy as np

with open("run/data/metadata.json", "r") as f:
    metadata = json.load(f)

def core_noCore_plot(metadata):
    photon_intensity_fake_185 = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_fake_1001 = [] # Array consists of values of the form detected_background_emission_1001keV
    photon_intensity_real_185 = []  # Array consists of values of the form detected_total_emission_185.7keV
    photon_intensity_real_1001 = []  # Array consists of values of the form detected_total_emission_1001.0keV
    ignore = [] # Array consists of boolean values, where True means that the corresponding point should be plotted with alpha=1.0 and False means that the corresponding point should be plotted with alpha=0.1

    for geometry in metadata.values():
        if geometry["radiationCase_thickness"] < 1.9:
            ignore.append(False)
        else:
            ignore.append(False)
        photon_intensity_fake_185.append(geometry["detected_background_emission_185.7keV"])
        photon_intensity_fake_1001.append(geometry["detected_background_emission_1001.0keV"])
        photon_intensity_real_185.append(geometry["detected_total_emission_185.7keV"])
        photon_intensity_real_1001.append(geometry["detected_total_emission_1001.0keV"])


    # Create alpha array: False → 1.0, True → 0.1
    alpha_values = np.where(ignore, 0.1, 1.0)

    plt.figure(figsize=(10, 5))
    plt.title("Detected emission from a warhead with the core removed and a warhead with the core")

    plt.scatter(photon_intensity_real_185, photon_intensity_real_1001, marker='o', color="orange", alpha=alpha_values)
    plt.scatter(photon_intensity_fake_185, photon_intensity_fake_1001, marker='+', color="blue", alpha=alpha_values)

    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', color='blue', label='Detected emission from a warhead with the core removed',
            linestyle='None', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='o', color='w', label='Detected emission from a warhead',
            markerfacecolor='orange', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Gamma Intensity (s^-1)")
    plt.ylabel("1001 keV Gamma Intensity (s^-1)")

    plt.savefig("core_vs_noCore.png", dpi=300)


def core_case_plot(metadata):
    photon_intensity_case_185 = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_case_1001 = [] # Array consists of values of the form detected_background_emission_1001keV
    photon_intensity_core_185 = []  # Array consists of values of the form detected_core_emission_185.7keV
    photon_intensity_core_1001 = []  # Array consists of values of the form detected_core_emission_1001.0keV
    Z = [] # Array consists of boolean values, where True means that the corresponding point should be plotted with alpha=1.0 and False means that the corresponding point should be plotted with alpha=0.1
    ignore = [] # Array consists of boolean values, where True means that the corresponding point should be plotted with alpha=1.0 and False means that the corresponding point should be plotted with alpha=0.1
    Z_value = "radiationCase_thickness"
    radiationCase_enrichments = []
    core_enrichments = []
    radiationCase_masses = []
    space_thicknesses = []
    gap_thicknesses = []
    for geometry in metadata.values():
        ignore.append(False)
        Z.append(geometry[Z_value])
        radiationCase_enrichments.append(geometry["radiationCase_enrichment"])
        core_enrichments.append(geometry["core_enrichment"])
        radiationCase_masses.append(geometry["radiationCase_mass"])
        space_thicknesses.append(geometry["space_thickness"])
        gap_thicknesses.append(geometry["gap_thickness"])
        photon_intensity_case_185.append(geometry["detected_background_emission_185.7keV"])
        photon_intensity_case_1001.append(geometry["detected_background_emission_1001.0keV"])
        photon_intensity_core_185.append(geometry["detected_core_emission_185.7keV"])
        photon_intensity_core_1001.append(geometry["detected_core_emission_1001.0keV"])


    # Create alpha array: False → 1.0, True → 0.1
    alpha_values = np.where(ignore, 0.1, 1.0)

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Intensity of 185.7 keV and 1001 keV Gammas from the core and the case")
    
    plt.scatter(photon_intensity_case_185, photon_intensity_case_1001, marker='+', label="Detected emission from the case", color="blue", alpha=alpha_values)
    plt.scatter(photon_intensity_core_185, photon_intensity_core_1001, marker='x', label="Detected emission from the core", color="orange", alpha=alpha_values)

    # Add colorbar to show mapping
    #plt.colorbar(sc, label=Z_value)

    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', color='blue', label='Detected emission from the case',
            linestyle='None', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', color='orange', label='Detected emission from the core',
            linestyle='None', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Gamma Intensity (s^-1)")
    plt.ylabel("1001 keV Gamma Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"core_vs_case.png", dpi=300)
    
    # ------ Use Thickness of the case as a colorbar ------

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Detected emission from the core and the case with case thickness as a colorbar")

    plt.scatter(photon_intensity_case_185, photon_intensity_case_1001, marker='+', label="Detected emission from the case", c=Z, alpha=alpha_values)
    sc = plt.scatter(photon_intensity_core_185, photon_intensity_core_1001, marker='x', label="Detected emission from the core", c=Z, alpha=alpha_values)

    # Add colorbar to show mapping
    plt.colorbar(sc, label="Radiation Case Thickness (cm)")

    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Detected emission from the case',
            color='black', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Detected emission from the core',
            color='black', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Gamma Intensity (s^-1)")
    plt.ylabel("1001 keV Gamma Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"core_vs_case_with_case_thickness.png", dpi=300)

    # ------ Use Case mass of the case as a colorbar ------

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Detected emission from the core and the case with case mass as a colorbar")

    plt.scatter(photon_intensity_case_185, photon_intensity_case_1001, marker='+', label="Detected emission from the case", c=radiationCase_masses, alpha=alpha_values)
    sc = plt.scatter(photon_intensity_core_185, photon_intensity_core_1001, marker='x', label="Detected emission from the core", c=radiationCase_masses, alpha=alpha_values)

    # Add colorbar to show mapping
    plt.colorbar(sc, label="Radiation Case Mass (kg)")

    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Detected emission from the case',
            color='black', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Detected emission from the core',
            color='black', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Gamma Intensity (s^-1)")
    plt.ylabel("1001 keV Gamma Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"core_vs_case_with_case_mass.png", dpi=300)

    # ------ Use Size of the center space as a colorbar ------

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Detected emission from the core and the case with space radius as a colorbar")

    plt.scatter(photon_intensity_case_185, photon_intensity_case_1001, marker='+', label="Detected emission from the case", c=space_thicknesses, alpha=alpha_values)
    sc = plt.scatter(photon_intensity_core_185, photon_intensity_core_1001, marker='x', label="Detected emission from the core", c=space_thicknesses, alpha=alpha_values)

    # Add colorbar to show mapping
    plt.colorbar(sc, label="Space radius (cm)")

    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Detected emission from the case',
            color='black', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Detected emission from the core',
            color='black', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Gamma Intensity (s^-1)")
    plt.ylabel("1001 keV Gamma Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"core_vs_case_with_space_radius.png", dpi=300)

    # ------ Use Enrichment of the case and the core as a colorbar ------

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Detected emission from the core and the case with enrichments as colorbars")

    sc_case = plt.scatter(
        photon_intensity_case_185, 
        photon_intensity_case_1001, 
        marker='+', 
        label="Detected emission from the case", 
        c=radiationCase_enrichments, 
        cmap="viridis",
        alpha=alpha_values)
    sc_core = plt.scatter(
        photon_intensity_core_185, 
        photon_intensity_core_1001, 
        marker='x', 
        label="Detected emission from the core", 
        c=core_enrichments, 
        cmap="plasma",
        alpha=alpha_values)

    # Add colorbar to show mapping
    plt.colorbar(sc_core, label="Core Enrichment", location="left")
    plt.colorbar(sc_case, label="Case Enrichment", location="right")

    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Detected emission from the case',
            color='black', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Detected emission from the core',
            color='black', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Gamma Intensity (s^-1)")
    plt.ylabel("1001 keV Gamma Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"core_vs_case_with_enrichments.png", dpi=300)

    # ------ Use Enrichment of the case and the core as a colorbar ------

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Detected emission from the core and the case with gap thickness as colorbars")

    plt.scatter(photon_intensity_case_185, photon_intensity_case_1001, marker='+', label="Detected emission from the case", c=gap_thicknesses, alpha=alpha_values)
    sc = plt.scatter(photon_intensity_core_185, photon_intensity_core_1001, marker='x', label="Detected emission from the core", c=gap_thicknesses, alpha=alpha_values)

    # Add colorbar to show mapping
    plt.colorbar(sc, label="Gap thickness (cm)")

    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Detected emission from the case',
            color='black', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Detected emission from the core',
            color='black', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Gamma Intensity (s^-1)")
    plt.ylabel("1001 keV Gamma Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"core_vs_case_with_gapThickness.png", dpi=300)

def core_case_emission_detection_plot(metadata):
    photon_intensity_core_185_emittied = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_core_185_detected = [] # Array consists of values of the form detected_background_emission_1001keV
    photon_intensity_core_1001_emittied = []  # Array consists of values of the form detected_core_emission_185.7keV
    photon_intensity_core_1001_detected = []  # Array consists of values of the form detected_core_emission_1001.0keV
    photon_intensity_case_185_emittied = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_case_185_detected = [] # Array consists of values of the form detected_background_emission_1001keV
    photon_intensity_case_1001_emittied = []  # Array consists of values of the form detected_core_emission_185.7keV
    photon_intensity_case_1001_detected = []  # Array consists of values of the form detected_core_emission_1001.0keV
    for geometry in metadata.values():
        photon_intensity_core_185_emittied.append(geometry["core_activity_185.7keV"])
        photon_intensity_core_185_detected.append(geometry["detected_core_emission_185.7keV"])
        photon_intensity_core_1001_emittied.append(geometry["core_activity_1001.0keV"])
        photon_intensity_core_1001_detected.append(geometry["detected_core_emission_1001.0keV"])
        photon_intensity_case_185_emittied.append(geometry["background_activity_185.7keV"])
        photon_intensity_case_185_detected.append(geometry["detected_background_emission_185.7keV"])
        photon_intensity_case_1001_emittied.append(geometry["background_activity_1001.0keV"])
        photon_intensity_case_1001_detected.append(geometry["detected_background_emission_1001.0keV"])


    # Create alpha array: True → 1.0, False → 0.1

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Emmitted and detected photons from the case and the core")

    

    plt.scatter(photon_intensity_core_185_emittied, photon_intensity_core_1001_emittied, marker='x', label="Emission from the core", color="black")
    plt.scatter(photon_intensity_case_185_emittied, photon_intensity_case_1001_emittied, marker='+', label="Emission from the case", color="black")
    plt.scatter(photon_intensity_core_185_detected, photon_intensity_core_1001_detected, marker='x', label="Detection from the core", color="orange")
    plt.scatter(photon_intensity_case_185_detected, photon_intensity_case_1001_detected, marker='+', label="Detection from the case", color="blue")


    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Detected emission from the case',
            color='blue', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Detected emission from the core',
            color='orange', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='+', linestyle='None', label='Emission from the case',
            color='black', markersize=8, alpha=1.0),
        Line2D([0], [0], marker='x', linestyle='None', label='Emission from the core',
            color='black', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Photon Intensity (s^-1)")
    plt.ylabel("1001.0 keV Photon Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"emission_and_detection.png", dpi=300)

# ----------------------------------------------------------------------------------------------

    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Emmitted and detected photons from the case and the core")

    alpha_value = 1
    
    plt.scatter(photon_intensity_core_185_emittied, photon_intensity_core_1001_emittied, marker='x', label="Emission from the core", color="black", alpha=alpha_value)
    plt.scatter(photon_intensity_case_185_emittied, photon_intensity_case_1001_emittied, marker='+', label="Emission from the case", color="black", alpha=alpha_value)
    plt.scatter(photon_intensity_core_185_detected, photon_intensity_core_1001_detected, marker='x', label="Detection from the core", color="orange", alpha=alpha_value)
    plt.scatter(photon_intensity_case_185_detected, photon_intensity_case_1001_detected, marker='+', label="Detection from the case", color="blue", alpha=alpha_value)
    
    with open("run/data/metadata_nothickness.json", "r") as f:
        metadata_nothickness = json.load(f)
    
    detected_core_emission_185_nocase = [] # Array consists of values of the form detected_core_emission_185.7keV for geometries with no case
    detected_core_emission_1001_nocase = [] # Array consists of values of the form detected_core_emission_1001.0keV for geometries with no case
    for key, this_metadata in metadata_nothickness.items():
        detected_core_emission_185_nocase.append(this_metadata["detected_core_emission_185.7keV"])
        detected_core_emission_1001_nocase.append(this_metadata["detected_core_emission_1001.0keV"])
    
    plt.scatter(detected_core_emission_185_nocase, detected_core_emission_1001_nocase, marker='x', label="Detection from the core with no case", color="red", alpha=1.0)


    # Create custom legend handles (force alpha=1)
    legend_elements = [
        Line2D([0], [0], marker='+', linestyle='None', label='Detected emission from the case',
            color='blue', markersize=8, alpha=alpha_value),
        Line2D([0], [0], marker='x', linestyle='None', label='Detected emission from the core',
            color='orange', markersize=8, alpha=alpha_value),
        Line2D([0], [0], marker='+', linestyle='None', label='Emission from the case',
            color='black', markersize=8, alpha=alpha_value),
        Line2D([0], [0], marker='x', linestyle='None', label='Emission from the core',
            color='black', markersize=8, alpha=alpha_value),
        Line2D([0], [0], marker='x', linestyle='None', label='Detection from the core with no case',
            color='red', markersize=8, alpha=1.0)
    ]

    plt.legend(handles=legend_elements)


    plt.xlabel("185.7 keV Photon Intensity (s^-1)")
    plt.ylabel("1001.0 keV Photon Intensity (s^-1)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"emission_and_detection_with_reference.png", dpi=300)


if __name__ == "__main__":
    core_noCore_plot(metadata)
    core_case_plot(metadata)
    core_case_emission_detection_plot(metadata)
    

