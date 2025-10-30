#=========================================================================
# Toplevel configure.ac for the Modular C++ Build System
#=========================================================================
# Please read the documenation in 'mcppbs-doc.txt' for more details on
# how the Modular C++ Build System works. For most new projects, a
# developer will only need to change the project metadata listed right
# below, and update which subprojects to include as part of this
# project. Do not place any configure checks here which will be used by
# a subproject - instead place such checks in the subproject's autoconf
# fragment.

#-------------------------------------------------------------------------
# Project metadata
#-------------------------------------------------------------------------

m4_define( proj_name,         [ECE4750 Software])
m4_define( proj_maintainer,   [Christopher Batten])
m4_define( proj_abbreviation, [ece4750])

#-------------------------------------------------------------------------
# Project version information
#-------------------------------------------------------------------------
# Version information is meant to be managed through a version control
# system's tags and revision numbers. In a working copy the version will
# not be defined here (you should just use the version control system's
# mechanisms). When we make a distribution then we can set the version
# here as formed by the scripts/vcs-version.sh script so that the
# distribution knows what version it came from. If you are not using
# version control then it is fine to set this directly.

m4_define( proj_version, [?])

#-------------------------------------------------------------------------
# Setup
#-------------------------------------------------------------------------

AC_INIT(proj_name,proj_version,proj_maintainer,proj_abbreviation)
AC_CONFIG_SRCDIR([ece4750/ece4750.h])
AC_CONFIG_AUX_DIR([scripts])
AC_CANONICAL_BUILD
AC_CANONICAL_HOST
AC_MSG_NOTICE([Host detected: $host])

#-------------------------------------------------------------------------
# Basic checks
#-------------------------------------------------------------------------

# Check for C compiler and set default C compiler flags
AS_IF([ test "${host}" = "riscv64-unknown-linux-gnu" || test "${host}" = "riscv64-unknown-elf"],
[
  AC_SUBST([LDFLAGS], ["-nostdlib -nodefaultlibs -nostartfiles"])
])
AC_PROG_CC
AC_SUBST([CFLAGS],["-std=c99 -Wall -Wextra -Wvla -Werror -Werror=vla -Wno-error=comment -Wconversion -Wuninitialized -g -O3"])


AS_IF([ test "${host}" = "riscv64-unknown-linux-gnu" || test "${host}" = "riscv64-unknown-elf" ],
[
  AC_SUBST([CFLAGS],["-std=c99 -D_RISCV -Wall -Wextra -Wvla -Werror -Werror=vla -Wno-error=comment -Wconversion -Wuninitialized -march=rv32im_zicsr -mabi=ilp32 -g -O3"])
  AC_SUBST([LDFLAGS], ["-march=rv32im_zicsr -mabi=ilp32 -nostdlib -T../scripts/tinyrv2.ld"])
])

# Check for tools to build libraries
AC_CHECK_TOOL([AR],[ar])
AC_CHECK_TOOL([RANLIB],[ranlib])

#-------------------------------------------------------------------------
# MCPPBS specific setup
#-------------------------------------------------------------------------

# Initialize the modular C++ build system

MCPPBS_INIT

# Check for non-native build

case ${host} in

  riscv*-*-*)
    riscv_crosscompile="yes"
  ;;

  *-*-*)
    riscv_crosscompile="no"
  ;;

esac

AC_SUBST([riscv_crosscompile])

#-------------------------------------------------------------------------
# MCPPBS subproject includes
#-------------------------------------------------------------------------
# Specify which subprojects make up this project. Subprojects can either
# be internal (ie. a subdirectory in the source directory) or external
# (ie. as an installed library). For external subprojects we use
# pkg-config to link against the appropriate library. Optional
# subprojects are denoted with an asterisk and are enabled with a
# --with-<subproject> configure command line option. Order the list so
# that subprojects only depend on those listed earlier. Here is an
# example project which includes four subprojects: the first is the
# standard utst subproject which has been installed and thus is being
# included as an external subproject. The second is an additional
# external subproject and the last is an optional internal subproject.
#
#  MCPPBS_INCLUDE_EXTERNAL([utst])
#  MCPPBS_INCLUDE_EXTERNAL([sproj-a])
#  MCPPBS_INCLUDE_INTERNAL([sproj-b])
#  MCPPBS_INCLUDE_INTERNAL([sproj-c*])
#

MCPPBS_INCLUDE_INTERNAL([ece4750])
MCPPBS_INCLUDE_INTERNAL([simple])
MCPPBS_INCLUDE_INTERNAL([ubmark])
#MCPPBS_INCLUDE_INTERNAL([mtbmark])

#-------------------------------------------------------------------------
# MCPPBS subproject libraries to install
#-------------------------------------------------------------------------
# The libraries and headers for these subprojects will be installed. The
# subprojects must have a pkg-config file named sproj/sproj.pc.in which
# is setup to allow other projects to use the installed subproject. Here
# is an example which installs the sproj-b subproject and sproj-c
# subproject (see above).
#
#  MCPPBS_INSTALL_LIBS([sproj-b,sproj-c])
#

#-------------------------------------------------------------------------
# Output
#-------------------------------------------------------------------------

AC_CONFIG_FILES([Makefile])
AC_OUTPUT

