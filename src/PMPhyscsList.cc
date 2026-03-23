#include "PMPhysicsList.hh"

PMPhysicsList::PMPhysicsList() {
    
    // Import Physics

    // EM Physics
    RegisterPhysics(new G4EmStandardPhysics_option4());

    // Radioactive Decay Physics
    RegisterPhysics(new G4RadioactiveDecayPhysics());

    // Decay Physics
    RegisterPhysics(new G4DecayPhysics());

    // Ion Physics
    RegisterPhysics(new G4IonPhysics());
}

PMPhysicsList::~PMPhysicsList() {}