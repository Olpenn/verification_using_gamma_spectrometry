import radioactivedecay as rd
import json
import math

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


# ----------- Variables --------------
# All numbers are in the unit cm
# The code is designed so that layers can take two different configurations:
# 1. Air - Core - Reflector - Tamper - HE -                  Casing
# 2. Air - Core - Reflector -          HE - Radiation Case - Casing
# The way to swich between these two configuration is to set either the Tamper thickness or the Radiation Case thickness to 0.

space_thickness = 7. - 1.23
core_thickness = 1.23
reflector_thickness = 1.
tamper_thickness = 0.
HE_thickness = 10.
radiationCase_thickness = 0.2
casing_thickness = 0.5
# ----------- Variables --------------


geometry_variables = dict()



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


# ---------------- Tamper --------------------------
if tamper_thickness:
    r_tamper_inner = r_reflector_outer
    r_tamper_outer = r_tamper_inner + tamper_thickness
    geometry_variables["Tamper"] = {"inner": r_tamper_inner, "outer" : r_tamper_outer}


# ------------- High Explosive ------------------------ 
if HE_thickness:
    if tamper_thickness:
        r_HE_inner = r_tamper_outer
    else:
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
    if radiationCase_thickness:
        r_casing_inner = r_radiationCase_outer
    else:
        r_casing_inner = r_HE_outer
    r_casing_outer = r_casing_inner + casing_thickness
    geometry_variables["Casing"] = {"inner": r_casing_inner, "outer" : r_casing_outer}


# ------------- Load into json file ------------------
with open("geometry_variables.json", "w") as f:
    json.dump(geometry_variables, f, indent=4)



'''
Calculate the activity and relative abundance from the core and the shield independently

'''

U_density = .0191     # Density of uranium in kg/cm3, use this for both the core and shield
mass_core = 4/3 * math.pi * (r_core_outer**3 - r_core_inner**3) * U_density

if tamper_thickness:
    mass_tamper = 4/3 * math.pi * (r_tamper_outer**3 - r_tamper_inner**3) * U_density
    background = rd.Inventory({"U-238" : mass_tamper}, 'kg')     # Depleted Uranium

elif radiationCase_thickness:
    mass_radiationCase = 4/3 * math.pi * (r_radiationCase_outer**3 - r_radiationCase_inner**3) * U_density
    background = rd.Inventory({"U-238" : 0.998 * mass_radiationCase, "U-235" : 0.002 * mass_radiationCase}, 'kg')     # Depleted Uranium


# Set a specific start
core = rd.Inventory({"U-235" : 0.935 * mass_core, "U-238": 0.055 * mass_core, "U-234": 0.01 * mass_core}, 'kg') # HEU              # Weapons grade Uranium


# Calculate ingrowth after a certaion time
years = 20.0
core_ingrowth = core.decay(years, 'y')
background_ingrowth = background.decay(years, 'y')


# Store the activities in a json file
core_activities = dict()
background_activities = dict()

'''
There are two possible sources where gamma rays can originate from, either the core with weapons grade Uranium
or the radiation case consisting of depleted Uranium. These two have two different activities.

For the material used when tracking abrobtion, use pure uranium, ignore this for this file

'''
# Calculate core activites
for nuclide in core_ingrowth.nuclides:
    nuclideName = str(nuclide)
    core_activities[nuclideName] = float(core_ingrowth.activities('Bq')[nuclideName])

with open("core_activities.json", "w") as f:
    json.dump(core_activities, f, indent=4)



# Calculate background activites
for nuclide in background_ingrowth.nuclides:
    nuclideName = str(nuclide)
    background_activities[nuclideName] = float(background_ingrowth.activities('Bq')[nuclideName])

with open("background_activities.json", "w") as f:
    json.dump(background_activities, f, indent=4)


