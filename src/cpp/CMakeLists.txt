#if (CMAKE_COMPILER_IS_GNUCXX AND USE_GCC_VISIBILITY)
#  # visibility support
#  check_cxx_compiler_flag(-fvisibility=hidden __HAVE_GCC_VISIBILITY)
#endif(CMAKE_COMPILER_IS_GNUCXX AND USE_GCC_VISIBILITY)

#if ( __HAVE_GCC_VISIBILITY )
   SET ( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fvisibility=hidden -fvisibility-inlines-hidden -DRPCPP_DLL -DRPCPP_DLL_EXPORTS" )
#endif ( __HAVE_GCC_VISIBILITY )

add_library (rpcpp SHARED echo.cxx) 