import json

def get_bg_activities(photon_energy):
    with open('data/background_activities.json') as json_data:
        d = json.load(json_data)
        json_data.close()
        if photon_energy == 185.7:
            photon185keV_activity = d["U-235"] * 0.572
            return photon185keV_activity
        elif photon_energy == 1001.0:
            photon1001keV_activity = d["Pa-234m"] * 0.00842
            return photon1001keV_activity
        else:
            raise ValueError("Photon energy must be either 185.7 or 1001.0 keV.")


def get_core_activities(photon_energy):
    with open('data/core_activities.json') as json_data:
        d = json.load(json_data)
        json_data.close()
        if photon_energy == 185.7:
            photon185keV_activity = d["U-235"] * 0.572
            return photon185keV_activity
        elif photon_energy == 1001.0:
            photon1001keV_activity = d["Pa-234m"] * 0.00842
            return photon1001keV_activity
        else:
            raise ValueError("Photon energy must be either 185.7 or 1001.0 keV.")