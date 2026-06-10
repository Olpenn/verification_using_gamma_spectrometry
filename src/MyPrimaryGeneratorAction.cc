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
    // Initialize with ParticleGun. The ParticleGun will be used when there is no randomization of original source.
    
    // Create particle gun with 1 particle per event
    G4int nParticles = 1;
    fParticleGun = new G4ParticleGun(nParticles);
    
    // Set the particle type to gamma (photon)
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* particle = particleTable->FindParticle("gamma");
    fParticleGun->SetParticleDefinition(particle);
    
    // Direction will be randomized for each event
    // Position will be randomized for each event
}


void MyPrimaryGeneratorAction::SetupIonSources() {
    // This function is not neccesary
}

MyPrimaryGeneratorAction::~MyPrimaryGeneratorAction() {
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
    // Look if we're using the core or radiation case as source of photons.
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