import sys
import os.path
sys.path.append( os.path.abspath( './release') )
import getopt
import time
import rpcppy
import rpyc
import rpyc.utils.server

def py_synch_benchmark( echo, val, count ):
    """Python implemented benchmark for synchronous calls"""
    start = time.clock()
    for i in xrange( count ):
        assert echo.call( val ) == val
    return time.clock() - start

def py_asynch_benchmark( echo, val, count ):
    """Python implemented benchmark for asynchronous RPyC calls"""
    def check_val( proxy ):
        if proxy.ready:
            assert proxy.value == val
            return False
        else:
            return True
    start = time.clock()
    proxies = [ rpyc.async( echo.call )( val ) for i in xrange( count ) ]
    while proxies:
        proxies = filter( check_val, proxies )
        if proxies:
            print len(proxies)
    return time.clock() - start

class adapter_factory( object ):
    """Factory adapter (swig delegate cannot be directly marshalled by RPyC)
    it is necessary to create an adapter - python wrapper - delegating the calls"""
    def __init__( self, factory ):
        self.factory = factory

    def create_echo_int( self ):
        return adapter_factory._wrap( rpcppy.echo_int )( self.factory.create_echo_int() )

    def create_echo_str( self ):
        return adapter_factory._wrap( rpcppy.echo_str )( self.factory.create_echo_str() )

    @staticmethod
    def _wrap( base ):
        class _adapter( base ):
            def __init__( self, next ):
                base.__init__( self )
                self._next = next
            def call( self, val ):
                return self._next.call( val )
        return _adapter

class remote_factory( object ):
    """Factory for remote (RPyC calls)"""
    def __init__( self, host, port ):
        self.conn = rpyc.classic.connect( host, port )
        mod = self.conn.modules["rpcppy"]
        self.create_echo_int = mod.create_echo_int
        self.create_echo_str = mod.create_echo_str

def advanced_test( factory, fn_bench_int, fn_bench_str, treshold, verbose ):
    """Each test consists of following tests:
    - integer sub-test
    - string sub-test for several string lengths (8, 16, ... 128)
    """
    def deref( ptr ):
        try:
            return ptr.__deref__()
        except:
            return ptr
    
    def do_benchmark( echo, fnbench, val ):
        i = 10
        while 2**(i+1) <= sys.maxint:
            i += 1
            t = fnbench( deref(echo), val, 2**i )
            if t > treshold:
                break
        print '%f calls/sec.' % ( float(2**i)/t )
        if verbose:
            print '\t\t(%d calls in %f seconds)' % ( 2**i, t )

    print '\tcall(int)\t\t',
    do_benchmark( factory.create_echo_int(), fn_bench_int, 42 )
    for i in range( 3, 8 ):
        print '\tcall(str[len=%d])\t' % ( 2**i ),
        do_benchmark( factory.create_echo_str(), fn_bench_str, 2**i * 'X' )

def parse_options():
    """\
    Usage:
        python test.py <options>
    Options:
        -h, --help     ... prints this message
        -m, --mode     ... mode (one of 'local', 'client', server)
        -H, --hostnames... comma separated list of servers' hostnames (default 'localhost')
        -p, --port     ... rpyc port (default 18861)
        -t, --treshold ... benchmark treshold (default 5.0 sec.)
        -v, --verbose  ... detailed test results printed (disabled by default)
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hH:m:p:t:v", ["help", "hostnames=", "mode=", "port=", "treshold=", "verbose"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        print parse_options.__doc__
        sys.exit(2)
    hostnames = ''
    port = 18861
    mode = 'local'
    treshold = 5.0
    verbose = False
    for o, a in opts:
        if o in ("-h", "--help"):
            print parse_options.__doc__
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
                print parse_options.__doc__
                sys.exit(2)
            mode = a
        else:
            assert False, "unhandled option"
    if mode == 'client' and not hostnames:
        hostnames = 'localhost'
    elif mode == 'server' and hostnames:
        print 'cannot specify hostnames in server mode'
        sys.exit(2)
    return mode, hostnames, port, treshold, verbose
    
def build_test_suite( hostnames, port ):
    """Builds whole test suite (a set of individual tests)"""
    # in-process tests
    suite = [ 
        ( 'in-process calls [c++ -> c++]:', rpcppy, rpcppy.benchmark_int, rpcppy.benchmark_str ), 
        ( 'in-process calls [python -> c++]:', rpcppy, py_synch_benchmark, py_synch_benchmark ), 
        ( 'in-process calls [c++ -> python -> c++]:', adapter_factory( rpcppy ), rpcppy.benchmark_int, rpcppy.benchmark_str ) ]
    if hostnames:
        # out-of-process tests for each specified server
        for hostname in hostnames.split(','):
            suite.append( (
                'out-of-process "%s" synch calls [c++ -> python -> RPC -> python -> c++]:' % hostname,
                adapter_factory( remote_factory( hostname, port ) ),
                rpcppy.benchmark_int,
                rpcppy.benchmark_str ) )
            suite.append( (
                'out-of-process "%s" synch calls [python -> RPC -> python -> c++]:' % hostname,
                remote_factory( hostname, port ),
                py_synch_benchmark,
                py_synch_benchmark ) )
            suite.append( (
                'out-of-process "%s" asynch calls [python -> RPC -> python -> c++]:' % hostname,
                remote_factory( hostname, port ),
                py_asynch_benchmark,
                py_asynch_benchmark ) )
    return suite

def run_test_suite( suite, treshold = 5.0, verbose = False ):
    """Runs all given tests"""
    for desc, f, fn_bench_int, fn_bench_str in suite:
        print desc
        advanced_test( f, fn_bench_int, fn_bench_str, treshold, verbose )

def test_server( port ):
    """Launches test server"""
    ts = rpyc.utils.server.ThreadedServer( rpyc.SlaveService, port = port )
    ts.start()
    
if __name__ == '__main__':
    mode, hostnames, port, treshold, verbose = parse_options()
    if mode == 'server':
        assert not hostnames
        test_server( port )
    else:
        assert mode != 'client' or hostnames
        run_test_suite( build_test_suite( hostnames, port ), treshold, verbose )
