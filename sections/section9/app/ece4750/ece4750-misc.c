//========================================================================
// ece4750-misc
//========================================================================

#include "ece4750-misc.h"

//------------------------------------------------------------------------
// ece4750_seed
//------------------------------------------------------------------------

#ifdef _RISCV

int ece4750_lfsr = 0x0000cafe;

void ece4750_srand( int seed )
{
  ece4750_lfsr = 0x0000ffff & seed;
}

#endif

//------------------------------------------------------------------------
// ece4750_rand
//------------------------------------------------------------------------
// Adapted from 16-bit LFSR from wikipedia:
//
//  https://en.wikipedia.org/wiki/Linear-feedback_shift_register
//

#ifdef _RISCV

int ece4750_rand()
{
  int x = ece4750_lfsr;
  int bit = (x ^ (x >> 1) ^ (x >> 3) ^ (x >> 12)) & 0x00000001;
  ece4750_lfsr = (ece4750_lfsr >> 1) | (bit << 15);

  return ece4750_lfsr;
}

#endif

//------------------------------------------------------------------------
// ece4750_atoi
//------------------------------------------------------------------------

#ifdef _RISCV

typedef int wchar_t;

int ece4750_atoi( const char* str )
{
  // Hack! Only works because the argv strings have already been widened
  // by the simulator test harness.

  const wchar_t* wstr = (const wchar_t*) str;

  // Work from most- to least-significant digit. result*10 takes into
  // account the place value, and - L'0' subtracts the code for the
  // lowest digit to convert to an integer from 0 to 9.

  int result = 0;
  int i = 0;
  while ( wstr[i] != L'\0' ) {
    result = result*10 + wstr[i] - L'0';
    i += 1;
  }

  return result;
}

#endif

//------------------------------------------------------------------------
// dummy function
//------------------------------------------------------------------------

#ifndef _RISCV

// We always need at least something in an object file, otherwise
// the native build won't work. So we create a dummy function for native
// builds.

int ece4750_( int arg )
{
  return arg;
}

#endif

