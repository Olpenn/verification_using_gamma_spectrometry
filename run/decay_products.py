import radioactivedecay as rd
import json
import math
import random

'''
This program is responsible to calculate the variables that the geometry is built upon. 
Note that the mass of the core and shield directly determines the volume and hence determines the thickness of that layer.

The geometry looks like:
Empty space - Air
Core - HEU
Neutron Reflector - Be
HE - TNT
Radiation Case - DU
Casing - Al

'''

def main(space_thickness, gap_thickness, radiationCase_thickness, core_enrichment, radiationCase_enrichment, core_emission, photon_energy):
    # ----------- Variables --------------
    # All numbers are in the unit cm
    # The code is designed so that layers can take the following configuration, from the center to the outside:
    # 1. Air - Center of the sphere to the inner radius of the core
    # 2. Core - 12kg of HEU, the thickness is determined by the mass of the core
    # 3. Neutron Reflector - 1cm of Be
    # 4. High Explosive - 10cm of TNT
    # 5. Gap - an eventual gap between the HE and the radiation case.
    # 6. Radiation Case - Consists of Depleted Uranium, the concentration of U-235 is a variable, the thickness is a variable. 
    # 7. Casing - 0.5cm of Al
    #
    #
    # There are 5 parameters that can be varied:
    # 1. The size of the empty space in the centre. This parameter is set between 5cm and 7cm.
    # 2. The percentage of U-235 in the core. This parameter is set between 0.9 and 1.0, the rest is U-238 and a small amount of U-234.
    # 3. The size of the gap in between the HE and the radiation case. This parameter is set between 0cm and 5cm.
    # 4. The thickness of the radiation case. This paramter is set between 0.2cm and 2cm.
    # 5. The concentration of U-235 in the radiation case. This parameter is set between 0.15% and 0.72% (the rest is U-238).

    
    core_thickness = ((3/(4*math.pi)) * 12/0.0191 + (space_thickness**3) )**(1/3)     # Calculate the thickness of the core based on the mass of the fissile material, which is 12kg 
    reflector_thickness = 1.
    HE_thickness = 10.
    casing_thickness = 0.5
    # ----------- Variables --------------


    geometry_variables = dict()
    geometry_variables["core_emission"] = core_emission
    if photon_energy == 185.7:
        geometry_variables["photon_energy"] = 185.7
    elif photon_energy == 1001.0:
        geometry_variables["photon_energy"] = 1001.0
    else:
        raise ValueError("Photon energy must be either 185.7 or 1001.0 keV.")


    # ------------ Fissile material in the core ------------
    # This is dependent on the mass of the fissile material 
    if core_thickness:
        r_core_inner = space_thickness    
        r_core_outer = r_core_inner + core_thickness
        geometry_variables["Core"] = {"inner": r_core_inner, "outer" : r_core_outer}


    # ---------------- Reflector --------------------------
    if reflector_thickness:
        r_reflector_inner = r_core_outer
        r_reflector_outer = r_reflector_inner + reflector_thickness
        geometry_variables["Reflector"] = {"inner": r_reflector_inner, "outer" : r_reflector_outer}


    # ------------- High Explosive ------------------------ 
    if HE_thickness:
        r_HE_inner = r_reflector_outer
        r_HE_outer = r_HE_inner + HE_thickness
        geometry_variables["HE"] = {"inner": r_HE_inner, "outer" : r_HE_outer}


    # -------------- Radiation Case ----------------------
    if radiationCase_thickness:
        r_radiationCase_inner = r_HE_outer
        r_radiationCase_outer = r_radiationCase_inner + radiationCase_thickness
        geometry_variables["RadiationCase"] = {"inner": r_radiationCase_inner, "outer" : r_radiationCase_outer}


    # ----------------- Casing ---------------------------
    if casing_thickness: 
        r_casing_inner = r_radiationCase_outer
        r_casing_outer = r_casing_inner + casing_thickness
        geometry_variables["Casing"] = {"inner": r_casing_inner, "outer" : r_casing_outer}


    # ------------- Load into json file ------------------
    with open("data/geometry_variables.json", "w") as f:
        json.dump(geometry_variables, f, indent=4)



    '''
    Calculate the activity and relative abundance from the core and the shield independently

    '''

    mass_core = 12
    U_density = 0.0191

    if radiationCase_thickness:
        mass_radiationCase = 4/3 * math.pi * (r_radiationCase_outer**3 - r_radiationCase_inner**3) * U_density
        background = rd.Inventory({"U-238" : (1 - radiationCase_enrichment) * mass_radiationCase, "U-235" : radiationCase_enrichment * mass_radiationCase}, 'kg')     # Depleted Uranium


    # Set a specific start
    core = rd.Inventory({"U-235" : core_enrichment * mass_core, "U-238": (1 - core_enrichment) * mass_core}, 'kg') # HEU              # Weapons grade Uranium


    # Calculate ingrowth after a certaion time
    years = 20.0
    core_ingrowth = core.decay(years, 'y')
    background_ingrowth = background.decay(years, 'y')


    # Store the activities in a json file
    core_activities = dict()
    background_activities = dict()

    '''
    There are two possible sources where gamma rays can originate from, either the core with HEU
    or the radiation case consisting of depleted Uranium. These two have two different activities.

    For the material used when tracking abrobtion, use pure uranium, ignore this for this file

    '''
    # Calculate core activites
    for nuclide in core_ingrowth.nuclides:
        nuclideName = str(nuclide)
        core_activities[nuclideName] = float(core_ingrowth.activities('Bq')[nuclideName])

    with open("data/core_activities.json", "w") as f:
        json.dump(core_activities, f, indent=4)



    # Calculate background activites
    for nuclide in background_ingrowth.nuclides:
        nuclideName = str(nuclide)
        background_activities[nuclideName] = float(background_ingrowth.activities('Bq')[nuclideName])

    with open("data/background_activities.json", "w") as f:
        json.dump(background_activities, f, indent=4)


if __name__ == "__main__":
    main()