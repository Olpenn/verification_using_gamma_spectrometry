#pragma once

#include "G4VSensitiveDetector.hh"

#include "G4AnalysisManager.hh"
#include "G4Gamma.hh"
#include "G4Electron.hh"
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"
#include "G4VProcess.hh"
#include <map>




class PMSensitiveDetector : public G4VSensitiveDetector
{
public:
    PMSensitiveDetector(G4String);
    ~PMSensitiveDetector();

private:
    virtual void Initialize(G4HCofThisEvent *) override;
    virtual void EndOfEvent(G4HCofThisEvent *) override;

    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory *);
};