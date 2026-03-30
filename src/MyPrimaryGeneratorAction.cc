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
    G4bool radiationCase_emission = true;

    if(core_emission) {
        // Open file with error checking
        std::ifstream activities_file("../core_activities.json");
        if (!activities_file.is_open()) {
            throw std::runtime_error("Could not open file '../core_activities.json'");
        }
        
        // Parse JSON
        json json_data;
        activities_file >> json_data;
        G4NistManager* nist = G4NistManager::Instance();
        int z;
        int a;
        std::string a_string;
        std::string symbol;
        G4ParticleDefinition* ion;

        G4double energy;

        // Add each nuclide as a separate source
        for (auto& [key, value] : json_data.items()) {
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
    if(radiationCase_emission) {
        // Open file with error checking
        std::ifstream activities_file("../radiationCase_activities.json");
        if (!activities_file.is_open()) {
            throw std::runtime_error("Could not open file '../radiationCase_activities.json'");
        }
        
        // Parse JSON
        json json_data;
        activities_file >> json_data;

        // Initialize varables
        G4NistManager* nist = G4NistManager::Instance();
        int z;
        int a;
        std::string a_string;
        std::string symbol;
        G4ParticleDefinition* ion;
        G4double energy;

        // Add each nuclide as a separate source
        for (auto& [key, value] : json_data.items()) {
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
            G4double coreOuterRadius = geometry_data["RadiationCase"]["outer"].get<double>()*cm;
            source->GetPosDist()->SetRadius(coreOuterRadius);
            source->GetPosDist()->ConfineSourceToVolume("physRadiationCase");
            

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