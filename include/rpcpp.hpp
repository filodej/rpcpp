#ifndef __RPCPP_INCLUDED_HPP__
#define __RPCPP_INCLUDED_HPP__
 
#include <boost/shared_ptr.hpp>
#include <string>
#include "./echo.hpp"
#include "./api_helper.hpp"

#ifdef RPCPP_DLL // defined if RPCPP is compiled as a DLL
  #ifdef RPCPP_DLL_EXPORTS // defined if we are building the FOX DLL (instead of using it)
    #define RPCPP_API API_DLL_EXPORT
  #else
    #define RPCPP_API API_DLL_IMPORT
  #endif // RPCPP_DLL_EXPORTS
  #define RPCPP_LOCAL API_DLL_LOCAL
#else // RPCPP_DLL is not defined: this means RPCPP is a static lib.
  #define RPCPP_API
  #define RPCPP_LOCAL
#endif // RPCPP_DLL

//typedef boost::shared_ptr<echo<std::string> const> str_echo_cptr;
//typedef boost::shared_ptr<echo<int> const>         int_echo_cptr;

//typedef boost::intrusive_ptr<echo const> echo_cptr;
// http://osdir.com/ml/programming.swig/2004-09/msg00097.html

template<class T>
extern boost::shared_ptr<echo<T> const> RPCPP_API create_echo();

template <class T>
extern double RPCPP_API benchmark( echo<T> const& e, T const& value, int walk_count );

#endif //__RPCPP_INCLUDED_HPP__
