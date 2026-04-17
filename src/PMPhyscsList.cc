#include "PMPhysicsList.hh"

PMPhysicsList::PMPhysicsList() {
    
    // Import Physics

    // EM Physics
    RegisterPhysics(new G4EmStandardPhysics_option4(0));

    // Radioactive Decay Physics
    RegisterPhysics(new G4RadioactiveDecayPhysics(0));

    // Decay Physics
    RegisterPhysics(new G4DecayPhysics(0));

    // Ion Physics
    RegisterPhysics(new G4IonPhysics(0));
}

PMPhysicsList::~PMPhysicsList() {}