//========================================================================
// ubmark-accumulate-eval
//========================================================================

#include "ece4750.h"
#include "ubmark-accumulate.h"
#include "ubmark-accumulate.dat"

int main( void )
{
  // Run the evaluation

  ece4750_stats_on();
  int sum = ubmark_accumulate( eval_src, eval_size );
  ece4750_stats_off();

  // Verify the results

  if ( sum != eval_ref ) {
    ece4750_wprintf( L"\n FAILED: sum != eval_ref (%d != %d)\n\n",
                     sum, eval_ref );
    ece4750_exit(1);
  }

  ece4750_wprintf( L"\n **PASSED** \n\n" );

  return 0;
}

