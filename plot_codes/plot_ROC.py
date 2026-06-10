import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
from sklearn.metrics import roc_curve, auc
import json
import numpy as np


with open("../run/data/metadata.json", "r") as f:
    metadata = json.load(f)


def plot_ROC(metadata):
    photon_intensity_core_185_detected = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_core_1001_detected = []  # Array consists of values of the form detected_core_emission_185.7keV
    photon_intensity_case_185_detected = [] # Array consists of values of the form detected_background_emission_185.7keV
    photon_intensity_case_1001_detected = []  # Array consists of values of the form detected_core_emission_185.7keV
    for geometry in metadata.values():
        photon_intensity_core_185_detected.append(geometry["detected_core_emission_185.7keV"])
        photon_intensity_core_1001_detected.append(geometry["detected_core_emission_1001.0keV"])
        photon_intensity_case_185_detected.append(geometry["detected_background_emission_185.7keV"])
        photon_intensity_case_1001_detected.append(geometry["detected_background_emission_1001.0keV"])
    photon_intensity_core_185_detected = np.array(photon_intensity_core_185_detected)
    photon_intensity_core_1001_detected = np.array(photon_intensity_core_1001_detected)
    photon_intensity_case_185_detected = np.array(photon_intensity_case_185_detected)
    photon_intensity_case_1001_detected = np.array(photon_intensity_case_1001_detected)

    # Define the true and false data points for the ROC curve
    hoax_185 = photon_intensity_case_185_detected
    real_185 = photon_intensity_case_185_detected + photon_intensity_core_185_detected
    hoax_1001 = photon_intensity_case_1001_detected
    real_1001 = photon_intensity_case_1001_detected + photon_intensity_core_1001_detected
    hoax_1001_185 = hoax_185 / hoax_1001
    real_1001_185 = real_185 / real_1001

    # Use ROC for 185
    y_scores_185 = np.concatenate([hoax_185, real_185])
    y_true_185 = np.concatenate([np.zeros(len(hoax_185)), np.ones(len(real_185))])

    # Compute ROC
    fpr_185, tpr_185, thresholds_185 = roc_curve(y_true_185, y_scores_185)

    # Area under curve
    roc_auc_185 = auc(fpr_185, tpr_185)


    # Use ROC for 1001
    y_scores_1001 = np.concatenate([hoax_1001, real_1001])
    y_true_1001 = np.concatenate([np.zeros(len(hoax_1001)), np.ones(len(real_1001))])

    # Compute ROC
    fpr_1001, tpr_1001, thresholds_1001 = roc_curve(y_true_1001, y_scores_1001)

    # Area under curve
    roc_auc_1001 = auc(fpr_1001, tpr_1001)


    # Use ROC for 1001/185
    y_scores_1001_185 = np.concatenate([hoax_1001_185, real_1001_185])
    y_true_1001_185 = np.concatenate([np.zeros(len(hoax_1001_185)), np.ones(len(real_1001_185))])

    # Compute ROC
    fpr_1001_185, tpr_1001_185, thresholds_1001_185 = roc_curve(y_true_1001_185, y_scores_1001_185)

    # Area under curve
    roc_auc_1001_185 = auc(fpr_1001_185, tpr_1001_185)



    # Plot
    plt.figure(figsize=(6,6))

    plt.plot(fpr_185, tpr_185, label=rf"185 keV: $\mathbf{{AUC = {roc_auc_185:.3f}}}$")
    plt.plot(fpr_1001, tpr_1001, label=rf"1001 keV: $\mathbf{{AUC = {roc_auc_1001:.3f}}}$")
    plt.plot(fpr_1001_185, tpr_1001_185, label=rf"1001 keV / 185 keV: $\mathbf{{AUC = {roc_auc_1001_185:.3f}}}$")
    plt.plot([0,1], [0,1], '--', color='gray')

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve for classification of HEU core vs no core")
    plt.legend()

    plt.savefig("ROC_185.png", dpi=300)


if __name__ == "__main__":
    plot_ROC(metadata)
    

