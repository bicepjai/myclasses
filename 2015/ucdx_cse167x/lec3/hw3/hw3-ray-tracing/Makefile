CC = g++

CFLAGS 		= 	-g -DGL_GLEXT_PROTOTYPES -DOSX -Wno-deprecated-register -Wno-deprecated-declarations -Wno-shift-op-parentheses 
INCFLAGS 	= 	-I./glm-0.9.2.7 -I/usr/X11/include -I./include/ -I/opt/local/include/
LDFLAGS 	= 	-L./osxlib/ -L/opt/local/lib -lm -lstdc++ -lfreeimage -lboost_thread-mt -lboost_system-mt

RM = /bin/rm -f

all: ray-tracing

ray-tracing: main.o Transform.o readfile.o RayTracer.o variables.h readfile.h RayTracer.h Transform.h
	$(CC) $(CFLAGS) -o ray-tracing main.o Transform.o readfile.o RayTracer.o $(INCFLAGS) $(LDFLAGS) 
main.o: main.cpp variables.h readfile.h RayTracer.h Transform.h
	$(CC) $(CFLAGS) $(INCFLAGS) -c main.cpp
readfile.o: readfile.cpp variables.h readfile.h RayTracer.h Transform.h
	$(CC) $(CFLAGS) $(INCFLAGS) -c readfile.cpp	
Transform.o: Transform.cpp Transform.h variables.h
	$(CC) $(CFLAGS) $(INCFLAGS) -c Transform.cpp  
RayTracer.o: RayTracer.cpp variables.h RayTracer.h
	$(CC) $(CFLAGS) $(INCFLAGS) -c RayTracer.cpp	

clean: 
	$(RM) *.o ray-tracing *.png


 
