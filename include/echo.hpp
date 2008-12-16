#ifndef __ECHO_INCLUDED_HPP__
#define __ECHO_INCLUDED_HPP__
 
#include <boost/noncopyable.hpp>

template <class T>
class echo : public boost::noncopyable
{
 public:
    virtual T call( T const& value ) const = 0;
    virtual ~echo() {};
};

#endif //__ECHO_INCLUDED_HPP__
