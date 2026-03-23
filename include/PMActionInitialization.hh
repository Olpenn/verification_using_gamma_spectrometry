#pragma once

#include "G4VUserActionInitialization.hh"

#include "MyPrimaryGeneratorAction.hh"
#include "PMRunAction.hh"

class PMActionInitialization : public G4VUserActionInitialization
{
public:
    PMActionInitialization();
    ~PMActionInitialization();

    virtual void BuildForMaster() const;
    virtual void Build() const;
};