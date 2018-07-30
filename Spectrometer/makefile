
CC=g++
CFLAGS=-Wall -Wunused -DLINUX -fPIC -I$(JDK_HOME)/include -I$(JDK_HOME)/include/linux -I$(OMNIDRIVER_HOME)/include
GFLAGS=-g

all: make_it.so 

make_it.so:
	$(CC) -o make_it.so -shared -lcommon -lOmniDriver -L$(OMNIDRIVER_HOME)/_jvm/lib/amd64/server -ljvm  -L$(OMNIDRIVER_HOME)/OOI_HOME
	rm *.o	



clean:
	rm *.so
