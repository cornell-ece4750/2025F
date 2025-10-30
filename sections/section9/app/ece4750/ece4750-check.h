//========================================================================
// ece4750-check
//========================================================================
// Very simple unit testing framework.
//
// _RISCV will only be defined when cross-compiling for RISCV.

#ifndef ECE4750_CHECK_H
#define ECE4750_CHECK_H

#include "ece4750-wprint.h"

//------------------------------------------------------------------------
// Helper Macros
//------------------------------------------------------------------------

// Colorize text

#define ECE4750_RED(x)    L"\033[31m" x L"\033[0m"
#define ECE4750_GREEN(x)  L"\033[32m" x L"\033[0m"
#define ECE4750_YELLOW(x) L"\033[33m" x L"\033[0m"

// Convert strings from ASCII to wide strings

#define ECE4750_A2W_(x)          L ## x
#define ECE4750_A2W(x)           ECE4750_A2W_(x)
#define ECE4750_STRINGIFY_(x)    #x
#define ECE4750_STRINGIFY(x)     ECE4750_STRINGIFY_(x)
#define ECE4750_STRINGIFY_A2W(x) ECE4750_A2W(ECE4750_STRINGIFY(x))

#define ECE4750_WFILE ECE4750_A2W(__FILE__)
#define ECE4750_WLINE ECE4750_STRINGIFY_A2W(__LINE__))

//------------------------------------------------------------------------
// Global Variables
//------------------------------------------------------------------------

// Which test case to run

extern int __n;

// Status of test file. Failed check sets this variable to 1.

extern int ece4750_check_status;

// Temporary variables to save the condition so that we don't evaluate
// the given expressions multiple times.

extern int ece4750_check_expr0;
extern int ece4750_check_expr1;

//------------------------------------------------------------------------
// ECE4750_CHECK
//------------------------------------------------------------------------
// Test case header

#define ECE4750_CHECK( ... )                                            \
  do {                                                                  \
    ece4750_wprintf( L"\n" ECE4750_WFILE L"::" __VA_ARGS__ L" " );      \
    if ( __n < 0 ) {                                                    \
      return;                                                           \
    }                                                                   \
  } while ( 0 )

//------------------------------------------------------------------------
// ECE4750_CHECK_FAIL
//------------------------------------------------------------------------
// Unconditionally fail a test case.

#define ECE4750_CHECK_FAIL( ... )                                       \
  do {                                                                  \
                                                                        \
    ece4750_wprint_str( ECE4750_RED(L"FAILED") );                       \
    if ( __n > 0 ) {                                                    \
      ece4750_wprintf( L"\n - [ " ECE4750_RED(L"FAILED") L" ] %S:%d: %S", \
        ECE4750_WFILE, __LINE__ );                                      \
      ece4750_wprintf( __VA_ARGS__ );                                   \
    }                                                                   \
    ece4750_flush();                                                    \
    ece4750_check_status = 1;                                           \
    return;                                                             \
                                                                        \
  } while ( 0 )

//------------------------------------------------------------------------
// ECE4750_CHECK_TRUE
//------------------------------------------------------------------------

#define ECE4750_CHECK_TRUE( expr_ )                                     \
  do {                                                                  \
    ece4750_check_expr0 = (expr_);                                      \
                                                                        \
    if ( !ece4750_check_expr0 ) {                                       \
      if ( __n > 0 ) {                                                  \
        ece4750_wprintf( L"\n - [ " ECE4750_RED(L"FAILED") L" ] %S:%d: %S (%d)", \
          ECE4750_WFILE, __LINE__,                                      \
          ECE4750_STRINGIFY_A2W(expr_), ece4750_check_expr0 );          \
      }                                                                 \
      else                                                              \
        ece4750_wprint_str( ECE4750_RED(L"FAILED") );                   \
      ece4750_flush();                                                  \
      ece4750_check_status = 1;                                         \
      return;                                                           \
    }                                                                   \
    else if ( __n > 0 ) {                                               \
      ece4750_wprintf( L"\n - [ " ECE4750_GREEN(L"passed") L" ] %S:%d: %S (%d)",\
        ECE4750_WFILE, __LINE__,                                        \
        ECE4750_STRINGIFY_A2W(expr_), ece4750_check_expr0 );            \
      ece4750_flush();                                                  \
    }                                                                   \
    else {                                                              \
      ece4750_wprint_str( ECE4750_GREEN(L".") );                        \
      ece4750_flush();                                                  \
    }                                                                   \
                                                                        \
  } while ( 0 )

