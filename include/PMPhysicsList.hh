#pragma once

#include "G4VModularPhysicsList.hh"
#include "G4EmStandardPhysics_option4.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4DecayPhysics.hh"
#include "G4StepLimiterPhysics.hh"
#include "G4IonPhysics.hh"
#include "G4GenericIon.hh"
#include "G4NuclideTable.hh"
#include "G4IonConstructor.hh"

class PMPhysicsList : public G4VModularPhysicsList
{
public:
    PMPhysicsList();
    ~PMPhysicsList();
};

