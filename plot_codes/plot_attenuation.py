import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
import json
import numpy as np


with open("../run/data/temp/core_185/metadata_ca1f0809-bb67-47d1-a632-8e7550fcaede.json", "r") as f:
    metadata_185 = json.load(f)

with open("../run/data/temp/core_1001/metadata_ca1f0809-bb67-47d1-a632-8e7550fcaede.json", "r") as f:
    metadata_1001 = json.load(f)


def plot_attenaution(metadata_185, metadata_1001):
    emission = [metadata_185["core_activity_185.7keV"], metadata_1001["core_activity_1001.0keV"]]
    detected_core = [metadata_185["detectedCore_core_emission_185.7keV"], metadata_1001["detectedCore_core_emission_1001.0keV"]]
    detected_reflector = [metadata_185["detectedReflector_core_emission_185.7keV"], metadata_1001["detectedReflector_core_emission_1001.0keV"]]
    detected_HE = [metadata_185["detectedHE_core_emission_185.7keV"], metadata_1001["detectedHE_core_emission_1001.0keV"]]
    detected_radiationCase = [metadata_185["detectedRadCase_core_emission_185.7keV"], metadata_1001["detectedRadCase_core_emission_1001.0keV"]]
    detected = [metadata_185["detected_core_emission_185.7keV"], metadata_1001["detected_core_emission_1001.0keV"]]


    plt.figure(figsize=(10, 5))
    ax = plt.gca()
    plt.title("Attenuation in the different layers")


    plt.scatter(emission[0], emission[1], marker='x', label="Emission", color="black")
    plt.scatter(detected_core[0], detected_core[1], marker='x', label="After core", color="darkred")
    plt.scatter(detected_reflector[0], detected_reflector[1], marker='x', label="After reflector", color="firebrick")
    plt.scatter(detected_HE[0], detected_HE[1], marker='x', label="After HE", color="red")
    plt.scatter(detected_radiationCase[0], detected_radiationCase[1], marker='x', label="After radiaiton case", color="orangered")
    plt.scatter(detected[0], detected[1], marker='x', label="After casing", color="orange")

    plt.annotate("Emission", emission, xytext=(-25, -14), textcoords="offset points")
    plt.annotate("After core", detected_core, xytext=(5, -4), textcoords="offset points")
    plt.annotate("After reflector", detected_reflector, xytext=(5, -10), textcoords="offset points")
    plt.annotate("After HE", detected_HE, xytext=(5, -4), textcoords="offset points")
    plt.annotate("After radiaiton case", detected_radiationCase, xytext=(5, -4), textcoords="offset points")
    plt.annotate("After casing", detected, xytext=(5, -10), textcoords="offset points")


    plt.legend()


    plt.xlabel("185.7 keV Photon Intensity ($s^{-1}$)")
    plt.ylabel("1001 keV Photon Intensity ($s^{-1}$)")
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.savefig(f"Attenuation.png", dpi=300)


if __name__ == "__main__":
    plot_attenaution(metadata_185, metadata_1001)
    

