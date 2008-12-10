namespace boost
{
template<class T> class shared_ptr
{
public:
    T * operator-> () 
    {
        return px;
    }

    T * get () 
    {
        return px;
    }    
};
} // namespace boost

