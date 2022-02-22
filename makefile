BUILDDIR=build
CXX=g++
CXXFLAGS= -std=c++20 -Wall -Wextra -pedantic
OUTPUTFILE=lisp
SOURCES :=$(patsubst %.cpp,%.o,$(wildcard src/*.cpp))

# use clang instead of apple clang on macos
UNAME := $(shell uname)
ifeq ($(UNAME),Darwin)
	CXX=clang++
endif

all: build

build: $(SOURCES)
	mkdir -p $(BUILDDIR)
	$(CXX) $(SOURCES) $(CXXFLAGS) -o $(BUILDDIR)/$(OUTPUTFILE)

debug: $(SOURCES)
	mkdir -p $(BUILDDIR)
	$(CXX) $(SOURCES) $(CXXFLAGS) -g -o $(BUILDDIR)/$(OUTPUTFILE)

run:
	./$(BUILDDIR)/$(OUTPUTFILE)

format:
	clang-format -i $(wildcard src/*.cpp)

clean:
	rm $(wildcard src/*.o)
	rm $(BUILDDIR)/$(OUTPUTFILE)