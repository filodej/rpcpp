%include "./shared_ptr.i"
%include "std_string.i"
%include <echo.hpp> 

%module pyecho

%module(directors="1") pyecho
#%feature("director") echo;

%define ECHO_WRAP( NAME, T ) 
  %template(echo_ ## NAME) echo<T>;
  %template(echo_ ## NAME ## _cptr) boost::shared_ptr<echo<T> const>;
  %template(new_echo_ ## NAME) new_echo<T>;
  %template(benchmark_## NAME) benchmark<T>;
%enddef

ECHO_WRAP( int, int )
ECHO_WRAP( str, std::string )


%{
#include <echo.hpp>
%}
