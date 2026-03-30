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
U_density = .0191     # Density of uranium in kg/cm3, use this for both the core and shield

mass_core = 12.       # Mass of the core in kg
mass_shield = 4.     # Mass of the shield in kg



# ----------- Variables --------------
# All numbers are in the unit cm

space_thickness = 7. - 1.23
reflector_thickness = 0.5
HE_thickness = 6.
radiationCase_thickness = 0.5
casing_thickness = 0.7
# ----------- Variables --------------


geometry_variables = dict()



# ------------ Fissile material in the core ------------
# This is dependent on the mass of the fissile material 
r_core_inner = space_thickness
volume_core = mass_core / U_density     
r_core_outer = (3/(4*math.pi) * volume_core + r_core_inner**3)**(1/3) # Use the volume of the fissile material to calculate the outer radius
geometry_variables["Core"] = {"inner": float(r_core_inner), "outer" : float(r_core_outer)}


# ---------------- Reflector --------------------------
r_reflector_inner = r_core_outer
r_reflector_outer = r_reflector_inner + reflector_thickness
geometry_variables["Reflector"] = {"inner": r_reflector_inner, "outer" : r_reflector_outer}


# ------------- High Explosive ------------------------ 
r_HE_inner = r_reflector_outer
r_HE_outer = r_HE_inner + HE_thickness
geometry_variables["HE"] = {"inner": r_HE_inner, "outer" : r_HE_outer}


# -------------- Radiation Case ----------------------
r_radiationCase_inner = r_HE_outer
r_radiationCase_outer = r_radiationCase_inner + radiationCase_thickness
geometry_variables["RadiationCase"] = {"inner": r_radiationCase_inner, "outer" : r_radiationCase_outer}


# ----------------- Casing ---------------------------
r_casing_inner = r_radiationCase_outer
r_casing_outer = r_casing_inner + casing_thickness
geometry_variables["Casing"] = {"inner": r_casing_inner, "outer" : r_casing_outer}


# ------------- Load into json file ------------------
with open("geometry_variables.json", "w") as f:
    json.dump(geometry_variables, f, indent=4)



'''
Calculate the activity and relative abundance from the core and the shield independently

'''

# Set a specific start
core = rd.Inventory({"U-235" : 0.9 * mass_core, "U-238": 0.1 * mass_core}, 'kg')                # Weapons grade Uranium
radiationCase = rd.Inventory({"U-235" : 0.007 * mass_shield, "U-238" : 0.993 * mass_shield}, 'kg')     # Natural Uranium


# Calculate ingrowth after a certaion time
years = 2000.0
core_ingrowth = core.decay(years, 'y')
radiationCase_ingrowth = radiationCase.decay(years, 'y')


# Store the activities in a json file
core_activities = dict()
radiationCase_activities = dict()

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



# Calculate radiation case activites
for nuclide in radiationCase_ingrowth.nuclides:
    nuclideName = str(nuclide)
    radiationCase_activities[nuclideName] = float(radiationCase_ingrowth.activities('Bq')[nuclideName])

with open("radiationCase_activities.json", "w") as f:
    json.dump(radiationCase_activities, f, indent=4)



