#ifndef __ECHO_INCLUDED_HPP__
#define __ECHO_INCLUDED_HPP__
 
#include <boost/noncopyable.hpp>
#include <boost/shared_ptr.hpp>
#include <string>
#include "api_helper.hpp"

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


template <class T>
class RPCPP_API echo : public boost::noncopyable
{
 public:
    virtual T call( T const& value ) const = 0;
    virtual ~echo() {};
 private:
};

typedef boost::shared_ptr<echo<std::string> const> str_echo_cptr;
typedef boost::shared_ptr<echo<int> const>         int_echo_cptr;

//typedef boost::intrusive_ptr<echo const> echo_cptr;

// http://osdir.com/ml/programming.swig/2004-09/msg00097.html

template<class T>
extern RPCPP_API boost::shared_ptr<echo<T> const> create_echo();

template <class T>
extern RPCPP_API double benchmark( echo<T> const& e, T const& value, int walk_count );

#endif //__ECHO_INCLUDED_HPP__
