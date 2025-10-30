//========================================================================
// Unit tests for ubmark accumulate
//========================================================================

#include "ece4750.h"
#include "ubmark-accumulate.h"
#include "ubmark-accumulate.dat"

//------------------------------------------------------------------------
// Test positive inputs
//------------------------------------------------------------------------

void test_case_1_pos()
{
  ECE4750_CHECK( L"test_case_1_pos" );

  int src[] = { 1,  2,  3,  4 };

  int sum = ubmark_accumulate( src, 4 );

  ECE4750_CHECK_INT_EQ( sum, 10 );
}

//------------------------------------------------------------------------
// Test negative inputs
//------------------------------------------------------------------------

void test_case_2_neg()
{
  ECE4750_CHECK( L"test_case_2_neg" );

  int src[] = { -1, -2, 3,  4 };

  int sum = ubmark_accumulate( src, 4 );

  ECE4750_CHECK_INT_EQ( sum, 4 );
}

//------------------------------------------------------------------------
// Test size 9
//------------------------------------------------------------------------

void test_case_3_size9()
{
  ECE4750_CHECK( L"test_case_3_size9" );

  int src[] = { 1, 5, 2, 8, 3, 5, 1, 0, 3 };

  int sum = ubmark_accumulate( src, 9 );

  ECE4750_CHECK_INT_EQ( sum, 28 );
}

//------------------------------------------------------------------------
// Test size 16
//------------------------------------------------------------------------

void test_case_4_size16()
{
  ECE4750_CHECK( L"test_case_4_size16" );

  int src[] = { 50, 95, 32, 26, 41, 3, 20, 28, 73, 90, 57, 71, 49, 46, 35, 19 };

  int sum = ubmark_accumulate( src, 16 );

  ECE4750_CHECK_INT_EQ( sum, 735 );
}

//------------------------------------------------------------------------
// Test eval dataset
//------------------------------------------------------------------------

void test_case_5_eval_dataset()
{
  ECE4750_CHECK( L"test_case_5_eval_dataset" );

  int sum = ubmark_accumulate( eval_src, eval_size );

  ECE4750_CHECK_INT_EQ( sum, eval_ref );
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  if ( (__n <= 0) || (__n == 1) ) test_case_1_pos();
  if ( (__n <= 0) || (__n == 2) ) test_case_2_neg();
  if ( (__n <= 0) || (__n == 3) ) test_case_3_size9();
  if ( (__n <= 0) || (__n == 4) ) test_case_4_size16();
  if ( (__n <= 0) || (__n == 5) ) test_case_5_eval_dataset();

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}
