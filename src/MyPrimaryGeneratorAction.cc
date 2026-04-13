#include "MyPrimaryGeneratorAction.hh"
#include "G4IonTable.hh"
#include "DecayHelper.hh"
#include "G4Event.hh"
#include "G4SystemOfUnits.hh"
#include "json.hpp"
#include "Randomize.hh"
#include <fstream>
#include <algorithm>
using json = nlohmann::json;



MyPrimaryGeneratorAction::MyPrimaryGeneratorAction() {
    fGPS = new G4GeneralParticleSource();
}


void MyPrimaryGeneratorAction::SetupIonSources() {
    // Clear default source
    fGPS->ClearAll();
    G4bool core_emission = false;
    G4bool background_emission = true;
    G4double photon_energy = 0.1857*MeV; 
    
    if(photon_energy) {
        fGPS->AddaSource(1); // Add a source with intensity 1 (the intensity will be scaled later in the analysis stage)
        G4SingleParticleSource* source = fGPS->GetCurrentSource();
        source->SetParticleDefinition(G4Gamma::GammaDefinition());
        source->GetEneDist()->SetMonoEnergy(photon_energy);
        source->GetPosDist()->SetPosDisType("Volume");
        source->GetPosDist()->SetPosDisShape("Sphere");
        // Load variables defined in the python script
        // Open file with error checking
        std::ifstream geometry_variables("../geometry_variables.json");
        if (!geometry_variables.is_open()) {
            throw std::runtime_error("Could not open file ../geometry_variables.json");
        }
        // Parse JSON
        json geometry_data;
        geometry_variables >> geometry_data;
        if(core_emission) {
             G4double coreOuterRadius = geometry_data["Core"]["outer"].get<double>()*cm;
             source->GetPosDist()->SetRadius(coreOuterRadius);
             source->GetPosDist()->ConfineSourceToVolume("physCore");
        } 
        if(geometry_data.contains("RadiationCase")) {
            G4double coreOuterRadius = geometry_data["RadiationCase"]["outer"].get<double>()*cm;
            source->GetPosDist()->SetRadius(coreOuterRadius);
            source->GetPosDist()->ConfineSourceToVolume("physRadiationCase");
        } else if (geometry_data.contains("Tamper")) {
            G4double tamperOuterRadius = geometry_data["Tamper"]["outer"].get<double>()*cm;
            G4cout << "Setting photon source radius to " << tamperOuterRadius << std::endl;
            source->GetPosDist()->SetRadius(tamperOuterRadius);
            source->GetPosDist()->ConfineSourceToVolume("physTamper");
        }

        // Set isotropic direction
        source->GetAngDist()->SetAngDistType("iso");
    }
    else if(core_emission) {
        // Open file with error checking
        std::ifstream activities_core("../core_activities.json");
        if (!activities_core.is_open()) {
            throw std::runtime_error("Could not open file '../core_activities.json'");
        }
        
        // Parse JSON
        json j_activities_core;
        activities_core >> j_activities_core;
        G4NistManager* nist = G4NistManager::Instance();
        int z;
        int a;
        std::string a_string;
        std::string symbol;
        G4ParticleDefinition* ion;

        G4double energy;

        // Add each nuclide as a separate source
        for (auto& [key, value] : j_activities_core.items()) {
            a_string.erase();
            symbol.erase();

            // nist->GetZ takes the symbol only as input. Have to extract that.
            size_t pos = key.find('-');
            symbol = key.substr(0,pos);
            z = nist->GetZ(symbol);

            // Remove all non-digit characters to get the value of a, convvert to int
            for (char c : key) {
                if (std::isdigit(static_cast<unsigned char>(c))) {
                    a_string += c;
                }
            }
            // Make string an int
            a = std::stoi(a_string);

            // Add source with its activity as intensity
            fGPS->AddaSource(value);
            
            // Configure this source
            G4SingleParticleSource* source = fGPS->GetCurrentSource();
            
            // The way to define metastable states is to define the exitation energy.
            energy = key=="Pa-234m"? 73.92*keV : 0; 

            ion = G4IonTable::GetIonTable()->GetIon(
                z, 
                a, 
                energy  // excitation energy
            );

            // Set as ion
            source->SetParticleDefinition(ion);
            
            // Set kinetic energy
            source->GetEneDist()->SetMonoEnergy(0.0);
            
            // Set position distribution as a uniform sphere with minimal radius r_min and maximal radius r_max
            source->GetPosDist()->SetPosDisType("Volume");
            source->GetPosDist()->SetPosDisShape("Sphere");
            // Load variables defined in the python script
            // Open file with error checking
            std::ifstream geometry_variables("../geometry_variables.json");
            if (!geometry_variables.is_open()) {
                throw std::runtime_error("Could not open file ../geometry_variables.json");
            }
            // Parse JSON
            json geometry_data;
            geometry_variables >> geometry_data;
            G4double coreOuterRadius = geometry_data["Core"]["outer"].get<double>()*cm;
            source->GetPosDist()->SetRadius(coreOuterRadius);
            source->GetPosDist()->ConfineSourceToVolume("physCore");
            

            // Set isotropic direction
            source->GetAngDist()->SetAngDistType("iso");
        }
    }
    else if(background_emission) {
        // Open file with error checking
        std::ifstream activities_background("../background_activities.json");
        if (!activities_background.is_open()) {
            throw std::runtime_error("Could not open file '../background_activities.json'");
        }
        
        // Parse JSON
        json j_activities_background;
        activities_background >> j_activities_background;

        // Initialize varables
        G4NistManager* nist = G4NistManager::Instance();
        int z;
        int a;
        std::string a_string;
        std::string symbol;
        G4ParticleDefinition* ion;
        G4double energy;

        // Add each nuclide as a separate source
        for (auto& [key, value] : j_activities_background.items()) {
            a_string.erase();
            symbol.erase();

            // nist->GetZ takes the symbol only as input. Have to extract that.
            size_t pos = key.find('-');
            symbol = key.substr(0,pos);
            z = nist->GetZ(symbol);

            // Remove all non-digit characters to get the value of a, convvert to int
            for (char c : key) {
                if (std::isdigit(static_cast<unsigned char>(c))) {
                    a_string += c;
                }
            }
            // Make string an int
            a = std::stoi(a_string);

            // Add source with its activity as intensity
            fGPS->AddaSource(value);
            
            // Configure this source
            G4SingleParticleSource* source = fGPS->GetCurrentSource();
            
            // The way to define metastable states is to define the exitation energy.
            energy = key=="Pa-234m"? 73.92*keV : 0; 

            ion = G4IonTable::GetIonTable()->GetIon(
                z, 
                a, 
                energy  // excitation energy
            );

            // Set as ion
            source->SetParticleDefinition(ion);
            
            // Set kinetic energy
            source->GetEneDist()->SetMonoEnergy(0.0);
            
            // Set position distribution as a uniform sphere with minimal radius r_min and maximal radius r_max
            source->GetPosDist()->SetPosDisType("Volume");
            source->GetPosDist()->SetPosDisShape("Sphere");
            // Load variables defined in the python script
            // Open file with error checking
            std::ifstream geometry_variables("../geometry_variables.json");
            if (!geometry_variables.is_open()) {
                throw std::runtime_error("Could not open file ../geometry_variables.json");
            }
            // Parse JSON
            json geometry_data;
            geometry_variables >> geometry_data;
            if(geometry_data.contains("RadiationCase")) {
                G4double coreOuterRadius = geometry_data["RadiationCase"]["outer"].get<double>()*cm;
                source->GetPosDist()->SetRadius(coreOuterRadius);
                source->GetPosDist()->ConfineSourceToVolume("physRadiationCase");
            } else if (geometry_data.contains("Tamper")) {
                G4double tamperOuterRadius = geometry_data["Tamper"]["outer"].get<double>()*cm;
                G4cout << "Setting background source radius to " << tamperOuterRadius << std::endl;
                source->GetPosDist()->SetRadius(tamperOuterRadius);
                source->GetPosDist()->ConfineSourceToVolume("physTamper");
            }

            // Set isotropic direction
            source->GetAngDist()->SetAngDistType("iso");
        }
    }

}

MyPrimaryGeneratorAction::~MyPrimaryGeneratorAction() {
    delete fGPS;
}

void MyPrimaryGeneratorAction::GeneratePrimaries(G4Event* event) {

    G4SingleParticleSource* source = fGPS->GetCurrentSource();
    fGPS->GeneratePrimaryVertex(event);

    G4int nVertices = event->GetNumberOfPrimaryVertex();
}