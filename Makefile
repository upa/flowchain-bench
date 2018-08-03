CC = gcc
INCLUDE := 
LDFLAGS := -lpthread
CFLAGS := -g -Wall $(INCLUDE)

PROGNAME = fc

all: $(PROGNAME)

.c.o:
	$(CC) $< -o $@

clean:
	rm -rf *.o
	rm -rf $(PROGNAME)

