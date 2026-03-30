#pragma once

#include "G4VUserDetectorConstruction.hh"

#include "G4Box.hh"
#include "G4Sphere.hh"
#include "G4Tubs.hh"

#include "G4LogicalVolume.hh"
#include "G4VPhysicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4Material.hh"

#include "G4ParticleTable.hh"
#include "G4IonTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4DecayTable.hh"
#include "G4RadioactiveDecay.hh"
#include "G4GenericIon.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"

#include "G4VisAttributes.hh"
#include "G4Colour.hh"
#include "G4SDManager.hh"
#include "G4UserLimits.hh"
#include <memory>
#include "PMSensitiveDetector.hh"

class PMDetectorConstruction : public G4VUserDetectorConstruction
{
public:
    PMDetectorConstruction(int time);
    virtual ~PMDetectorConstruction();   
    
    virtual G4VPhysicalVolume *Construct();

    

private:
    G4LogicalVolume* logicWorld = nullptr;

    // Declare the logicvolumes in the header to access it in differnet methods later.
    G4LogicalVolume* logicCore = nullptr;
    G4LogicalVolume* logicReflector = nullptr;
    G4LogicalVolume* logicHE = nullptr;
    G4LogicalVolume* logicRadiationCase = nullptr;
    G4LogicalVolume* logicCasing = nullptr;


    G4LogicalVolume* GetLayer(G4double radiusInner, G4double radiusOuter, G4Material* material, G4String name);
    
    virtual void ConstructSDandField(); 

};