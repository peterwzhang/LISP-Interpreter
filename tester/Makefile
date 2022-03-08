####################################################################### 
#      Makefile for use with C++ kamin interpreters
# #######################################################################
CC = gcc
CXX = g++
CFLAGS=
LIBS = -lg++

#     The following two rules add automaticity to c++ suffixes
.SUFFIXES: .cc .C
.cc.o:
	$(CXX) $(CFLAGS) -c  $<
.C.o:
	$(CXX) $(CFLAGS) -c $<
#######################################################################
ifiles = main.o reader.o expression.o list.o function.o environment.o lisp.o

kamincpp: $(ifiles) chap2.o
	g++ -o kamincpp $(ifiles) chap2.o