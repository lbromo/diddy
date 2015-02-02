CC = g++
EV3_LIB = ../ev3dev-lang/cpp/

all: ev3dev sensor_test

ev3dev: ev3dev.o
	-@(MAKE) -C EV3_LIB clean all

sensor_test: ev3dev.o sensor_test.o
	CC main.cpp -I${EV3_LIB}
