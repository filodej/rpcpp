%include "./shared_ptr.i"
%include "std_string.i"
%include <echo.hpp> 

%module(directors="1") rpycpp

%define ECHO_WRAP( NAME, T ) 
//  %rename(echo_ ## NAME) echo<T>;
  %feature("director") echo<T>;
  %template(echo_ ## NAME) echo<T>;
  %template(echo_ ## NAME ## _cptr) boost::shared_ptr<echo<T> const>;
  %template(create_echo_ ## NAME) create_echo<T>;
  %template(benchmark_## NAME) benchmark<T>;
%enddef

ECHO_WRAP( int, int )
ECHO_WRAP( str, std::string )


%{
#include <echo.hpp>
%}
