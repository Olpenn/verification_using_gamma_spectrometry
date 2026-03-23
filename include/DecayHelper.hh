#pragma once

#include <vector>
#include <map>
#include <string>

class DecayHelper {
public:
    struct DecayProduct {
        std::string symbol;
        int z;
        int a;
        double halfLife;
        double decayRate;
        double nuclearMass;
        double relativeAbundance;
        double relativeMass;
    };

    static std::vector<DecayProduct> GetU235DecayComposition(double time);

    static std::vector<DecayHelper::DecayProduct> GetDecayCompisition(std::string nuclideName, double time);

private:
    DecayHelper() = delete;

    static std::map<std::string, double> GetComposition(std::vector<std::pair<std::string, double>> nuclide_decayRate_pairs, double time);

    static const std::map<std::string, double> fDecayConstants;

};
