import total_activity
import decay_products
import json
import math
import ROOT as root
import subprocess
import uuid
import os
import random

def main():
    # Initialize the dict where data is stored
    # The key is the size of the core, the size of the radiation case and where the emission was from
    # For example: "core_emission_core_1.23_radCase_0.2" : 1000, "background_emission_core_1.23_radCase_0.2" : 500
    
    core_activity_185, core_y_185 = simulate(5, 0, 1, 0.9, 0.01, True, 185.7)
    


def simulate(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, core_emission, photon_energy):
    # Input: thickness of layers in cm, enrichment of the form 0.95, 0.002 etc. photon energy is either 185.7 or 1001.0
    # Output: The amount of 185.7 keV photons or 1001.0 keV photons detected outside the warhead.

    # Determine the geometry of the system
    decay_products.main(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, core_emission, photon_energy)

    # Find the activity of the photon that we want to simulate
    if core_emission:
        photon_activity = total_activity.get_core_activities(photon_energy)
    else:
        photon_activity = total_activity.get_bg_activities(photon_energy)
    print(f"Photon activity: {photon_activity} s^-1")

    # Simulate 10^6 photons. Then scale w.r.t. activity to get the number of photons emitted in 1 second, which is the photon intensity.
    subprocess.run(["./sim", "run_minimal.mac"])

    f = root.TFile("data/output0.root")
    h = f.Get("Casing")
    if photon_energy == 185.7:
        x = 0.1857  # Convert keV to MeV
    elif photon_energy == 1001.0:
        x = 1.00103

    bin_number = h.FindBin(x)
    y = h.GetBinContent(bin_number) * photon_activity / 10**6 

    print(f"Photon energy: {photon_energy} keV")
    print("Bin Number:", bin_number)
    print("Intensity:", y)

    return photon_activity, y
    

if __name__ == "__main__":
    main()