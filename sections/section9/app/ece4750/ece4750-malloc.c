//========================================================================
// ece4750-malloc
//========================================================================

#include "ece4750-malloc.h"

//------------------------------------------------------------------------
// ece4750_malloc
//------------------------------------------------------------------------

#ifdef _RISCV

void* ece4750_malloc( int mem_size )
{
  extern unsigned char _end; // defined in linker script
  static unsigned char* heap_end;
  unsigned char* prev_heap_end;

  if ( heap_end == 0 )
    heap_end = &_end;

  prev_heap_end = heap_end;
  heap_end += mem_size;
  return prev_heap_end;
}

#else

// We always need at least something in an object file, otherwise
// the native build won't work. So we create a dummy function for native
// builds.

int ece4750_( int arg )
{
  return arg;
}

#endif


