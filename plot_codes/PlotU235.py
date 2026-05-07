import requests
import pandas as pd
import matplotlib.pyplot as plt

url = (
    "https://www.nndc.bnl.gov/nudat3/"
    "decaysearchdirect.jsp?nuc=235U&unc=nds"
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
table = tables[5]

energies = [float(x.split()[0]) for x in table[1][1:] if pd.notnull(x)]
intensities = [float(y.split()[0]) for y in table[2][1:] if pd.notnull(y)]

plt.figure(figsize=(10,5))

plt.bar(
    energies,
    intensities,
    width=3  # keV width of bars
)

plt.annotate(
    f"185.7 keV",
    xy=(185.7, 57.2),  # Example coordinates, replace with actual values
    xytext=(7, -50),  # vertical offset
    textcoords="offset points",
    ha="center",
    fontsize=10,
    rotation=-90
)

plt.annotate(
    f"13.0 keV",
    xy=(13.0, 27.7),  # Example coordinates, replace with actual values
    xytext=(7, -50),  # vertical offset
    textcoords="offset points",
    ha="center",
    fontsize=10,
    rotation=-90
)

plt.title("Relative gamma energy intensity of the decay of U235")
plt.xlabel("Energy (keV)")
plt.ylabel("Intensity (%)")

plt.savefig("u235_gamma_rays.png", dpi=300)