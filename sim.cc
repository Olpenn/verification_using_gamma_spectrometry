#include <iostream>

#include "G4RunManager.hh"
#include "G4MTRunManager.hh"
#include "G4UImanager.hh"
#include "G4VisManager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"

#include "PMPhysicsList.hh"
#include "PMDetectorConstruction.hh"
#include "PMActionInitialization.hh"



int main(int argc, char** argv)
{
    int time = 0;
    G4UIExecutive *ui = nullptr;

    #ifdef G4MULTITHREADED
        G4MTRunManager *runManager = new G4MTRunManager;
    #else 
        G4RunManager *runManager = new G4RunManager;
    #endif
    // Physics list
    PMPhysicsList* physicsList = new PMPhysicsList();
    runManager->SetUserInitialization(physicsList);
    
    // Detector Construction
    runManager->SetUserInitialization(new PMDetectorConstruction(time));
    
    // Primary Generator
    MyPrimaryGeneratorAction* primaryAction = new MyPrimaryGeneratorAction();
 
    // Action Initialization
    runManager->SetUserInitialization(new PMActionInitialization());

    runManager->Initialize();
    
    primaryAction->SetupIonSources(); 



    if (argc == 1)
    {
        ui = new G4UIExecutive(argc, argv);
    }

    G4VisManager *visManager  = new G4VisExecutive();
    visManager->Initialize();

    G4UImanager *UImanager = G4UImanager::GetUIpointer();

    if (ui)
    {
        UImanager->ApplyCommand("/control/execute vis.mac");
        ui->SessionStart();
    }
    else 
    {
        G4String command = "/control/execute ";
        G4String fileName = argv[1];
        UImanager->ApplyCommand(command + fileName);
    }
       

    return 0;
}