#include "PMDetectorConstruction.hh"
#include "DecayHelper.hh"
#include <string>
#include "json.hpp"
using json = nlohmann::json;

PMDetectorConstruction::PMDetectorConstruction(int time)
{
    time = time;
}

PMDetectorConstruction::~PMDetectorConstruction()
{
}

G4Material* GetMaterial(std::string file_name)
// Output: The G4Material* that exists after that time.
{
    // Open file with error checking
    std::ifstream abundances_file(file_name);
    if (!abundances_file.is_open()) {
        throw std::runtime_error("Could not open file " + file_name);
    }

    // Parse JSON
    json json_data;
    abundances_file >> json_data;

    G4int N_elements = json_data.size();

    G4Material* material = new G4Material("Material", 19.1*g/cm3, N_elements);

    G4NistManager* nist = G4NistManager::Instance();
    int z;
    int a;
    std::string a_string;
    std::string symbol;

    for (auto& [key, value] : json_data.items()) {
        a_string.erase();
        symbol.erase();

        // nist->GetZ takes the symbol only as input. Have to extract that.
        size_t pos = key.find('-');
        symbol = key.substr(0,pos);
        z = nist->GetZ(symbol);

        // Remove all non-digit characters to get the value of a, convvert to int
        for (char c : key) {
            if (std::isdigit(static_cast<unsigned char>(c))) {
                a_string += c;
            }
        }
        // Make string an int
        a = std::stoi(a_string);

        G4double mass = G4ParticleTable::GetParticleTable()->GetIonTable()->GetIonMass(z, a) / 931.494061; // Convert to g/mole
        G4Element *element = new G4Element("element", key, z, mass * g/mole);
        material->AddElement(element, value.get<double>());
    }
    return material;

} 

G4LogicalVolume* PMDetectorConstruction::GetLayer(G4double radiusInner, G4double radiusOuter, G4Material* material, G4String name) {
    // Each layer is constructed similarly, the difference between them are, the radius and material 
    G4bool checkOverlaps = true;

    G4Sphere *solid = new G4Sphere("solid" + name, radiusInner, radiusOuter, 0.0, 360. * deg, 0.0, 180. * deg);
    G4LogicalVolume* logic = new G4LogicalVolume(solid, material, "logic" + name);
    G4VPhysicalVolume *physic = new G4PVPlacement(0, G4ThreeVector(0.,0.,0.), logic, "phys" + name, logicWorld, 0, checkOverlaps);
    return logic;
}

