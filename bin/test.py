import sys
import getopt
import new
import rpcppy
import rpyc
import rpyc.utils.server

def deref( ptr ):
    try:
	return ptr.__deref__()
    except:
	return ptr

def _make_echo_adapter( base ):
    class _adapter( base ):
        def __init__( self, next ):
            base.__init__( self )
	    self._next = next
	def call( self, val ):
	    return self._next.call( val )
    return _adapter

class adapter_factory( object ):
    echo_int = _make_echo_adapter( rpcppy.echo_int )
    echo_str = _make_echo_adapter( rpcppy.echo_str )
    
    def __init__( self, factory = rpcppy ):
	self.factory = factory
	
    def create_echo_int( self ):
	return adapter_factory.echo_int( self.factory.create_echo_int() )
	
    def create_echo_str( self ):
	return adapter_factory.echo_str( self.factory.create_echo_str() )

class remote_factory( object ):
    def __init__( self, host, port ):
	self.conn = rpyc.classic.connect( host, port )
	mod = self.conn.modules["rpcppy"]
	self.create_echo_int = mod.create_echo_int
	self.create_echo_str = mod.create_echo_str
	
def simple_test( factory = rpcppy ):
    ei = factory.create_echo_int()
    assert 42 == ei.call( 42 )
    
    es = factory.create_echo_str()
    assert '42' == es.call( '42' )

def advanced_test( factory = rpcppy, treshold = 5.0, verbose = False ):
    def benchmark( echo, fn, val ):
	i = 10
	while True:
	    i += 1
	    t = fn( deref(echo), val, 2**i )
	    if t > treshold:
		break
	print '%f calls/sec.' % ( float(2**i)/t )
	if verbose:
    	    print '\t\t(%d calls in %f seconds)' % ( 2**i, t )

    print '\tcall(int)\t\t',
    benchmark( factory.create_echo_int(), rpcppy.benchmark_int, 42 )
    for i in range( 3, 8 ):
        print '\tcall(str[len=%d])\t' % ( 2**i ),
	benchmark( factory.create_echo_str(), rpcppy.benchmark_str, 2**i * 'X' )
    
g_usage = """\
usage:
    python test.py <options>
options:
    -h, --help     ... prints this message
    -m, --mode     ... mode (one of 'local', 'client', server)
    -H, --hostnames... comma separated list of servers' hostnames (default 'localhost')
    -p, --port     ... rpyc port (default 18861)
    -t, --treshold ... benchmark treshold (default 5.0 sec.)
    -v, --verbose  ... detailed test results printed (disabled by default)
"""

def parse_options():
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hH:m:p:t:v", ["help", "hostnames=", "mode=", "port=", "treshold=", "verbose"])
    except getopt.GetoptError, err:
	print str(err) # will print something like "option -a not recognized"
	print g_usage
	sys.exit(2)
    hostnames = 'localhost'
    port = 18861
    mode = 'local'
    treshold = 5.0
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
	    print g_usage
	    sys.exit()
	elif o in ("-p", "--port"):
	    port = a
	elif o in ("-t", "--treshold"):
	    treshold = float(a)
	elif o in ("-v", "--verbose"):
	    verbose = True
	elif o in ("-H", "--hostnames"):
	    hostnames = a
	elif o in ("-m", "--mode"):
	    if a not in ('local', 'client', 'server'):
		print 'unknown mode:', a
		print g_usage
		sys.exit(2)
	    mode = a
	else:
	    assert False, "unhandled option"
    return mode, hostnames, port, treshold, verbose
    
    
if __name__ == '__main__':
    mode, hostnames, port, treshold, verbose = parse_options()
    if mode == 'server':
        ts = rpyc.utils.server.ThreadedServer( rpyc.SlaveService, port = port )
	ts.start()
    else:
	factories = [ 
	    ( 'in-process calls [c++ -> c++]:', rpcppy ), 
	    ( 'in-process calls [c++ -> python -> c++]:', adapter_factory() ) ]
	if mode == 'client':
	    for hostname in hostnames.split(','):
    		factories.append( ( 'out-of-process localhost calls [c++ -> python -> RPC -> python -> c++]:', adapter_factory( remote_factory( hostname, port ) ) ) )
	for desc, f in factories:
	    print desc
	    simple_test( f )
	    advanced_test( f, treshold, verbose )
