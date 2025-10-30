//========================================================================
// Unit tests for simple avg function
//========================================================================

#include "ece4750.h"
#include "simple-avg.h"

//------------------------------------------------------------------------
// Test positive inputs where the sum is even
//------------------------------------------------------------------------

void test_case_1_pos_pos_even()
{
  ECE4750_CHECK( L"test_case_1_pos_pos_even" );

  ECE4750_CHECK_INT_EQ( avg(   4,   8 ),   6 );
  ECE4750_CHECK_INT_EQ( avg( 100, 200 ), 150 );
  ECE4750_CHECK_INT_EQ( avg(  37,  53 ),  45 );
}

//------------------------------------------------------------------------
// Test positive inputs where the sum is odd
//------------------------------------------------------------------------
// Should truncate the result (round to zero)

void test_case_2_pos_pos_odd()
{
  ECE4750_CHECK( L"test_case_2_pos_pos_odd" );

  ECE4750_CHECK_INT_EQ( avg(   5,   8 ),   6 );
  ECE4750_CHECK_INT_EQ( avg( 101, 200 ), 150 );
  ECE4750_CHECK_INT_EQ( avg(  38,  53 ),  45 );
}

//------------------------------------------------------------------------
// Test negative inputs where the sum is even
//------------------------------------------------------------------------

void test_case_3_neg_neg_even()
{
  ECE4750_CHECK( L"test_case_3_neg_neg_even" );

  ECE4750_CHECK_INT_EQ( avg(   -4,   -8 ),   -6 );
  ECE4750_CHECK_INT_EQ( avg( -100, -200 ), -150 );
  ECE4750_CHECK_INT_EQ( avg(  -37,  -53 ),  -45 );
}

//------------------------------------------------------------------------
// Test positive inputs where the sum is odd
//------------------------------------------------------------------------
// Should truncate the result (round to zero)

void test_case_4_neg_neg_odd()
{
  ECE4750_CHECK( L"test_case_4_neg_neg_odd" );

  ECE4750_CHECK_INT_EQ( avg(   -5,   -8 ),   -6 );
  ECE4750_CHECK_INT_EQ( avg( -101, -200 ), -150 );
  ECE4750_CHECK_INT_EQ( avg(  -38,  -53 ),  -45 );
}

//------------------------------------------------------------------------
// Test positive/negative inputs where the sum is even
//------------------------------------------------------------------------

void test_case_5_pos_neg_even()
{
  ECE4750_CHECK( L"test_case_5_pos_neg_even" );

  ECE4750_CHECK_INT_EQ( avg(   -4,    8 ),    2 );
  ECE4750_CHECK_INT_EQ( avg( -100,  200 ),   50 );
  ECE4750_CHECK_INT_EQ( avg(  -38,   54 ),    8 );
}

//------------------------------------------------------------------------
// Test positive/negative inputs where the sum is odd
//------------------------------------------------------------------------

void test_case_6_pos_neg_odd()
{
  ECE4750_CHECK( L"test_case_6_pos_neg_odd" );

  ECE4750_CHECK_INT_EQ( avg(   -4,    9 ),    2 );
  ECE4750_CHECK_INT_EQ( avg( -100,  201 ),   50 );
  ECE4750_CHECK_INT_EQ( avg(  -38,   55 ),    8 );
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  if ( (__n <= 0) || (__n == 1) ) test_case_1_pos_pos_even();
  if ( (__n <= 0) || (__n == 2) ) test_case_2_pos_pos_odd();
  if ( (__n <= 0) || (__n == 3) ) test_case_3_neg_neg_even();
  if ( (__n <= 0) || (__n == 4) ) test_case_4_neg_neg_odd();
  if ( (__n <= 0) || (__n == 5) ) test_case_5_pos_neg_even();
  if ( (__n <= 0) || (__n == 6) ) test_case_6_pos_neg_odd();

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}

