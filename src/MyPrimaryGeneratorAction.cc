#include "MyPrimaryGeneratorAction.hh"
#include "G4IonTable.hh"
#include "DecayHelper.hh"
#include "G4Event.hh"
#include "G4SystemOfUnits.hh"
#include "json.hpp"
#include "Randomize.hh"
#include "G4RandomDirection.hh"
#include <fstream>
#include <algorithm>
using json = nlohmann::json;



MyPrimaryGeneratorAction::MyPrimaryGeneratorAction() {
    // Initialize with both GPS and ParticleGun. The ParticleGun will be used when there is no randomization of original source.
    
    fGPS = new G4GeneralParticleSource();

    // Create particle gun with 1 particle per event
    G4int nParticles = 1;
    fParticleGun = new G4ParticleGun(nParticles);
    
    // Set the particle type to gamma (photon)
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* particle = particleTable->FindParticle("gamma");
    fParticleGun->SetParticleDefinition(particle);
    
    // Direction will be set to point inward/outward as needed
    // Position will be randomized for each event
}


void MyPrimaryGeneratorAction::SetupIonSources() {
    // Load variables defined in the python script
    // Open file with error checking
    std::ifstream geometry_variables("data/geometry_variables.json");
    if (!geometry_variables.is_open()) {
        throw std::runtime_error("Could not open file geometry_variables.json");
    }
    // Parse JSON
    json geometry_data;
    geometry_variables >> geometry_data;
    
    // If we use photon emission, particle gun will be used in another method.
    if(!photon_emission){
        // Clear default source
        fGPS->ClearAll();
        G4bool core_emission = geometry_data["core_emission"].get<bool>();
        G4bool background_emission = !core_emission;
        if(core_emission) {
            // Open file with error checking
            std::ifstream activities_core("data/core_activities.json");
            if (!activities_core.is_open()) {
                throw std::runtime_error("Could not open file 'data/core_activities.json'");
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
                G4double coreOuterRadius = geometry_data["Core"]["outer"].get<double>()*cm;
                source->GetPosDist()->SetRadius(coreOuterRadius);
                source->GetPosDist()->ConfineSourceToVolume("physCore");
                

                // Set isotropic direction
                source->GetAngDist()->SetAngDistType("iso");
            }
        }
        if(background_emission) {
            // Open file with error checking
            std::ifstream activities_background("data/background_activities.json");
            if (!activities_background.is_open()) {
                throw std::runtime_error("Could not open file 'data/background_activities.json'");
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
}

MyPrimaryGeneratorAction::~MyPrimaryGeneratorAction() {
    delete fGPS;
    delete fParticleGun;
}

G4ThreeVector MyPrimaryGeneratorAction::GetRandomPointInHollowSphere(G4double innerRadius, G4double outerRadius) {
    G4double r = std::cbrt(G4UniformRand() * (std::pow(outerRadius, 3) - std::pow(innerRadius, 3)) + std::pow(innerRadius, 3));
    G4ThreeVector direction = G4RandomDirection();
    return r * direction;
}

void MyPrimaryGeneratorAction::GeneratePrimaries(G4Event* event) {
    // Load variables defined in the python script
    // Open file with error checking

    std::ifstream geometry_variables("data/geometry_variables.json");
    if (!geometry_variables.is_open()) {
        throw std::runtime_error("Could not open file data/geometry_variables.json");
    }
    // Parse JSON
    json geometry_data;
    geometry_variables >> geometry_data;

    if (!photon_emission) {
        // In case of ion emission, use GPS to facilitate the randomization of the source.
        G4SingleParticleSource* source = fGPS->GetCurrentSource();
        fGPS->GeneratePrimaryVertex(event);
    }
    else {
        G4double photon_energy;
        if (geometry_data["photon_energy"].get<double>() == 185.7) {
            photon_energy = 185.713*keV; 
        } else if (geometry_data["photon_energy"].get<double>() == 1001.0) {
            photon_energy = 1001.0*keV;             
        } else {
            throw std::runtime_error("Photon energy must be either 185.7 or 1001.0 keV.");
        }
        fParticleGun->SetParticleEnergy(photon_energy);
        G4double innerRadius, outerRadius;
        // In case of photon emission, use particle gun.
        if (geometry_data["core_emission"].get<bool>()) {
            outerRadius = geometry_data["Core"]["outer"].get<double>()*cm;
            innerRadius = geometry_data["Core"]["inner"].get<double>()*cm;
        } else {
            outerRadius = geometry_data["RadiationCase"]["outer"].get<double>()*cm;
            innerRadius = geometry_data["RadiationCase"]["inner"].get<double>()*cm;
        }
        
        // Get random position on the hollow sphere surface
        G4ThreeVector position = GetRandomPointInHollowSphere(innerRadius, outerRadius);
        fParticleGun->SetParticlePosition(position);
        fParticleGun->SetParticleMomentumDirection(G4RandomDirection());

        fParticleGun->GeneratePrimaryVertex(event);
    }
}