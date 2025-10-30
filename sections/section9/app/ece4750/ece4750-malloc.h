//========================================================================
// ece4750-malloc
//========================================================================
// Very, very simple bump pointer malloc. Very easy to run out of memory.
// Do not abuse this!
//
// _RISCV will only be defined when cross-compiling for RISCV.

#ifndef ECE4750_MALLOC_H
#define ECE4750_MALLOC_H

#include "ece4750-misc.h"

#ifdef _RISCV
#define NULL 0
#endif

//------------------------------------------------------------------------
// ece4750_malloc
//------------------------------------------------------------------------

#ifdef _RISCV

void* ece4750_malloc( int mem_size );

#else

inline
void* ece4750_malloc( int mem_size )
{
  return malloc( (size_t) mem_size );
}

#endif

//------------------------------------------------------------------------
// ece4750_free
//------------------------------------------------------------------------

#ifdef _RISCV

inline
void ece4750_free( void* ptr )
{
  // don't do anything on RISCV .. can easily run out of memory!
  ECE4750_UNUSED_PTR( ptr );
}

#else

inline
void ece4750_free( void* ptr )
{
  free( ptr );
}

#endif

#endif /* ECE4750_MISC_H */


