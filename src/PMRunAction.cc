#include "PMRunAction.hh"


PMRunAction::PMRunAction()
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();
    G4double Emin = 0.;
    G4double Emax = 2.3 * MeV;
    G4int nBins = 10000;

    analysisManager->CreateH1("Source",     "Energy of Gamma rays exiting the Source",      nBins, Emin, Emax);
    analysisManager->CreateH1("Reflector",  "Energy of Gamma rays exiting the Reflector",   nBins, Emin, Emax);
    analysisManager->CreateH1("Tamper",     "Energy of Gamma rays exiting the Tamper",      nBins, Emin, Emax);
    analysisManager->CreateH1("HE",         "Energy of Gamma rays exiting the HE",          nBins, Emin, Emax);
    analysisManager->CreateH1("Casing",     "Energy of Gamma rays exiting the Casing",      nBins, Emin, Emax);
    analysisManager->CreateH1("Shield",     "Energy of Gamma rays exiting the Shield",      nBins, Emin, Emax);
    analysisManager->CreateH1("Detector",   "Energy of Gamma rays exiting the Detector",    nBins, Emin, Emax);
}

PMRunAction::~PMRunAction() {}

void PMRunAction::BeginOfRunAction(const G4Run *run)
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();
    
    G4int runID = run->GetRunID();
    std::stringstream strRunID;
    strRunID << runID;

    analysisManager->OpenFile("output" + strRunID.str() + ".root");
}

void PMRunAction::EndOfRunAction(const G4Run *run)
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();


    analysisManager->Write();
    analysisManager->CloseFile();

    if(G4Threading::IsMasterThread()) {
        int result = std::system("root -l -b -q '../beautify.C'");
    }
}