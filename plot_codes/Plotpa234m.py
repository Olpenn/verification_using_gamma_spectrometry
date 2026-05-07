import requests
import pandas as pd
import matplotlib.pyplot as plt

url = (
    "https://www.nndc.bnl.gov/nudat3/"
    "decaysearchdirect.jsp?nuc=234Pa&unc=nds"
)

# Pretend to be a normal browser
headers = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)

# Check request succeeded

# Parse HTML tables
tables = pd.read_html(response.text)


# Inspect tables

table = tables[11]

energies = [float(x.split()[0]) for x in table[1][1:] if pd.notnull(x)]
intensities = [float(y.split()[0]) for y in table[2][1:] if pd.notnull(y)]

plt.figure(figsize=(10, 5))

plt.bar(
    energies,
    intensities,
    width=5  # keV width of bars
)

plt.annotate(
    f"1001 keV",
    xy=(1001, 0.842),  # Example coordinates, replace with actual values
    xytext=(7, -50),  # vertical offset
    textcoords="offset points",
    ha="center",
    fontsize=10,
    rotation=-90
)

plt.annotate(
    f"766.4 keV",
    xy=(766.4, 0.317),  # Example coordinates, replace with actual values
    xytext=(7, -50),  # vertical offset
    textcoords="offset points",
    ha="center",
    fontsize=10,
    rotation=-90
)

plt.xlim(0, 2000)

plt.title("Relative gamma energy intensity of the decay of Pa234m")
plt.xlabel("Energy (keV)")
plt.ylabel("Intensity (%)")

plt.savefig("Pa234m_gamma_rays.png", dpi=300)