/*  
    G4Sphere* solidDetector = new G4Sphere("solidDetector", detectorRadiusInner, detectorRadiusOuter, 0., 360. * deg, 0., 180.*deg);
    logicDetector = new G4LogicalVolume(solidDetector, worldMat, "logicDetector");
    G4VPhysicalVolume* physDetector = new G4PVPlacement(nullptr, G4ThreeVector(0.,0.,0.), logicDetector, "physDetector", logicWorld, 0, checkOverlaps);
*/
G4VPhysicalVolume *PMDetectorConstruction::Construct()
{
    G4bool checkOverlaps = true;

/* 
###########################################################
                        Define Materials
###########################################################
*/

// Nuclear weapon is constructed, from the inside out, by:
// Air
// Fissile material, U or Pu, Using bateman to solve for concentration
// Neutron reflector, Be
// Tamper, Th
// High Explosive, TNT
// Casing, U
// Surrounding, Air


    G4NistManager *nist = G4NistManager::Instance();


//------------------------------ Air -------------------------------------
    G4Material *worldMat = nist->FindOrBuildMaterial("G4_AIR");


//--------------- Fissile material, Open the Bateman solution --------------
    G4Material* sourceMat = nist->FindOrBuildMaterial("G4_U");


//------------------------Neutron reflector---------------------------------
    G4Material* refMat = nist->FindOrBuildMaterial("G4_Be"); //G4_Be


//---------------------------- Tamper --------------------------------------
    G4Material* tampMat = nist->FindOrBuildMaterial("G4_Th"); //G4_Th


//-------------------------High Explosive----------------------------------
    // Create TNT material

    G4Material* TNT = new G4Material("TNT", 1.65 * g/cm3, 4);
    
    // Define the required elements
    G4Element* H = nist->FindOrBuildElement("H"); //G4_H
    G4Element* C = nist->FindOrBuildElement("C"); //G4_C
    G4Element* N = nist->FindOrBuildElement("N"); //G4_N
    G4Element* O = nist->FindOrBuildElement("O"); //G4_O

    // TNT has (CH3C6H2(NO2)3) which results in:
    TNT->AddElement(H, 2);  // 2 hydrogen atoms
    TNT->AddElement(C, 7);  // 7 carbon atom
    TNT->AddElement(N, 3);  // 3 nitrogen atoms
    TNT->AddElement(O, 6);  // 6 oxygen atoms


//---------------------------Casing---------------------------------------
    G4Material* casingMat = nist->FindOrBuildMaterial("G4_Al"); //G4_Al


//---------------------------Shield---------------------------------------
    G4Material* shieldMat = nist->FindOrBuildMaterial("G4_U"); //G4_U

    


/* 
###########################################################
        Create Objects with the defined materials
###########################################################
*/
// The model that is to be designed consists of the dimensions:
// Air
//
// Fissile material, HEU or WgPu, Using bateman to solve for concentration
// Neutron reflector, Be
// High Explosive, TNT
// Radiation Case Shield, DU
// Casing, Al
// Surrounding, Air

    // Load variables defined in the python script
    // Open file with error checking
    std::ifstream geometry_variables("../geometry_variables.json");
    if (!geometry_variables.is_open()) {
        throw std::runtime_error("Could not open file ../geometry_variables.json");
    }

    // Parse JSON
    json json_data;
    geometry_variables >> json_data;

    // Define variables
    G4double xWorld = 1.2 * m;
    G4double yWorld = 1.2 * m;
    G4double zWorld = 1.2 * m;


    // Create world
    G4Box *solidWorld = new G4Box("solidWorld", 0.5 * xWorld, 0.5 * yWorld, 0.5 * zWorld);
    logicWorld = new G4LogicalVolume(solidWorld, worldMat, "logicalWorld");
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "physWorld", 0, false, 0, checkOverlaps);


    // Create core
    logicCore = GetLayer(json_data["Core"]["inner"].get<double>()*cm, json_data["Core"]["outer"].get<double>()*cm, sourceMat, "Core");

    // Create reflector
    logicReflector = GetLayer(json_data["Reflector"]["inner"].get<double>()*cm, json_data["Reflector"]["outer"].get<double>()*cm, refMat, "Reflector");

    // Create HE
    logicHE = GetLayer(json_data["HE"]["inner"].get<double>()*cm, json_data["HE"]["outer"].get<double>()*cm, TNT, "HE");

    // Create radiation case
    logicRadiationCase = GetLayer(json_data["RadiationCase"]["inner"].get<double>()*cm, json_data["RadiationCase"]["outer"].get<double>()*cm, casingMat, "RadiationCase");

    // Create casing
    logicCasing = GetLayer(json_data["Casing"]["inner"].get<double>()*cm, json_data["Casing"]["outer"].get<double>()*cm, casingMat, "Casing");

    return physWorld;
}

void PMDetectorConstruction::ConstructSDandField()
{
    auto SDManager = G4SDManager::GetSDMpointer();

    // Create, Initiate and Apply the respective SD to each logic volume
    if (logicCore != nullptr){
        auto SDCore = new PMSensitiveDetector("SDCore");
        SDManager->AddNewDetector(SDCore);
        logicCore->SetSensitiveDetector(SDCore);
    }
    if (logicReflector != nullptr){
        auto SDReflector = new PMSensitiveDetector("SDReflector");
        SDManager->AddNewDetector(SDReflector);
        logicReflector->SetSensitiveDetector(SDReflector);
    }
    if (logicHE != nullptr){
        auto SDHE = new PMSensitiveDetector("SDHE");
        SDManager->AddNewDetector(SDHE);
        logicHE->SetSensitiveDetector(SDHE);
    }   
    if (logicRadiationCase != nullptr){
        auto SDRadiationCasing = new PMSensitiveDetector("SDRadiationCasing");
        SDManager->AddNewDetector(SDRadiationCasing);
        logicRadiationCase->SetSensitiveDetector(SDRadiationCasing);
    }     
    if (logicCasing != nullptr){
        auto SDCasing = new PMSensitiveDetector("SDCasing");
        SDManager->AddNewDetector(SDCasing);
        logicCasing->SetSensitiveDetector(SDCasing);
    }     

}