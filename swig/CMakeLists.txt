include(UseSWIG)

include_directories (${PROJECT_SOURCE_DIR}/include ${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_PATH} )
#include_directories (${JAVA_INCLUDE_PATH})

link_directories    (${PROJECT_SOURCE_DIR}/bin) 
link_directories    (${PYTHON_LIBRARY_PATH})

set(CMAKE_SWIG_OUTDIR ${LIBRARY_OUTPUT_PATH})
set(CMAKE_SWIG_FLAGS "")
set_source_files_properties(rpcppy.i PROPERTIES CPLUSPLUS ON)
set_source_files_properties(rpcppy.i PROPERTIES SWIG_FLAGS "-Wall;-DSCI_NOPERSISTENT")

set( rpcppy_HEADER_FILES
     shared_ptr.i 
     echo.i 
     )

set_source_files_properties(
    ${rpcppy_HEADER_FILES}
    PROPERTIES
    HEADER_FILE_ONLY TRUE
    )

swig_add_module(rpcppy python rpcppy.i)
swig_link_libraries(rpcppy rpcpp ${PYTHON_LIBRARIES} )
set_target_properties(_rpcppy PROPERTIES SUFFIX ".pyd")

#swig_add_module(rpcppj java rpcppj.i)
#swig_link_libraries(rpcppj rpcpp ${JAVA_LIBRARIES} )
