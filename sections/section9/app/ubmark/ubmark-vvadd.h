//========================================================================
// ubmark-vvadd
//========================================================================
// This microbenchmark performs elementwise addition across two input
// arrays and stores the result in the destination array.

#ifndef UBMARK_VVADD_H
#define UBMARK_VVADD_H

#include "ece4750.h"

void ubmark_vvadd( int* dest, int* src0, int* src1, int size );

#endif /* UBMARK_VVADD_H */

