cmake_minimum_required(VERSION 3.16)


project(sim)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


# Find Geant4
option(WITH_GEANT4_UIVIS "Build example with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()
include(${Geant4_USE_FILE})

# Find ROOT
set(ROOT_DIR "home/olovrahm/root/cmake" CACHE PATH "ROOT installation directory")
find_package(ROOT CONFIG REQUIRED) 


# Explicitly add ROOT include directories
set(ROOT_INCLUDE_DIR "/home/olovrahm/root/include")
include_directories(${ROOT_INCLUDE_DIR})

# Also include the ROOT subdirectory if needed
include_directories("${ROOT_INCLUDE_DIR}/ROOT")



execute_process(
  COMMAND ${ROOT_CONFIG} --libs
  OUTPUT_VARIABLE ROOT_INCLUDE_LIBRARIES
  OUTPUT_STRIP_TRAILING_WHITESPACE
)



include_directories(${PROJECT_SOURCE_DIR}/include 
${Geant4_CXX_FLAGS} ${ROOT_CXX_FLAGS})


file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/.h)
file(GLOB MACRO_FILES "macros/*.mac")
file(COPY ${MACRO_FILES} DESTINATION ${CMAKE_BINARY_DIR}/)


add_executable(sim sim.cc ${sources} ${headers})

target_link_libraries(
  sim 
  ${Geant4_LIBRARIES}
  ${ROOT_LIBRARIES}
)