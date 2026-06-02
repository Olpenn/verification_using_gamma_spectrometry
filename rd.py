import radioactivedecay as rd
import numpy as np
import matplotlib.pyplot as plt

def main(nuclide_input):
    # Set a specific start
    core = rd.Inventory({nuclide_input : 1000}, 'Bq')

    X = np.logspace(-5, 10, num=100) # Time in years
    activities_dict = dict()

    # Initialize the activities dictionary with empty lists for each nuclide
    time = X[0]
    core_ingrowth = core.decay(time, 'y')
    
    # Get activities as a dict {nuclide: activity}
    activities = core_ingrowth.activities()

    # Sort nuclides by decreasing activity
    sorted_nuclides = sorted(activities.items(), key=lambda x: x[1], reverse=True)

    # If you only want the nuclide names:
    nuclide_names = [nuc for nuc, act in sorted_nuclides]

    for nuclide in nuclide_names:
        activities_dict[nuclide] = [float(activities[nuclide])]

    # Calculate ingrowth after a certaion time
    for time in X[1:]:
        core_ingrowth = core.decay(time, 'y')
        for nuclide in core_ingrowth.nuclides:
            nuclide = str(nuclide)
            activities_dict[nuclide].append(float(core_ingrowth.activities("Bq")[nuclide]))


    plt.figure(figsize=(10, 5), dpi=300)
    ax = plt.gca()



    # Plot the activities
    for nuclide in nuclide_names:
        activity_list = activities_dict[nuclide]
        activity_list = np.array(activity_list)
        plt.plot(X, activity_list/1000, label=nuclide)

    ax.set_xscale('log')
    plt.title(f"Activity of nuclides from decay of {nuclide_input} over time")
    plt.xlabel("Time (years)")
    plt.xticks(fontsize=14, fontweight='bold')
    plt.ylabel(r"Relative Activity ($A/A_0$)")
    plt.legend(fontsize='small')
    plt.savefig(f"activities_{nuclide_input}.png")

if __name__ == "__main__":
    main("U-235")
    main("U-238")
    main("U-234")