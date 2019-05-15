#include "convertor.h"

/*
 * Reference:
 * https://fr.wikipedia.org/wiki/IEEE_754
 * https://en.wikipedia.org/wiki/Single-precision_floating-point_format
 * https://en.wikipedia.org/wiki/Double-precision_floating-point_format
 * 
 * 32 bits float:
 *   byte 3      byte 2      byte 1     byte 0
 * Seee eeee | efff ffff | ffff ffff | ffff ffff
 * 
 * 64 bits double:
 *   byte 7      byte 6     byte 5            byte 0
 * Seee eeee | eeee ffff | ffff ffff | ... | ffff ffff
 * 
 * where:
 * S: sign bit
 * e: exponent bits
 * f: fraction bits
 */
void toDouble(float value, byte outputDouble[8]) {
  byte* floatBytes = (byte*)&value;

  byte floatExponent = ((floatBytes[3] & BITS_6_0_MASK) << 1) | ((floatBytes[2] & BIT_7_MASK) >> 7);

  uint16_t doubleExponent;
  if (floatExponent == 0x00) {
    doubleExponent = 0x00;
  } else {
    doubleExponent = (int16_t)(floatExponent - FLOAT_EXPONENT_OFFSET) + DOUBLE_EXPONENT_OFFSET;
  }
  byte* doubleExponentBytes = (byte*)&doubleExponent;

  outputDouble[7] = (floatBytes[3] & BIT_7_MASK) | ((doubleExponentBytes[1] & BITS_2_0_MASK) << 4) | ((doubleExponentBytes[0] & BITS_7_4_MASK) >> 4);
  outputDouble[6] = ((doubleExponentBytes[0] & BITS_3_0_MASK) << 4) | ((floatBytes[2] & BITS_6_0_MASK) >> 3);
  outputDouble[5] = ((floatBytes[2] & BITS_2_0_MASK) << 5) | ((floatBytes[1] & BITS_7_3_MASK) >> 3);
  outputDouble[4] = ((floatBytes[1] & BITS_2_0_MASK) << 5) | ((floatBytes[0] & BITS_7_3_MASK) >> 3);
  outputDouble[3] = (floatBytes[0] & BITS_2_0_MASK) << 5;
  outputDouble[2] = 0;
  outputDouble[1] = 0;
  outputDouble[0] = 0;
}

