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
    i = 0
    if os.path.exists("data/metadata.json"):
        with open("data/metadata.json", "r") as f:
            metadata = json.load(f)
    else:
        metadata = dict()
    with open("data/metadata_DUcore.json", "r") as f:
        metadata_DUcore = json.load(f)
    
    # Use all simulations already run, simulate when the core is of the same enrichment as the case. 
    for key, item in metadata.items():
        if os.path.exists(f"data/temp/metadata_{key}.json"): continue
        space_thickness = item["space_thickness"]
        gap_thickness = item["gap_thickness"]
        radiationCase_thickness = item["radiationCase_thickness"]
        core_enrichment = item["radiationCase_enrichment"]
        radiationCase_enrichment = 0.
        # Simulation 1
        DUcore_activity_185, detected_DUcore_emission_185, detectedRadCase_DUcore_emission_185, detectedHE_DUcore_emission_185, detectedReflector_DUcore_emission_185, detectedCore_DUcore_emission_185 = simulate(
            space_thickness,
            gap_thickness,
            radiationCase_thickness,
            core_enrichment,
            radiationCase_enrichment,
            core_emission = True,
            photon_energy = 185.7)
        item["DUcore_activity_185.7keV"] = DUcore_activity_185
        item["detected_DUcore_emission_185.7keV"] = detected_DUcore_emission_185
        item["detectedRadCase_DUcore_emission_185.7keV"] = detectedRadCase_DUcore_emission_185
        item["detectedHE_DUcore_emission_185.7keV"] = detectedHE_DUcore_emission_185
        item["detectedReflector_DUcore_emission_185.7keV"] = detectedReflector_DUcore_emission_185
        item["detectedCore_DUcore_emission_185.7keV"] = detectedCore_DUcore_emission_185        
        
        with open(f"data/temp/DUcore_185/metadata_{key}.json", "w") as f:
            json.dump(item, f, indent=4)
        i+=1
        if i > 0: break


def simulate(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, core_emission, photon_energy):
    # Input: thickness of layers in cm, enrichment of the form 0.95, 0.002 etc. photon energy is either 185.7 or 1001.0
    # Output: The amount of 185.7 keV photons or 1001.0 keV photons detected outside the warhead.

    # Determine the geometry of the system, as well as the emission intesity
    decay_products.main(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, core_emission, photon_energy)

    # Find the activity of the photon that we want to simulate
    if core_emission:
        photon_activity = total_activity.get_core_activities(photon_energy)
    else:
        photon_activity = total_activity.get_bg_activities(photon_energy)
    print(f"Photon activity: {photon_activity} s^-1")

    # Simulate 10^6 photons. Then scale w.r.t. activity to get the number of photons emitted in 1 second, which is the photon intensity.
    subprocess.run(["./sim", "run.mac"])

    f = root.TFile("data/output0.root")
    if photon_energy == 185.7:
        x = 0.1857  # Convert keV to MeV
    elif photon_energy == 1001.0:
        x = 1.00103
    bin_number = f.Get("Casing").FindBin(x)

    Casing = f.Get("Casing").GetBinContent(bin_number) * photon_activity / 10**6 
    RadiationCase = f.Get("RadiationCase").GetBinContent(bin_number) * photon_activity / 10**6 
    HE = f.Get("HE").GetBinContent(bin_number) * photon_activity / 10**6 
    Reflector = f.Get("Reflector").GetBinContent(bin_number) * photon_activity / 10**6 
    Core = f.Get("Core").GetBinContent(bin_number) * photon_activity / 10**6 

    print(f"Photon energy: {photon_energy} keV")
    print("Bin Number:", bin_number)
    print("Intensity:", Casing)

    return photon_activity, Casing, RadiationCase, HE, Reflector, Core
    

if __name__ == "__main__":
    main()