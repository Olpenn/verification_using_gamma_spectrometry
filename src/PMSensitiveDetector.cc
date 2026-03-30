#include "PMSensitiveDetector.hh"
#include "PMRunAction.hh"


PMSensitiveDetector::PMSensitiveDetector(G4String name) : G4VSensitiveDetector(name) 
{
}

PMSensitiveDetector::~PMSensitiveDetector() {}

void PMSensitiveDetector::Initialize(G4HCofThisEvent *) 
{
}

void PMSensitiveDetector::EndOfEvent(G4HCofThisEvent *)
{   
}

G4bool PMSensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *)
{    
    G4Track* track = aStep->GetTrack();

    auto trackDefinition = track->GetDefinition();
    auto postStep = aStep->GetPostStepPoint();
    G4double ke = postStep->GetKineticEnergy();

    auto analysis = G4AnalysisManager::Instance();
    G4String exitingVolumeName = aStep->GetPreStepPoint()->GetPhysicalVolume()->GetName();

    if (trackDefinition == G4Gamma::Definition() && aStep->GetPostStepPoint()->GetStepStatus() == fGeomBoundary) {
        G4String exitingVolumeName = aStep->GetPreStepPoint()->GetPhysicalVolume()->GetName();
        G4String enteringVolumeName = aStep->GetPostStepPoint()->GetPhysicalVolume()->GetName();
        
        G4int histID = 
        exitingVolumeName=="physCore" && enteringVolumeName=="physReflector"        ? 0 :
        exitingVolumeName=="physReflector" && enteringVolumeName=="physHE"          ? 1 :
        exitingVolumeName=="physHE" && enteringVolumeName=="physRadiationCase"      ? 2 :
        exitingVolumeName=="physRadiationCase" && enteringVolumeName=="physCasing"  ? 3 :
        exitingVolumeName=="physCasing" && enteringVolumeName=="physWorld"          ? 4 : -1;

        // If histID = -1, the gamma ray bounces backwards towards the center
        if (histID != -1) {
            analysis->FillH1(histID, ke);
        }        
    }
    
    return true;
}

 