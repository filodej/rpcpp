cmake_minimum_required (VERSION 2.6)
project (pyecho) 

INCLUDE(FindPythonInterp)
INCLUDE(FindPythonLibs)
INCLUDE(FindSWIG)
FIND_PACKAGE(SWIG REQUIRED)
FIND_PACKAGE(Boost REQUIRED)

SET(BUILD_SHARED_LIBS ON)
SET(CMAKE_VERBOSE_MAKEFILE ON)

SET(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin CACHE INTERNAL
  "Single output directory for building all libraries.")
SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin CACHE INTERNAL
  "Single output directory for building all executables.")
  
add_subdirectory (src) 
add_subdirectory (swig)
