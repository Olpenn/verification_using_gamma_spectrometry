#include "PMRunAction.hh"


PMRunAction::PMRunAction()
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();
    G4double Emin = 0.;
    G4double Emax = 3.0 * MeV;
    G4int nBins = 30000;

    analysisManager->CreateH1("Core",           "Energy of Gamma rays exiting the Core",            nBins, Emin, Emax, "MeV");
    analysisManager->CreateH1("Reflector",      "Energy of Gamma rays exiting the Reflector",       nBins, Emin, Emax, "MeV");
    analysisManager->CreateH1("Tamper",         "Energy of Gamma rays exiting the Tamper",          nBins, Emin, Emax, "MeV");
    analysisManager->CreateH1("HE",             "Energy of Gamma rays exiting the HE",              nBins, Emin, Emax, "MeV");
    analysisManager->CreateH1("RadiationCase",  "Energy of Gamma rays exiting the Radiation Case",  nBins, Emin, Emax, "MeV");
    analysisManager->CreateH1("Casing",         "Energy of Gamma rays exiting the Casing",          nBins, Emin, Emax, "MeV");
}

PMRunAction::~PMRunAction() {}

void PMRunAction::BeginOfRunAction(const G4Run *run)
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();
    
    G4int runID = run->GetRunID();
    std::stringstream strRunID;
    strRunID << runID;

    analysisManager->OpenFile("data/output" + strRunID.str() + ".root");
}

void PMRunAction::EndOfRunAction(const G4Run *run)
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();


    analysisManager->Write();
    analysisManager->CloseFile();

    //if(G4Threading::IsMasterThread()) {
    //    int result = std::system("root -l -b -q '../beautify.C'");
    //}
}