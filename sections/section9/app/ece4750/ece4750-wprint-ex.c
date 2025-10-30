//========================================================================
// example of using wprint
//========================================================================

#include "ece4750-wprint.h"

const wchar_t* str = L"foobar";
int b = 0;
int a[] = { 1,2,3 };

int main( void )
{
  // Print some numbers and characters

  ece4750_wprint_int ( 42    );
  ece4750_wprint_char( L' '  );
  ece4750_wprint_int ( 13    );
  ece4750_wprint_char( L' '  );
  ece4750_wprint_int ( 57    );
  ece4750_wprint_char( L'\n' );

  // Print some strings

  ece4750_wprint_str( L"Testing print function: \n" );
  ece4750_wprint_str( L"Hello, World!\n" );

  // Use printf

  ece4750_wprintf( L"number = %d\n", 42 );
  ece4750_wprintf( L"char   = %C\n", L'a' );
  ece4750_wprintf( L"string = %S\n", L"foobar" );

  ece4750_wprintf( L"number = %d, char = %C, string = %S \n", 42, L'a', L"foobar" );

  return 0;
}

