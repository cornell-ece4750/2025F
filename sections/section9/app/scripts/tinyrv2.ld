/*======================================================================*/
/* Default TinyRV2 linker script                                          */
/*======================================================================*/

/*----------------------------------------------------------------------*/
/* Setup                                                                */
/*----------------------------------------------------------------------*/

/* The ENTRY command specifies the entry point (ie. first instruction to
   execute). The symbol _start is defined in crt0.S */

ENTRY( _start )
STARTUP( crt0.o )

/*----------------------------------------------------------------------*/
/* Sections                                                             */
/*----------------------------------------------------------------------*/
/* This is where we specify how the input sections map to output
   sections. The .= commands set the location counter, and the
   sections are inserted in increasing address order according to the
   location counter. The following statement will take all of the .bar
   input sections and reloate them into the .foo output section which
   starts at address 0x200.

    . = 0.x200;
    .foo : { *(.bar) }

   We can also set a global external symbol to a specific address in the
   output binary with this syntax:

    _etext = .;
    PROVIDE( etext = . );

   This will set the global symbol _ftext to the current location. If we
   wrap this in a PROVIDE commad, the symbol will only be set if it is
   not defined. We do this with symbols which don't begin with an
   underscore since technically in ansi C someone might have a function
   with the same name (eg. etext).

   If we need to label the beginning of a section we need to make sure
   that the linker doesn't insert an orphan section inbetween where we
   set the symbol and the actual begining of the section. We can do that
   by assigning the location dot to itself.

    . = .
    _ftext = .;
    .text :
    { }

*/

SECTIONS
{

  /DISCARD/ : { *(.note.gnu.build-id) }

  /*--------------------------------------------------------------------*/
  /* Code and read-only segment                                         */
  /*--------------------------------------------------------------------*/

  /* Begining of code and text segment */
  . = 0x000200;

  /* text: Program code section */
  .text : 
  {
    *(.text)
    *(.text.*)
  }

  /* rodata: Read-only data */
  .rodata : 
  {
    *(.rdata)
    *(.rodata)
    *(.rodata.*)
  }

  /*--------------------------------------------------------------------*/
  /* Initialized data segment                                           */
  /*--------------------------------------------------------------------*/

  /* Start of initialized data segment */
  . = ALIGN(16);
   _fdata = .;

  /* data: Writable data */
  .data : 
  {
    *(.data)
    *(.data.*)
  }

  /* _gp points to middle of sdata/sbss to maximize displacement range */
  . = ALIGN(16);
  _gp = . + 0x800;

  /* Writable small data segment */
  .sdata : 
  {
    *(.sdata)
    *(.sdata.*)
    *(.srodata.*)
  }

  /*--------------------------------------------------------------------*/
  /* Uninitialized data segment                                         */
  /*--------------------------------------------------------------------*/

  /* Start of uninitialized data segment */
  . = ALIGN(16);
  _fbss = .;

  /* Writable uninitialized small data segment */
  .sbss : 
  {
    *(.sbss)
    *(.sbss.*)
  }

  /* bss: Uninitialized writeable data section */
  . = .;
  .bss : 
  {
    *(.bss)
    *(.bss.*)
    *(COMMON)
  }

  /* End of uninitialized data segment (used for heap) */
  _end = ALIGN(16);
}
