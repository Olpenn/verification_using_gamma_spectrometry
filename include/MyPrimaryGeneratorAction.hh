#pragma once

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4NistManager.hh"
#include "G4GeneralParticleSource.hh"
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
};