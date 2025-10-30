//========================================================================
// ubmark-vvadd
//========================================================================

#include "ubmark-vvadd.h"

void ubmark_vvadd( int* dest, int* src0, int* src1, int size )
{
  for ( int i = 0; i < size; i++ )
    dest[i] = src0[i] + src1[i];
}

