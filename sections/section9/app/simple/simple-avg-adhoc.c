//========================================================================
// simple average program
//========================================================================

#include "ece4750.h"

__attribute__ ((noinline))
int avg( int x, int y )
{
  int sum = x + y;
  return sum / 2;
}

int main( void )
{
  int a = 10;
  int b = 20;
  int c = avg( a, b );

  ece4750_wprintf( L"average of %d and %d is %d\n", a, b, c );

  return 0;
}

