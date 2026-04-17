#pragma once

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4NistManager.hh"
#include "G4GeneralParticleSource.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "globals.hh"
#include "G4Gamma.hh"

class G4Event;

class MyPrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
public:
    MyPrimaryGeneratorAction();
    virtual ~MyPrimaryGeneratorAction();

    virtual void GeneratePrimaries(G4Event* event);
    void SetupIonSources();

private:
    G4GeneralParticleSource* fGPS;
    G4ParticleGun* fParticleGun;
    G4bool photon_emission = true; // Set to true to simulate photon emission instead of ion emission

    G4ThreeVector GetRandomPointInHollowSphere(G4double innerRadius, G4double outerRadius);
};