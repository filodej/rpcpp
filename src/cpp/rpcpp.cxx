#include <rpcpp.hpp>
#include <boost/timer.hpp>
#include <stdexcept>

// echo interface implementation
template <class T>
class echo_impl : public echo<T>
{
public: // echo interface
  T call( T const& value ) const { return value; }
  echo_impl() {}
};

// http://osdir.com/ml/programming.swig/2004-09/msg00097.html

// echo factory function
template <class T>
boost::shared_ptr<echo<T> const> create_echo()
{
  return boost::shared_ptr<echo<T> const>( new echo_impl<T> );
}

// echo benchmark
template<class T>
double benchmark( echo<T> const& e, T const& value, int walk_count )
{
  boost::timer t;
  for ( int i=0; i<walk_count; ++i )
  {
    if ( value != e.call( value ) )
      throw std::runtime_error( "echo corrupted" );
  }
  return t.elapsed();
}

// explicit template instantiations
template RPCPP_API boost::shared_ptr<echo<int> const> create_echo<int>();
template RPCPP_API double benchmark( echo<int> const&, int const& , int );

template RPCPP_API boost::shared_ptr<echo<std::string> const> create_echo<std::string>();
template RPCPP_API double benchmark( echo<std::string> const&, std::string const&, int );


