import radioactivedecay as rd
import json
import math

'''
This program is responsible to calculate the variables that the geometry is built upon. 
Note that the mass of the core and shield directly determines the volume and hence determines the thickness of that layer.

The geometry looks like:
Empty space - Air
Core - WgU
Neutron Reflector - Be
Tamper - Th
HE - TNT
Casing - Al
Shield - U
'''
U_density = .0191     # Density of uranium in kg/cm3, use this for both the core and shield

mass_core = 12.       # Mass of the core in kg
mass_shield = 4.     # Mass of the shield in kg



# ----------- variables --------------
# All numbers are in the unit cm

space_thickness = 7. - 1.23
reflector_thickness = 0.5
tamper_thickness = 3.
HE_thickness = 6.
casing_thickness = 0.7
# ----------- variables --------------

geometry_variables = dict()


r_space_inner = 0.
r_space_outer = r_space_inner + space_thickness
geometry_variables["Space"] = {"inner": float(r_space_inner), "outer" : float(r_space_outer)}

r_core_inner = r_space_outer
volume_core = mass_core / U_density     # Volume is mass / density

# 4/3 pi r_outer^3 - 4/3 pi r_inner^3 = volume_core
# r_outer = (3/(4pi) volume_core + r_inner^3)^(1/3)
r_core_outer = (3/(4*math.pi) * volume_core + r_core_inner**3)**(1/3)
geometry_variables["Core"] = {"inner": float(r_core_inner), "outer" : float(r_core_outer)}

r_reflector_inner = r_core_outer
r_reflector_outer = r_reflector_inner + reflector_thickness
geometry_variables["Reflector"] = {"inner": r_reflector_inner, "outer" : r_reflector_outer}

r_tamper_inner = r_reflector_outer
r_tamper_outer = r_tamper_inner + tamper_thickness
geometry_variables["Tamper"] = {"inner": r_tamper_inner, "outer" : r_tamper_outer}

r_HE_inner = r_tamper_outer
r_HE_outer = r_HE_inner + HE_thickness
geometry_variables["HE"] = {"inner": r_HE_inner, "outer" : r_HE_outer}

r_casing_inner = r_HE_outer
r_casing_outer = r_casing_inner + casing_thickness
geometry_variables["Casing"] = {"inner": r_casing_inner, "outer" : r_casing_outer}

r_shield_inner = r_casing_outer
volume_shield = mass_shield / U_density     # Volume is mass / density

# 4/3 pi r_outer^3 - 4/3 pi r_inner^3 = volume_shield
# r_outer = (3/(4pi) volume_shield + r_inner^3)^(1/3)
r_shield_outer = (3/(4*math.pi) * volume_shield + r_shield_inner**3)**(1/3)
geometry_variables["Shield"] = {"inner": r_shield_inner, "outer" : r_shield_outer}


with open("geometry_variables.json", "w") as f:
    json.dump(geometry_variables, f, indent=4)

'''
Calculate the activity and relative abundance from the core and the shield independently

'''


# Calculate ingrowth after time t
core = rd.Inventory({"U-235" : 0.9 * mass_core, "U-238": 0.1 * mass_core}, 'kg')                # Weapons grade Uranium
shield = rd.Inventory({"U-235" : 0.007 * mass_shield, "U-238" : 0.993 * mass_shield}, 'kg')     # Natural Uranium
years = 20.0

core_ingrowth = core.decay(years, 'y')
shield_ingrowth = shield.decay(years, 'y')


# Store the activities in a json file
core_activities = dict()
core_abundances_relative = dict()
shield_activities = dict()
shield_abundances_relative = dict()

'''
There are two possible sources where gamma rays can originate from, either the core with weapons grade Uranium
or the shield consisting of natural Uranium. These two have two different activities and abundances.

Geant4 wants the abundances to be normalized so this is done in this program as well.

'''
# Calculate core activites
for nuclide in core_ingrowth.nuclides:
    nuclideName = str(nuclide)
    core_activities[nuclideName] = float(core_ingrowth.activities('Bq')[nuclideName])

with open("core_activities.json", "w") as f:
    json.dump(core_activities, f, indent=4)


# Calculate core abundances
core_abundances = core_ingrowth.numbers()
core_N_nuclides = sum([float(core_abundances[key]) for key in core_abundances.keys()])
for nuclide in core_ingrowth.nuclides:
    nuclideName = str(nuclide)
    core_abundances_relative[nuclideName] = float(core_ingrowth.numbers()[nuclideName])/core_N_nuclides

with open("core_abundances.json", "w") as f:
    json.dump(core_abundances_relative, f, indent=4)


# Calculate shield activites
for nuclide in shield_ingrowth.nuclides:
    nuclideName = str(nuclide)
    shield_activities[nuclideName] = float(shield_ingrowth.activities('Bq')[nuclideName])

with open("shield_activities.json", "w") as f:
    json.dump(shield_activities, f, indent=4)


# Calculate shield abundances
shield_abundances = shield_ingrowth.numbers()
shield_N_nuclides = sum([float(shield_abundances[key]) for key in shield_abundances.keys()])
for nuclide in shield_ingrowth.nuclides:
    nuclideName = str(nuclide)
    shield_abundances_relative[nuclideName] = float(shield_ingrowth.numbers()[nuclideName])/shield_N_nuclides

with open("shield_abundances.json", "w") as f:
    json.dump(shield_abundances_relative, f, indent=4)

