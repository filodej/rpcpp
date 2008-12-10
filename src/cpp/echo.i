%include "./shared_ptr.i"
%include "./yoyo.hpp" 

%define YOYO_WRAP( NAME, T ) 
  %template(yoyo_ ## NAME) yoyo<T>;
  %template(yoyo_ ## NAME ## _cptr) boost::shared_ptr<yoyo<T> const>;
  %template(create_yoyo_ ## NAME) create_yoyo<T>;
  %template(benchmark_## NAME) benchmark<T>;
%enddef

YOYO_WRAP( int, int )
YOYO_WRAP( str, std::string )


%{
#include "./yoyo.hpp"
%}
