//========================================================================
// ubmark-vvadd-eval
//========================================================================

#include "ece4750.h"
#include "ubmark-vvadd.h"
#include "ubmark-vvadd.dat"

int main( void )
{
  // Allocate destination array for results

  int* dest = ece4750_malloc( eval_size * (int)sizeof(int) );

  // Run the evaluation

  ece4750_stats_on();
  ubmark_vvadd( dest, eval_src0, eval_src1, eval_size );
  ece4750_stats_off();

  // Verify the results

  for ( int i = 0; i < eval_size; i++ ) {
    if ( dest[i] != eval_ref[i] ) {
      ece4750_wprintf( L"\n FAILED: dest[%d] != eval_ref[%d] (%d != %d)\n\n",
                       i, i, dest[i], eval_ref[i] );
      ece4750_exit(1);
    }
  }

  ece4750_wprintf( L"\n **PASSED** \n\n" );

  // Free destination array

  ece4750_free(dest);

  return 0;
}

