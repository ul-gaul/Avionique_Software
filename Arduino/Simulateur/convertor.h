#ifndef _convertor_h
#define _convertor_h

#include "Arduino.h"

#define FLOAT_EXPONENT_OFFSET 127
#define DOUBLE_EXPONENT_OFFSET 1023

#define BIT_7_MASK 0b10000000
#define BITS_7_4_MASK 0b11110000
#define BITS_3_0_MASK 0b00001111
#define BITS_6_0_MASK 0b01111111
#define BITS_2_0_MASK 0b00000111
#define BITS_7_3_MASK 0b11111000

/*
 * Convert a 32 bits single precision floating point number into a 64 bits double precision floating point number.
 * The bytes are in little-endian format.
 */
void toDouble(float value, byte outputDouble[8]);

#endif
