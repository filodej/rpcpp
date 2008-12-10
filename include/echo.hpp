#ifndef __ECHO_INCLUDED_HPP__
#define __ECHO_INCLUDED_HPP__
 
#include <boost/noncopyable.hpp>
#include <boost/shared_ptr.hpp>
#include <string>

template <class T>
class echo : boost::noncopyable
{
 public:
    virtual T call( T const& value ) const = 0;
    virtual ~echo() = 0;
 private:
};

typedef boost::shared_ptr<echo<std::string> const> str_echo_cptr;
typedef boost::shared_ptr<echo<int> const>         int_echo_cptr;

//typedef boost::intrusive_ptr<echo const> echo_cptr;

// http://osdir.com/ml/programming.swig/2004-09/msg00097.html

template<class T>
boost::shared_ptr<echo<T> const> new_echo();

template <class T>
double benchmark( echo<T> const& e, T const& value, int walk_count );

#endif //__ECHO_INCLUDED_HPP__
