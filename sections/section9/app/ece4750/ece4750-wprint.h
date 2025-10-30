//========================================================================
// ece4750-wprint
//========================================================================
// A simple implementation of wprint that enables TinyRV2 applications to
// print an integer, character, or string to the terminal as well as a
// _very_ simple wprintf function.
//
// Note that using chars would require manipulating bytes, but TinyRV2
// only supports lw/sw. So we instead use wchar_t which is a "wide 4B
// character". Technically this is for unicode, but it still works fine
// with ASCII characters. This does mean that all character literals need
// to have the L prefix like this:
//
//  ece4750_wprint( L'a');
//  ece4750_wprint( L"abc" );
//  ece4750_wprintf( L"number=%d, char=%C, string=%S", 42, L'a', L"abc" );
//
// _RISCV will only be defined when cross-compiling for RISCV.
//

#ifndef ECE4750_WPRINT_H
#define ECE4750_WPRINT_H

#ifndef _RISCV
  #include <wchar.h>
#endif

//------------------------------------------------------------------------
// wprint integer
//------------------------------------------------------------------------
// Print a single integer to the terminal in decimal format.

#ifdef _RISCV

typedef int wchar_t;

inline
void ece4750_wprint_int( int i )
{
  __asm__ ( "csrw 0x7c0, %0" :: "r"(0x00030000) );
  __asm__ ( "csrw 0x7c0, %0" :: "r"(i) );
}

#else

inline
void ece4750_wprint_int( int i )
{
  wprintf( L"%d", i );
}

#endif

//------------------------------------------------------------------------
// wprint character
//------------------------------------------------------------------------
// Print a single character. As mentioned above, we must use wchar_t
// since TinyRV2 only supports lw/sw.

#ifdef _RISCV

inline
void ece4750_wprint_char( wchar_t c )
{
  __asm__ ( "csrw 0x7c0, %0" :: "r"(0x00030001) );
  __asm__ ( "csrw 0x7c0, %0" :: "r"(c) );
}

#else

inline
void ece4750_wprint_char( wchar_t c )
{
  wprintf( L"%C", c );
}

#endif

//------------------------------------------------------------------------
// wprint string
//------------------------------------------------------------------------
// Print a string. As mentioned above, we must use wchar_t since TinyRV2
// only supports lw/sw.

#ifdef _RISCV

inline
void ece4750_wprint_str( const wchar_t* p )
{
  __asm__ ( "csrw 0x7c0, %0" :: "r"(0x00030002) );
  while ( *p != 0 ) {
    __asm__ ( "csrw 0x7c0, %0" :: "r"(*p) );
    p++;
  }
  __asm__ ( "csrw 0x7c0, %0" :: "r"(*p) );
}

#else

inline
void ece4750_wprint_str( const wchar_t* str )
{
  wprintf( L"%S", str );
}

#endif

//------------------------------------------------------------------------
// wprintf
//------------------------------------------------------------------------
// A _very_ simple wprintf. Only supports three format flags:
//
//  %d : integer in decimal format
//  %C : character
//  %S : string
//

#ifdef _RISCV

void ece4750_wprintf( const wchar_t* fmt, ... );

#else

#define ece4750_wprintf wprintf

#endif

//------------------------------------------------------------------------
// flush
//------------------------------------------------------------------------
// When combining our simulators with the tee program so we can display
// and log the output, sometimes the output shows up only when the
// simulation is completely done. We need to flush the output buffer
// explicitly using the flush function.

#ifdef _RISCV

inline
void ece4750_flush()
{
  __asm__ ( "csrw 0x7c0, %0" :: "r"(0x00030003) );
}

#else

inline
void ece4750_flush()
{ }

#endif

#endif /* ECE4750_WPRINT_H */

