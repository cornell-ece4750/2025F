//========================================================================
// Unit tests for unit testing framework
//========================================================================

#include "ece4750-misc.h"
#include "ece4750-check.h"
#include "ece4750-wprint.h"
#include "ece4750-malloc.h"

//------------------------------------------------------------------------
// Test malloc int
//------------------------------------------------------------------------

void test_case_1_malloc_int()
{
  ECE4750_CHECK( L"test_case_1_malloc_int" );

  int* a_ptr = ece4750_malloc(4);
  *a_ptr = 42;

  ECE4750_CHECK_INT_EQ( *a_ptr, 42  );

  ece4750_free(a_ptr);
}

//------------------------------------------------------------------------
// Test malloc struct
//------------------------------------------------------------------------

typedef struct
{
  int x;
  int y;
}
point_t;

void test_case_2_malloc_struct()
{
  ECE4750_CHECK( L"test_case_2_malloc_struct" );

  point_t* point_p = ece4750_malloc( sizeof(point_t) );
  point_p->x = -1;
  point_p->y =  1;

  ECE4750_CHECK_INT_EQ( point_p->x, -1 );
  ECE4750_CHECK_INT_EQ( point_p->y,  1 );

  ece4750_free(point_p);
}

//------------------------------------------------------------------------
// Test malloc array
//------------------------------------------------------------------------

void test_case_3_malloc_array()
{
  ECE4750_CHECK( L"test_case_3_malloc_array" );

  int* a = ece4750_malloc( 4*sizeof(int) );
  a[0] = 0;
  a[1] = 1;
  a[2] = 2;
  a[3] = 3;

  ECE4750_CHECK_INT_EQ( a[0], 0 );
  ECE4750_CHECK_INT_EQ( a[1], 1 );
  ECE4750_CHECK_INT_EQ( a[2], 2 );
  ECE4750_CHECK_INT_EQ( a[3], 3 );

  ece4750_free(a);
}

//------------------------------------------------------------------------
// Test slist
//------------------------------------------------------------------------

typedef struct _slist_int_node_t
{
  int                       value;
  struct _slist_int_node_t* next_p;
}
slist_int_node_t;

typedef struct
{
  slist_int_node_t* head_p;
}
slist_int_t;

// Construct slist

void slist_int_construct( slist_int_t* this )
{
  this->head_p = NULL;
}

// Destruct slist

void slist_int_destruct( slist_int_t* this )
{
  while ( this->head_p != NULL ) {
    slist_int_node_t* temp_p
      = this->head_p->next_p;
    ece4750_free( this->head_p );
    this->head_p = temp_p;
  }
}

// Push value on front of slist

void slist_int_push_front( slist_int_t* this, int v )
{
  slist_int_node_t* new_node_p
    = ece4750_malloc( sizeof(slist_int_node_t) );
  new_node_p->value  = v;
  new_node_p->next_p = this->head_p;
  this->head_p       = new_node_p;
}

// Test function

void test_case_4_slist()
{
  ECE4750_CHECK( L"test_case_4_slist" );

  slist_int_t lst;
  slist_int_construct ( &lst );
  slist_int_push_front( &lst, 12 );
  slist_int_push_front( &lst, 11 );
  slist_int_push_front( &lst, 10 );

  ECE4750_CHECK_INT_EQ( lst.head_p->value,                 10 );
  ECE4750_CHECK_INT_EQ( lst.head_p->next_p->value,         11 );
  ECE4750_CHECK_INT_EQ( lst.head_p->next_p->next_p->value, 12 );

  slist_int_destruct  ( &lst );
}

//------------------------------------------------------------------------
// main
//------------------------------------------------------------------------

int main( int argc, char** argv )
{
  __n = ( argc == 1 ) ? 0 : ece4750_atoi( argv[1] );

  if ( (__n <= 0) || (__n == 1) ) test_case_1_malloc_int();
  if ( (__n <= 0) || (__n == 2) ) test_case_2_malloc_struct();
  if ( (__n <= 0) || (__n == 3) ) test_case_3_malloc_array();
  if ( (__n <= 0) || (__n == 4) ) test_case_4_slist();

  ece4750_wprintf( L"\n\n" );
  return ece4750_check_status;
}

