CC=gcc
CFLAGS=-shared -fPIC
LIBS=-ldl

sandbox.so: sandbox.c
	$(CC) $(CFLAGS) -o sandbox.so sandbox.c $(LIBS)

clean:
	rm *.so
