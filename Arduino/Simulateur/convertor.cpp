#include "convertor.h"

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

