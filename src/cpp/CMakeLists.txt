if ( CMAKE_COMPILER_IS_GNUCC )
	add_definitions( -fvisibility=hidden -fvisibility-inlines-hidden )
endif ( CMAKE_COMPILER_IS_GNUCC )
add_definitions(-DRPCPP_DLL)

set( rpcpp_HEADER_FILES
     ../../include/api_helper.hpp 
     ../../include/echo.hpp 
     ../../include/rpcpp.hpp 
     )

set( rpcpp_SOURCE_FILES
     rpcpp.cxx 
     )

set_source_files_properties(
    ${rpcpp_HEADER_FILES}
    PROPERTIES
    HEADER_FILE_ONLY TRUE
    )

add_library (rpcpp SHARED ${rpcpp_HEADER_FILES} ${rpcpp_SOURCE_FILES} ) 

set_target_properties(rpcpp PROPERTIES DEFINE_SYMBOL RPCPP_DLL_EXPORTS )
