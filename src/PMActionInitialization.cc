#include "PMActionInitialization.hh"
#include "KillerStackingAction.hh"

PMActionInitialization::PMActionInitialization()
{}

PMActionInitialization::~PMActionInitialization()
{}

void PMActionInitialization::BuildForMaster() const {
    SetUserAction(new PMRunAction());
}

void PMActionInitialization::Build() const
{  
    // Implement the GPS
    SetUserAction(new MyPrimaryGeneratorAction());

    // Implement run action
    SetUserAction(new PMRunAction());


    SetUserAction(new KillerStackingAction());
}
