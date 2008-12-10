CXX = g++
CXXFLAGS = -g -O2 -I/usr/local/include/boost-1_35 -I/usr/include/python2.5 -I. -Wall -Wno-sign-compare -Wno-unknown-pragmas -Wno-format -D_GNU_SOURCE

#yoyo_wrap.cxx: yoyo.i yoyo.cxx
#	swig -Wall -c++ -python -module pyyoyo yoyo.i
_pyyoyo.so: yoyo_wrap.cxx
	${CXX} $< ${CXXFLAGS} -shared -fPIC -L. -lyoyo -Wl,-soname,$@ -o $@
libyoyo.so : yoyo.cxx
	${CXX} $< ${CXXFLAGS} -shared -fPIC -L. -Wl,-soname,$@ -o $@
clean:
	rm -f libyoyo.so _pyyoyo.so
