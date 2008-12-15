#ifndef __API_HELPER_H__
#define __API_HELPER_H__

// Generic helper definitions for shared library support
#if defined _WIN32 || defined __CYGWIN__
  #define API_DLL_IMPORT __declspec(dllimport)
  #define API_DLL_EXPORT __declspec(dllexport)
  #define API_DLL_LOCAL
#else
  #if __GNUC__ >= 4
    #define API_DLL_IMPORT __attribute__ ((visibility("default")))
    #define API_DLL_EXPORT __attribute__ ((visibility("default")))
    #define API_DLL_LOCAL  __attribute__ ((visibility("hidden")))
  #else
    #define API_DLL_IMPORT
    #define API_DLL_EXPORT
    #define API_DLL_LOCAL
  #endif
#endif

#endif //  __API_HELPER_H__

