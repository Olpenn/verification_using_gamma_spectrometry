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
    if os.path.exists("data/metadata.json"):
        with open("data/metadata.json", "r") as f:
            metadata = json.load(f)
    else:
        metadata = dict()
    
    for i in range(1):
        # Create the parameters:
        space_thickness = random.uniform(5, 7)
        gap_thickness = random.uniform(0, 5)
        radiationCase_thickness = random.uniform(0.2, 2)
        core_enrichment = random.uniform(0.9, 1.0)
        radiationCase_enrichment = random.uniform(0.0015, 0.0072)

        core_thickness = ((3/(4*math.pi)) * 12/0.0191 + (space_thickness**3) )**(1/3)

        # Store the parameters in this metadata
        this_metadata = {
            "space_thickness": space_thickness,
            "core_thickness": core_thickness,
            "reflector_thickness": 1,
            "HE_thickness": 10,
            "gap_thickness": gap_thickness,
            "radiationCase_thickness": radiationCase_thickness,
            "core_enrichment": core_enrichment,
            "radiationCase_enrichment": radiationCase_enrichment,
            "core_mass": 12,
            "radiationCase_mass": round((4/3)*math.pi*(((core_thickness + 1 + 10 + gap_thickness + radiationCase_thickness)**3) - ((core_thickness + 1 + 10 + gap_thickness)**3)) * 0.0191, 2)
        }

        # Simulate the system with the given configuration
        core_activity_185, core_y_185 = simulate(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, True, 185.7)
        bg_activity_185, bg_y_185 = simulate(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, False, 185.7)
        
        this_metadata["core_activity_185.7keV"] = core_activity_185
        this_metadata["detected_core_emission_185.7keV"] = core_y_185
        this_metadata["background_activity_185.7keV"] = bg_activity_185
        this_metadata["detected_background_emission_185.7keV"] = bg_y_185
        this_metadata["detected_total_emission_185.7keV"] = bg_y_185 + core_y_185

        # Simulate the system with the given configuration
        core_activity_1001, core_y_1001 = simulate(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, True, 1001.0)
        bg_activity_1001, bg_y_1001 = simulate(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, False, 1001.0)

        this_metadata["core_activity_1001.0keV"] = core_activity_1001
        this_metadata["detected_core_emission_1001.0keV"] = core_y_1001
        this_metadata["background_activity_1001.0keV"] = bg_activity_1001
        this_metadata["detected_background_emission_1001.0keV"] = bg_y_1001
        this_metadata["detected_total_emission_1001.0keV"] = bg_y_1001 + core_y_1001

        metadata[str(uuid.uuid4())] = this_metadata

    with open("data/metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)


def simulate(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, core_emission, photon_energy):
    # Input: thickness of layers in cm, enrichment of the form 0.95, 0.002 etc. photon energy is either 185.7 or 1001.0
    # Output: The amount of 185.7 keV photons or 1001.0 keV photons detected outside the warhead.

    # Determine the geometry of the system
    decay_products.main(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, core_emission, photon_energy)

    # Find the activity of the photon that we want to simulate
    if core_emission:
        photon_activity = round(total_activity.get_core_activities(photon_energy))
    else:
        photon_activity = round(total_activity.get_bg_activities(photon_energy))
    print(f"Photon activity: {photon_activity} s^-1")

    # Simulate 10^5 photons. Then scale w.r.t. activity to get the number of photons emitted in 1 second, which is the photon intensity.
    subprocess.run(["./sim", "run.mac"])

    f = root.TFile("data/output0.root")
    h = f.Get("Casing")
    if photon_energy == 185.7:
        x = 0.1857  # Convert keV to MeV
    elif photon_energy == 1001.0:
        x = 1.00103

    bin_number = h.FindBin(x)
    y = h.GetBinContent(bin_number) * photon_activity / 10**5

    print(f"Photon energy: {photon_energy} keV")
    print("Bin Number:", bin_number)
    print("Intensity:", y)

    return photon_activity, y
    

if __name__ == "__main__":
    main()