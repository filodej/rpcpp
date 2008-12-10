import sys
import getopt
import new
import pyecho
import rpyc
import rpyc.utils.server

def deref( ptr ):
    try:
	return ptr.__deref__()
    except:
	return ptr

class adapter_factory:
    def __init__( self, factory = pyecho ):
	self.factory = factory
	
    def create_echo_int( self ):
	class adapter( pyecho.echo_int ):
	    def __init__( self, next ):
		pyecho.echo_int.__init__( self )
		self._next = next
	    def __getattribute__( self, name ):
		if name[0] == '_':
		    return pyecho.echo_int.__getattribute__(self, name) 
		return getattr( self._next, name )		
	return adapter( self.factory.create_echo_int() )
	
    def create_echo_str( self ):
	class adapter( pyecho.echo_str ):
	    def __init__( self, next ):
		pyecho.echo_str.__init__( self )
		self._next = next
	    def __getattribute__( self, name ):
		if name[0] == '_':
		    return pyecho.echo_str.__getattribute__(self, name) 
		return getattr( self._next, name )		
	return adapter( self.factory.create_echo_str() )

class remote_factory:
    def __init__( self, host, port ):
	self.conn = rpyc.classic.connect( host, port )
	#self.create_echo_int = new.instancemethod( self.conn.modules["pyecho"].create_echo_int, self, self.__class__)
	#self.create_echo_str = new.instancemethod( self.conn.modules["pyecho"].create_echo_str, self, self.__class__)

    def create_echo_int( self ): 
	return self.conn.modules["pyecho"].create_echo_int()
	
    def create_echo_str( self ): 
	return self.conn.modules["pyecho"].create_echo_str()
	
def simple_test( factory = pyecho ):
    ei = factory.create_echo_int()
    assert 42 == ei.call( 42 )
    
    es = factory.create_echo_str()
    assert '42' == es.call( '42' )

def advanced_test( factory = pyecho, treshold = 5.0 ):
    def benchmark( echo, fn, val ):
	i = 10
	while True:
	    i += 1
	    t = fn( deref(echo), val, 2**i )
	    if t > treshold:
		break
	print '\t\t%f calls/sec.\n\t\t\t(%d calls in %f seconds)' % ( float(2**i)/t, 2**i, t )

    print '\tcall(int)'
    benchmark( factory.create_echo_int(), pyecho.benchmark_int, 42 )
    print '\tcall(str[len=42])'
    benchmark( factory.create_echo_str(), pyecho.benchmark_str, 42 * 'X' )
    
g_usage = """\
usage:
    python test.py <options>
options:
    -h, --help     ... prints this message
    -m, --mode     ... mode (one of 'local', 'client', server)
    -H, --hostname ... rpyc server hostname (default 'localhost')
    -p, --port     ... rpyc port (default 18861)
"""

def parse_options():
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hH:m:p:", ["help", "hostname=", "mode=", "port="])
    except getopt.GetoptError, err:
	print str(err) # will print something like "option -a not recognized"
	print g_usage
	sys.exit(2)
    hostname = "localhost"
    port = 18861
    mode = 'local'
    for o, a in opts:
        if o in ("-h", "--help"):
	    print g_usage
	    sys.exit()
	elif o in ("-p", "--port"):
	    port = a
	elif o in ("-h", "--hostname"):
	    hostname = a
	elif o in ("-m", "--mode"):
	    if a not in ('local', 'client', 'server'):
		print 'unknown mode:', a
		print g_usage
		sys.exit(2)
	    mode = a
	else:
	    assert False, "unhandled option"
    return mode, hostname, port
    
    
if __name__ == '__main__':
    mode, hostname, port = parse_options()
    if mode == 'server':
        ts = rpyc.utils.server.ThreadedServer( rpyc.SlaveService, port = port )
	ts.start()
    else:
	factories = [ 
	    ( 'in-process calls [c++ -> c++]:', pyecho ), 
	    ( 'in-process calls [c++ -> python -> c++]:', adapter_factory() ) ]
	if mode == 'client':
    	    factories.append( ( 'out-of-process localhost calls [c++ -> python -> RPC -> python -> c++]:', adapter_factory( remote_factory( hostname, port ) ) ) )
	for desc, f in factories:
	    print desc
	    simple_test( f )
	    advanced_test( f )
