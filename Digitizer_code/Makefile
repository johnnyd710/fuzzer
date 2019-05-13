all: acquire_to_disk bin2txt split-channels

CFLAGS=-O2 -Wall
LFLAGS=-lATSApi

acquire_to_disk: acquire_to_disk.o
	c++ $(CFLAGS) -o acquire_to_disk acquire_to_disk.o $(LFLAGS)

acquire_to_disk.o: acquire_to_disk.c++
	c++ $(CFLAGS) -c acquire_to_disk.c++

bin2txt: bin2txt.c++
	c++ $(CFLAGS) -o bin2txt bin2txt.c++

split-channels: split-channels.c++
	c++ $(CFLAGS) -o split-channels split-channels.c++

clean:
	rm -f acquire_to_disk acquire_to_disk.o bin2txt split-channels

