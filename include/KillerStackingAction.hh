// KillerStackingAction.hh
#ifndef KILLERSTACKINGACTION_HH
#define KILLERSTACKINGACTION_HH

#include "G4UserStackingAction.hh"
#include "G4Track.hh"
#include "G4Ions.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"
#include <string>

class KillerStackingAction : public G4UserStackingAction {
public:
    int killAllIfThisTrackDecays = -1;
    bool killAll = false;
    KillerStackingAction() = default;
    virtual ~KillerStackingAction() = default;
    
    virtual G4ClassificationOfNewTrack ClassifyNewTrack(const G4Track* track) override {

        // Get the particle definition
        const G4ParticleDefinition* particle = track->GetDefinition();
        auto particleType = particle->GetParticleType();

        G4String particleName = particle->GetParticleName();

        
        if(particleName == "e-" || particleName == "anti_nu_e") {
            return fKill;
        }

        G4Ions* ion = (G4Ions*)particle;

        // As soon as the daughter particle goes into a non-excited state, set this track to be watched
        if (particleType == "nucleus" && particleName != "alpha" && track->GetParentID() != 0) {
            
            G4double energy = ion->GetExcitationEnergy();
                        
            if (energy == 0.) {
                // Kill all tracks if this track decays
                return fKill;
            }
        }

        
        // Process all other tracks normally
        return fUrgent;
    }
};

#endif