//------------------------------------------------------------------------
// ECE4750_CHECK_FALSE
//------------------------------------------------------------------------

#define ECE4750_CHECK_FALSE( expr_ )                                    \
  do {                                                                  \
    ece4750_check_expr0 = (expr_);                                      \
                                                                        \
    if ( ece4750_check_expr0 ) {                                        \
      if ( __n > 0 ) {                                                  \
        ece4750_wprintf( L"\n - [ " ECE4750_RED(L"FAILED") L" ] %S:%d: %S (%d)", \
          ECE4750_WFILE, __LINE__,                                      \
          ECE4750_STRINGIFY_A2W(expr_), ece4750_check_expr0 );          \
      }                                                                 \
      else                                                              \
        ece4750_wprint_str( ECE4750_RED(L"FAILED") );                   \
      ece4750_flush();                                                  \
      ece4750_check_status = 1;                                         \
      return;                                                           \
    }                                                                   \
    else if ( __n > 0 ) {                                               \
      ece4750_wprintf( L"\n - [ " ECE4750_GREEN(L"passed") L" ] %S:%d: %S (%d)",\
        ECE4750_WFILE, __LINE__,                                        \
        ECE4750_STRINGIFY_A2W(expr_), ece4750_check_expr0 );            \
      ece4750_flush();                                                  \
    }                                                                   \
    else {                                                              \
      ece4750_wprint_str( ECE4750_GREEN(L".") );                        \
      ece4750_flush();                                                  \
    }                                                                   \
                                                                        \
  } while ( 0 )

//------------------------------------------------------------------------
// ECE4750_CHECK_INT_EQ
//------------------------------------------------------------------------
// Check to see if two expressions are equal

#define ECE4750_CHECK_INT_EQ( expr0_, expr1_ )                          \
  do {                                                                  \
    ece4750_check_expr0 = (expr0_);                                     \
    ece4750_check_expr1 = (expr1_);                                     \
                                                                        \
    if ( ece4750_check_expr0 != ece4750_check_expr1 ) {                 \
      if ( __n > 0 ) {                                                  \
        ece4750_wprintf( L"\n - [ " ECE4750_RED(L"FAILED") L" ] %S:%d: %S != %S (%d != %d)", \
          ECE4750_WFILE, __LINE__,                                      \
          ECE4750_STRINGIFY_A2W(expr0_), ECE4750_STRINGIFY_A2W(expr1_), \
          ece4750_check_expr0, ece4750_check_expr1 );                   \
      }                                                                 \
      else                                                              \
        ece4750_wprint_str( ECE4750_RED(L"FAILED") );                   \
      ece4750_flush();                                                  \
      ece4750_check_status = 1;                                         \
      return;                                                           \
    }                                                                   \
    else if ( __n > 0 ) {                                               \
      ece4750_wprintf( L"\n - [ " ECE4750_GREEN(L"passed") L" ] %S:%d: %S == %S (%d == %d)", \
        ECE4750_WFILE, __LINE__,                                        \
        ECE4750_STRINGIFY_A2W(expr0_), ECE4750_STRINGIFY_A2W(expr1_),   \
        ece4750_check_expr0, ece4750_check_expr1 );                     \
      ece4750_flush();                                                  \
    }                                                                   \
    else {                                                              \
      ece4750_wprint_str( ECE4750_GREEN(L".") );                        \
      ece4750_flush();                                                  \
    }                                                                   \
                                                                        \
  } while ( 0 )

//------------------------------------------------------------------------
// ECE4750_CHECK_NOTE
//------------------------------------------------------------------------

#define ECE4750_CHECK_NOTE( ... )                                       \
  do {                                                                  \
                                                                        \
    if ( __n > 0 ) {                                                    \
      ece4750_wprintf( L"\n - [ " ECE4750_YELLOW(L"-note-") L" ] %S:%d: ", \
        ECE4750_WFILE, __LINE__ );                                      \
      ece4750_wprintf( __VA_ARGS__ );                                   \
      ece4750_flush();                                                  \
    }                                                                   \
                                                                        \
  } while ( 0 )

#endif /* ECE4750_CHECK_H */

