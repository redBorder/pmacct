dnl Process this file with autoconf to produce a configure script.
dnl configuration file for pmacct 

AC_INIT([pmacct], [1.7.1-git], [paolo@pmacct.net])
AM_INIT_AUTOMAKE([foreign])
AC_CONFIG_MACRO_DIR([m4])
LT_INIT
AC_PREFIX_DEFAULT([/usr/local])
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES(yes)])

COMPILE_ARGS="${ac_configure_args}"

dnl Checks for programs.
AC_PROG_CC

dnl pkg-config stuff
PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:/usr/local/lib/pkgconfig
export PKG_CONFIG_PATH
PKG_PROG_PKG_CONFIG

AC_CANONICAL_HOST

AC_MSG_CHECKING(OS)
AC_MSG_RESULT($host_os)

AC_MSG_CHECKING(hardware)
AC_MSG_RESULT($host_cpu)

dnl initial checks; tweakings to CFLAGS and LDFLAGS
dnl see final checks for tweakings to LIBS
if test "x$ac_cv_prog_gcc" = xyes ; then
  CFLAGS="-O2 ${CFLAGS}"
fi

dnl set debug level
AC_MSG_CHECKING([whether to enable debugging compiler options])
AC_ARG_ENABLE(debug,
	[  --enable-debug                   Enable debugging compiler options (default: no)],
	[
	        if test x$enableval = x"yes" ; then
			AC_MSG_RESULT(yes)
			tmp_CFLAGS=`echo $CFLAGS | sed 's/O2/O0/g'`
			CFLAGS="$tmp_CFLAGS"
  			CFLAGS="$CFLAGS -g -W -Wall"
		else
			AC_MSG_RESULT(no)
		fi
	],
	[
		AC_MSG_RESULT(no)
	]
)

dnl set relax level
AC_MSG_CHECKING([whether to relax compiler optimizations])
AC_ARG_ENABLE(relax,
[  --enable-relax                   Relax compiler optimization (default: no)],
	[
		if test x$enableval = x"yes" ; then
			AC_MSG_RESULT(yes)
        		tmp_CFLAGS=`echo $CFLAGS | sed 's/O2/O0/g'`
       			CFLAGS="$tmp_CFLAGS"
		else
			AC_MSG_RESULT(no)
		fi
	],
	[
        	AC_MSG_RESULT(no)
	]
)

dnl: shared object handling
AC_MSG_CHECKING([whether to disable linking against shared objects])
AC_ARG_ENABLE(so,
        [  --disable-so                     Disable linking against shared objects (default: no)],
	[ 
        if test x$enableval = x"yes" ; then
          AC_MSG_RESULT(no)
          AC_CHECK_FUNC(dlopen, [ USING_DLOPEN="yes" ], [])
          AC_CHECK_LIB(dl, dlopen,
                [ USING_DLOPEN="yes"
                  LIBS="${LIBS} -ldl" ],
                  [])
          if test x"$USING_DLOPEN" != x"yes"; then
                AC_MSG_ERROR(Unable to find dlopen(). Try with --disable-so)
          fi
        else
          AC_MSG_RESULT(yes)
	  if test "x$ac_cv_prog_gcc" = xyes ; then
		LDFLAGS="-static ${LDFLAGS}"
	  fi
        fi
        ],
	[
        AC_MSG_RESULT(no)
        AC_CHECK_FUNC(dlopen, [ USING_DLOPEN="yes" ], [])
        AC_CHECK_LIB(dl, dlopen,
                [ USING_DLOPEN="yes"
                  LIBS="${LIBS} -ldl" ],
                  [])
        if test x"$USING_DLOPEN" != x"yes"; then
                AC_MSG_ERROR(Unable to find dlopen(). Try with --disable-so)
        fi
	]
)
dnl finish: shared object handling

dnl os specific flags
case "$host_os" in
  Sun*)
    AC_DEFINE(SOLARIS, 1)
    LIBS="-lresolv -lsocket -lnsl ${LIBS}"
    ;;
  *BSD)
    AC_DEFINE(BSD, 1)
    ;;
  linux*)
    AC_DEFINE(LINUX, 1)
    ;;
esac

dnl cpu specific flags
case "$host_cpu" in
  sun*)
  AC_DEFINE(CPU_sparc, 1)
  ;;
esac

AC_CHECK_PROG(MAKE, gmake, gmake)
if test x"$MAKE" = x""; then
  AC_CHECK_PROG(MAKE, make, make)
fi
AC_SUBST(MAKE)
AC_PROG_MAKE_SET

dnl
dnl some systems have __progname ; if this is the case and we play around argv
dnl we need to enable a minor hack to make things work nicely.
dnl
AC_MSG_CHECKING(for __progname)
AC_TRY_LINK([ extern char *__progname; ], 
[ __progname = "test"; ],
[AC_MSG_RESULT(yes); AC_DEFINE(PROGNAME, 1)], [AC_MSG_RESULT(no)])

dnl
dnl Some checks to understand whether we need to instruct the linker for
dnl exporting collector symbols to dynamically loaded classifiers. 
dnl
dnl OS'es with ELF executables using the GNU linker (Linux and recent *BSD,
dnl in rare cases Solaris) typically need '-Wl,-export-dynamic'; some SYSv4
dnl systems instead need '-Wl,-Bexport'; AIX 4.x wants -Wl,-bexpall,-brtl'.
dnl
      
AC_MSG_CHECKING(for extra flags needed to export symbols)
if test "x$ac_cv_prog_gcc" = xyes ; then
	save_ldflags="${LDFLAGS}"
	LDFLAGS="-Wl,--export-dynamic ${save_ldflags}"
	AC_TRY_LINK(,,
		[ AC_MSG_RESULT(--export-dynamic) ],
		[ LDFLAGS="-Wl,-Bexport ${save_ldflags}"
		  AC_TRY_LINK(,,
			[ AC_MSG_RESULT(-Bexport) ],
		  	[ AC_MSG_RESULT(none)
		    	  LDFLAGS="${save_ldflags}" ]
		  )
		]
	)
else
	AC_MSG_RESULT(none)
fi

dnl
dnl some C compilers (ex. MipsPRO) don't know how to parse the 'inline' keyword
dnl
AC_MSG_CHECKING(for static inline)
AC_TRY_COMPILE([#include <stdio.h>]

static inline func()
{
}
,
[
  func();
],
[AC_MSG_RESULT(yes)], [AC_MSG_RESULT(no); AC_DEFINE(NOINLINE, 1)])

dnl
dnl Check for architecture endianess: big | little 
dnl
dnl XXX: switch to manually define this feature 
ac_cv_endianess="unknown"
if test x"$ac_cv_endianess" = x"unknown"; then
  AC_MSG_CHECKING(endianess)
  AC_TRY_RUN([main () {

  union
  {
    long l;
    char c[sizeof (long)];
  } u;
  u.l = 1;
  exit (u.c[sizeof (long) - 1] == 1);
  }], ac_cv_endianess="little", ac_cv_endianess="big", ac_cv_endianess="little")
  AC_MSG_RESULT($ac_cv_endianess)
fi

if test x"$ac_cv_endianess" = x"big"; then
  AC_DEFINE(IM_BIG_ENDIAN, 1)
fi
if test x"$ac_cv_endianess" = x"little"; then
  AC_DEFINE(IM_LITTLE_ENDIAN, 1)
fi

dnl
dnl Check for unaligned memory access; based entirely over
dnl AC_LBL_UNALIGNED_ACCESS
dnl
dnl XXX: switch to manually define this feature;
ac_cv_unaligned="unknown"
case "$host_cpu" in
  alpha*|arm*|hp*|mips*|sh*|sparc*|ia64|nv1)
    ac_cv_unaligned="fail"
    AC_MSG_CHECKING(unaligned accesses)
    AC_MSG_RESULT($ac_cv_unaligned)
    ;;
esac

if test x"$ac_cv_unaligned" = x"unknown"; then
  AC_MSG_CHECKING(unaligned accesses)
  cat > conftest.c << EOF
    #include <sys/types.h>
    #include <sys/wait.h>
    #include <stdio.h>
    unsigned char a[[5]] = { 1, 2, 3, 4, 5 };
    main () {
    	unsigned int i;
        pid_t pid;
        int status;
        /* avoid "core dumped" message */
        pid = fork();
        if (pid <  0) exit(2);
        if (pid > 0) {
        	/* parent */
                pid = waitpid(pid, &status, 0);
                if (pid < 0) exit(3);
                exit(!WIFEXITED(status));
        }
        /* child */
        i = *(unsigned int *)&a[[1]];
        printf("%d\n", i);
        exit(0);
    }
EOF
  ${CC-cc} -o conftest $CFLAGS $CPPFLAGS $LDFLAGS \
	conftest.c $LIBS >/dev/null 2>&1
  if test ! -x conftest ; then
    ac_cv_unaligned="fail"
  else
    ./conftest >conftest.out
    if test ! -s conftest.out ; then ac_cv_unaligned="fail"
    else ac_cv_unaligned="ok"
    fi
  fi
  rm -f conftest* core core.conftest
  AC_MSG_RESULT($ac_cv_unaligned)
fi

if test x"$ac_cv_unaligned" = x"fail"; then
  AC_DEFINE(NEED_ALIGN, 1)
fi

AC_MSG_CHECKING([whether to enable L2 features])
AC_ARG_ENABLE(l2,
        [  --enable-l2                      Enable Layer-2 features and support (default: yes)],
	[
        	if test x$enableval = x"yes" ; then
        		AC_MSG_RESULT(yes)
	  		AC_DEFINE(HAVE_L2, 1) 
        	else
			AC_MSG_RESULT(no)
        	fi
	],
	[
        	AC_MSG_RESULT(yes)
		AC_DEFINE(HAVE_L2, 1) 
		COMPILE_ARGS="${COMPILE_ARGS} '--enable-l2'"
	]
)

AC_MSG_CHECKING([whether to enable IPv6 code])
AC_ARG_ENABLE(ipv6,
        [  --enable-ipv6                    Enable IPv6 code (default: yes)],
	[ 
		if test x$enableval = x"yes" ; then
        		AC_MSG_RESULT(yes)
        		AC_CHECK_FUNCS(inet_pton)
        		if test x"$ac_cv_func_inet_pton" = x"no"; then
        			AC_MSG_ERROR(ERROR: missing inet_pton(); disable IPv6 hooks !)
        		fi

			AC_CHECK_FUNCS(inet_ntop)
			if test x"$ac_cv_func_inet_ntop" = x"no"; then
          			AC_MSG_ERROR(ERROR: missing inet_ntop(); disable IPv6 hooks !)
        		fi

			AC_DEFINE(ENABLE_IPV6, 1)
			ipv6support="yes"
		else
			AC_MSG_RESULT(no)
			ipv6support="no"
		fi
	],
	[
        	AC_MSG_RESULT(yes)
        		AC_CHECK_FUNCS(inet_pton)
        		if test x"$ac_cv_func_inet_pton" = x"no"; then
        			AC_MSG_ERROR(ERROR: missing inet_pton(); disable IPv6 hooks !)
        		fi

			AC_CHECK_FUNCS(inet_ntop)
			if test x"$ac_cv_func_inet_ntop" = x"no"; then
          			AC_MSG_ERROR(ERROR: missing inet_ntop(); disable IPv6 hooks !)
        		fi

			AC_DEFINE(ENABLE_IPV6, 1)
		ipv6support="yes"
		COMPILE_ARGS="${COMPILE_ARGS} '--enable-ipv6'"
	]
)

AC_MSG_CHECKING([whether to enable IP prefix labels])
AC_ARG_ENABLE(plabel,
  [  --enable-plabel                  Enable IP prefix labels (default: no)],
  [
	if test x$enableval = x"yes" ; then
          AC_MSG_RESULT(yes)
          AC_DEFINE(ENABLE_PLABEL, 1)
	else
          AC_MSG_RESULT(no)
	fi
  ],
  [
	AC_MSG_RESULT(no)
  ])

AC_ARG_WITH(pcap-includes,
  [  --with-pcap-includes=DIR         Search the specified directory for header files],
  [
	AC_LINEARIZE_PATH($withval, withval=$absdir)
	INCLUDES="${INCLUDES} -I$withval"
	PCAPINCLS=$withval
	PCAPINCLUDESFOUND=1
  ])

if test x"$PCAPINCLS" != x""; then
  AC_MSG_CHECKING(your own pcap includes)
  if test -r $PCAPINCLS/pcap.h; then 
    AC_MSG_RESULT(ok)
    AC_DEFINE(HAVE_PCAP_H, 1)
  else
    AC_MSG_RESULT(no)
    AC_MSG_ERROR(ERROR: missing pcap.h in $PCAPINCLS) 
  fi
fi

if test x"$PCAPINCLUDESFOUND" = x""; then
  AC_MSG_CHECKING([default locations for pcap.h])
  if test -r /usr/include/pcap.h; then
    AC_MSG_RESULT([found in /usr/include])
    PCAPINCLUDESFOUND=1
    AC_DEFINE(HAVE_PCAP_H, 1)
  elif test -r /usr/include/pcap/pcap.h; then
    AC_MSG_RESULT([found in /usr/include])
    PCAPINCLUDESFOUND=1
    AC_DEFINE(HAVE_PCAP_PCAP_H, 1)
  elif test -r /usr/local/include/pcap.h; then
    AC_MSG_RESULT([found in /usr/local/include])
    INCLUDES="${INCLUDES} -I/usr/local/include"
    PCAPINCLUDESFOUND=1
    AC_DEFINE(HAVE_PCAP_H, 1) 
  elif test -r /usr/local/include/pcap/pcap.h; then
    AC_MSG_RESULT([found in /usr/local/include])
    INCLUDES="${INCLUDES} -I/usr/local/include"
    PCAPINCLUDESFOUND=1
    AC_DEFINE(HAVE_PCAP_PCAP_H, 1)
  fi
  if test x"$PCAPINCLUDESFOUND" = x""; then
    AC_MSG_RESULT([not found])
    AC_MSG_ERROR(ERROR: missing pcap.h)
  fi
fi

AC_ARG_WITH(pcap-libs,
  [  --with-pcap-libs=DIR             Search the specified directory for pcap library],
  [	
	AC_LINEARIZE_PATH($withval, withval=$absdir)
	LIBS="${LIBS} -L$withval"
	PCAPLIB=$withval
	PCAPLIBFOUND=1
  ])

if test x"$PCAPLIB" != x""; then
  AC_MSG_CHECKING(your own pcap libraries)
  if test -r $PCAPLIB/libpcap.a -o -r $PCAPLIB/libpcap.so; then
    AC_MSG_RESULT(ok)
    PCAP_LIB_FOUND=1
    AC_MSG_CHECKING(for PF_RING library)
    if test -r $PCAPLIB/libpfring.a -o -r $PCAPLIB/libpfring.so; then
      LIBS="${LIBS} -lpfring -lpcap"
      AC_MSG_RESULT(yes)
      PFRING_LIB_FOUND=1
      AC_DEFINE(PFRING_LIB_FOUND, 1)
    else
      AC_MSG_RESULT(no)
    fi
  else
    AC_MSG_RESULT(no)
    AC_MSG_ERROR(ERROR: unable to find pcap library in $PCAPLIB)
  fi
fi

if test x"$PCAPLIBFOUND" = x""; then
  AC_MSG_CHECKING([default locations for libpcap])
  if test -r /usr/local/lib/libpcap.a -o -r /usr/local/lib/libpcap.so; then
    LIBS="${LIBS} -L/usr/local/lib"
    AC_MSG_RESULT([found in /usr/local/lib])
    PCAPLIBFOUND=1
    AC_MSG_CHECKING(for PF_RING library)
    if test -r /usr/local/lib/libpfring.a -o -r /usr/local/lib/libpfring.so; then
      LIBS="${LIBS} -lpfring -lpcap"
      AC_MSG_RESULT(yes)
      PFRING_LIB_FOUND=1
      AC_DEFINE(PFRING_LIB_FOUND, 1)
    else
      AC_MSG_RESULT(no)
    fi
  else
    AC_MSG_RESULT(no)
  fi
fi

dnl Checks for libraries.

dnl libpcap is checked only if PF_RING is not found
if test x"$PFRING_LIB_FOUND" = x""; then
  AC_CHECK_LIB([pcap], [pcap_dispatch], [], [AC_MSG_ERROR([
    ERROR: missing pcap library. Refer to: http://www.tcpdump.org/
  ])])

  AC_CHECK_LIB([pcap], [pcap_set_protocol], [ AC_DEFINE(PCAP_SET_PROTOCOL, 1) ], [])
  AC_CHECK_LIB([pcap], [bpf_filter], [ AC_DEFINE(PCAP_NOBPF, 1) ], [])
else
  dnl Unable to test: we should check for these libs
  #AC_CHECK_LIB([numa], [numa_bind], [], [AC_MSG_ERROR([
  #  ERROR: missing libnuma devel. Requirement for building PF_RING.
  #])])

  #AC_CHECK_LIB([rt], [clock_gettime], [], [AC_MSG_ERROR([
  #  ERROR: missing librt devel. Requirement for building PF_RING.
  #])])

  LIBS="${LIBS} -lrt -lnuma"
fi

dnl packet capture type check; taken from libpcap.
AC_MSG_CHECKING(packet capture type)
if test -r /dev/bpf0 ; then
        V_PCAP=bpf
elif test -r /usr/include/net/pfilt.h ; then
        V_PCAP=pf
elif test -r /dev/enet ; then
        V_PCAP=enet
elif test -r /dev/nit ; then
        V_PCAP=snit
elif test -r /usr/include/sys/net/nit.h ; then
        V_PCAP=nit
elif test -r /usr/include/linux/socket.h ; then
        V_PCAP=linux
elif test -r /usr/include/net/raw.h ; then
        V_PCAP=snoop
elif test -r /usr/include/odmi.h ; then
        #
        # On AIX, the BPF devices might not yet be present - they're
        # created the first time libpcap runs after booting.
        # We check for odmi.h instead.
        #
        V_PCAP=bpf
elif test -r /usr/include/sys/dlpi.h ; then
        V_PCAP=dlpi
elif test -c /dev/bpf0 ; then           # check again in case not readable
        V_PCAP=bpf
elif test -c /dev/enet ; then           # check again in case not readable
        V_PCAP=enet
elif test -c /dev/nit ; then            # check again in case not readable
        V_PCAP=snit
else
        V_PCAP=null
fi
AC_MSG_RESULT($V_PCAP)
AC_DEFINE_UNQUOTED(PCAP_TYPE_$V_PCAP, 1)

dnl start: mysql handling
AC_MSG_CHECKING(whether to enable MySQL support)
AC_ARG_ENABLE(mysql,
  [  --enable-mysql                   Enable MySQL support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)

dnl Unfortunately, no pkg-config support for MySQL
    AC_CHECK_PROG([MYSQL_CONFIG], [mysql_config], [mysql_config], [no])
    if test "x${MYSQL_CONFIG}" = "xno"; then
      AC_MSG_ERROR([ERROR: missing mysql_config program])
    fi
    AC_CHECK_LIB([mysqlclient], [mysql_init],
                 [MYSQL_CFLAGS=`$MYSQL_CONFIG --cflags`
                  MYSQL_LIBS=`$MYSQL_CONFIG --libs`],
                 [AC_MSG_ERROR([ERROR: missing MySQL client library])],
                 [`$MYSQL_CONFIG --libs`])
    dnl version check not enforced with a AC_MSG_ERROR for now
    AX_LIB_MYSQL(5.6.3)

    AC_SUBST(MYSQL_CFLAGS)
    AC_SUBST(MYSQL_LIBS)

    PLUGINS="${PLUGINS} mysql"
    USING_SQL="yes"
    USING_MYSQL="yes"
    PMACCT_CFLAGS="$PMACCT_CFLAGS $MYSQL_CFLAGS"
    AC_DEFINE(WITH_MYSQL, 1)
    _save_LIBS="$LIBS"
    LIBS="$LIBS $MYSQL_LIBS"
    AC_CHECK_LIB([mysqlclient], [mysql_query])
    LIBS="$_save_LIBS"
    _save_CFLAGS="$CFLAGS"
    CFLAGS="$CFLAGS $MYSQL_CFLAGS"
    AC_CHECK_HEADER([mysql/mysql.h])
    CFLAGS="$_save_CFLAGS"
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: mysql handling

dnl start: pgsql handling
AC_MSG_CHECKING(whether to enable PostgreSQL support)
AC_ARG_ENABLE(pgsql,
  [  --enable-pgsql                   Enable PostgreSQL support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([PGSQL], [libpq >= 9.3], [
      PLUGINS="${PLUGINS} pgsql"
      USING_SQL="yes"
      USING_PGSQL="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $PGSQL_CFLAGS"
      AC_DEFINE(WITH_PGSQL, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $PGSQL_LIBS"
      AC_CHECK_LIB([pq], [PQexec])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $PGSQL_CFLAGS"
      AC_CHECK_HEADER([libpq-fe.h])
      CFLAGS="$_save_CFLAGS"
    ], [
      AC_MSG_ERROR([Missing PQ library. Refer to: http://www.postgresql.org/download/])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: pgsql handling

dnl start: mongodb handling
AC_MSG_CHECKING(whether to enable MongoDB support)
AC_ARG_ENABLE(mongodb,
  [  --enable-mongodb                 Enable MongoDB support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([MONGODB], [libmongoc],, [
	AC_MSG_CHECKING([default locations for libmongoc])
	if test -r /usr/lib/libmongoc.a -o -r /usr/lib/libmongoc.so; then
		MONGODB_LIBS="-L/usr/lib -lmongoc"
		AC_MSG_RESULT([found in /usr/lib])
	elif test -r /usr/lib64/libmongoc.a -o -r /usr/lib64/libmongoc.so; then
		MONGODB_LIBS="-L/usr/lib64 -lmongoc"
		AC_MSG_RESULT([found in /usr/lib64])
	elif test -r /usr/local/lib/libmongoc.a -o -r /usr/local/lib/libmongoc.so; then
		MONGODB_LIBS="-L/usr/local/lib -lmongoc"
		AC_MSG_RESULT([found in /usr/local/lib])
	else
		AC_MSG_RESULT([not found])
                _save_LIBS="$LIBS"
                LIBS="$LIBS $MONGODB_LIBS"
		AC_CHECK_LIB([mongoc], [mongo_connect], [], [AC_MSG_ERROR([
			ERROR: missing MongoDB library (0.8 version). Refer to: https://github.com/mongodb/mongo-c-driver-legacy
		])])
                LIBS="$_save_LIBS"
	fi

	AC_MSG_CHECKING([default locations for mongo.h])
	if test -r /usr/include/mongo.h; then
		MONGODB_CFLAGS="-I/usr/include"
		AC_MSG_RESULT([found in /usr/include])
	elif test -r /usr/local/include/mongo.h; then
		MONGODB_CFLAGS="-I/usr/local/include"
		AC_MSG_RESULT([found in /usr/local/include])
	else
		AC_MSG_RESULT([not found])
                _save_CFLAGS="$CFLAGS"
                CFLAGS="$CFLAGS $MONGODB_CFLAGS"
		AC_CHECK_HEADER([mongo.h], [], [AC_MSG_ERROR(ERROR: missing MongoDB headers)])
                CFLAGS="$_save_CFLAGS"
	fi
    ])
    PLUGINS="${PLUGINS} mongodb"
    USING_MONGODB="yes"
    PMACCT_CFLAGS="$PMACCT_CFLAGS $MONGODB_CFLAGS"
    AC_DEFINE(WITH_MONGODB, 1)
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: mongodb handling

dnl start: sqlite3 handling
AC_MSG_CHECKING(whether to enable SQLite3 support)
AC_ARG_ENABLE(sqlite3,
  [  --enable-sqlite3                 Enable SQLite3 support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    dnl reasonably old libsqlite3 already support pkg-config
    PKG_CHECK_MODULES([SQLITE3], [sqlite3 >= 3.7.13], [
      PLUGINS="${PLUGINS} sqlite3"
      USING_SQL="yes"
      USING_SQLITE3="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $SQLITE3_CFLAGS"
      AC_DEFINE(WITH_SQLITE3, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $SQLITE3_LIBS"
      AC_CHECK_LIB([sqlite3], [sqlite3_exec])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $SQLITE3_CFLAGS"
      AC_CHECK_HEADER([sqlite3.h])
      CFLAGS="$_save_CFLAGS"
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: sqlite3 handling

dnl start: RabbitMQ/AMQP handling
AC_MSG_CHECKING(whether to enable RabbitMQ/AMQP support)
AC_ARG_ENABLE(rabbitmq,
  [  --enable-rabbitmq                Enable RabbitMQ/AMQP support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    dnl reasonably old librabbitmq already support pkg-config
    PKG_CHECK_MODULES([RABBITMQ], [librabbitmq >= 0.8.0], [
      PLUGINS="${PLUGINS} rabbitmq"
      USING_RABBITMQ="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $RABBITMQ_CFLAGS"
      AC_DEFINE(WITH_RABBITMQ, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $RABBITMQ_LIBS"
      AC_CHECK_LIB([rabbitmq], [amqp_basic_publish])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $RABBITMQ_CFLAGS"
      AC_CHECK_HEADER([amqp.h])
      CFLAGS="$_save_CFLAGS"
    ], [
      AC_MSG_ERROR([Missing RabbitMQ C API. Refer to: https://github.com/alanxz/rabbitmq-c/])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: RabbitMQ/AMQP handling

dnl start: ZMQ/AMQP handling
AC_MSG_CHECKING(whether to enable ZMQ/AMQP support)
AC_ARG_ENABLE(zmq,
  [  --enable-zmq                     Enable ZMQ/AMQP support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([ZMQ], [libzmq >= 4.2.0], [
      SUPPORTS="${SUPPORTS} zmq"
      USING_ZMQ="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $ZMQ_CFLAGS"
      AC_DEFINE(WITH_ZMQ, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $ZMQ_LIBS"
      AC_CHECK_LIB([zmq], [zmq_send])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $ZMQ_CFLAGS"
      AC_CHECK_HEADER([zmq.h])
      CFLAGS="$_save_CFLAGS"
    ], [
      AC_MSG_ERROR([Missing ZeroMQ. Refer to: http://zeromq.org/intro:get-the-software])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: ZMQ/AMQP handling

dnl start: Kafka handling
AC_MSG_CHECKING(whether to enable Kafka support)
AC_ARG_ENABLE(kafka,
  [  --enable-kafka                   Enable Kafka support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([KAFKA], [rdkafka >= 0.9.2], [
      PLUGINS="${PLUGINS} kafka"
      USING_KAFKA="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $KAFKA_CFLAGS"
      AC_DEFINE(WITH_KAFKA, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $KAFKA_LIBS"
      AC_CHECK_LIB([rdkafka], [rd_kafka_produce])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $KAFKA_CFLAGS"
      AC_CHECK_HEADER([librdkafka/rdkafka.h])
      CFLAGS="$_save_CFLAGS"
    ], [
      AC_MSG_ERROR([Missing librdkafka. Refer to: https://github.com/edenhill/librdkafka/])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: Kafka handling

dnl start: geoip handling
AC_MSG_CHECKING(whether to enable GeoIP support)
AC_ARG_ENABLE(geoip,
  [  --enable-geoip                   Enable GeoIP support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    dnl reasonably old Maxmind GeoIP v1 already support pkg-config
    PKG_CHECK_MODULES([GEOIP], [geoip >= 1.0.0], [
      SUPPORTS="${SUPPORTS} geoip"
      USING_MMGEOIP="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $GEOIP_CFLAGS"
      AC_DEFINE(WITH_GEOIP, 1)
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)

AC_MSG_CHECKING(whether to enable GeoIPv2 (libmaxminddb) support)
AC_ARG_ENABLE(geoipv2,
  [  --enable-geoipv2                 Enable GeoIPv2 (libmaxminddb) support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([GEOIPV2], [libmaxminddb >= 1.2], [
      SUPPORTS="${SUPPORTS} geoipv2"
      USING_MMGEOIPV2="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $GEOIPV2_CFLAGS"
      AC_DEFINE(WITH_GEOIPV2, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $GEOIPV2_LIBS"
      AC_CHECK_LIB([maxminddb], [MMDB_open])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $GEOIPV2_CFLAGS"
      AC_CHECK_HEADER([maxminddb.h])
      CFLAGS="$_save_CFLAGS"
    ], [
      AC_MSG_ERROR([Missing Maxmind libmaxminddb C library. Refer to: http://www.maxmind.com/download/geoip/api/c/])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: GeoIP handling

dnl start: Jansson handling
AC_MSG_CHECKING(whether to enable Jansson support)
AC_ARG_ENABLE(jansson,
  [  --enable-jansson                 Enable Jansson support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    dnl reasonably old Jansson already support pkg-config
    PKG_CHECK_MODULES([JANSSON], [jansson >= 2.5], [
      SUPPORTS="${SUPPORTS} jansson"
      USING_JANSSON="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $JANSSON_CFLAGS"
      AC_DEFINE(WITH_JANSSON, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $JANSSON_LIBS"
      AC_CHECK_LIB([jansson], [json_object])
      AC_CHECK_FUNCS([json_object_update_missing])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $JANSSON_CFLAGS"
      AC_CHECK_HEADER([jansson.h])
      CFLAGS="$_save_CFLAGS"
    ], [
      AC_MSG_ERROR([Missing libjansson. Refer to: http://www.digip.org/jansson/])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: Jansson handling

dnl start: Avro handling
AC_MSG_CHECKING(whether to enable Avro support)
AC_ARG_ENABLE(avro,
  [  --enable-avro                    Enable Apache Avro support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([AVRO], [avro-c >= 1.8], [
      SUPPORTS="${SUPPORTS} avro"
      USING_AVRO="yes"
      PMACCT_CFLAGS="$PMACCT_CFLAGS $AVRO_CFLAGS"
      AC_DEFINE(WITH_AVRO, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $AVRO_LIBS"
      AC_CHECK_LIB([avro], [avro_record_get])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $AVRO_CFLAGS"
      AC_CHECK_HEADER([avro.h])
      CFLAGS="$_save_CFLAGS"
    ], [
      AC_MSG_ERROR([Missing Apache Avro C library. Refer to: http://www.apache.org/dyn/closer.cgi/avro/])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: Avro handling

dnl start: nDPI handling
AC_ARG_WITH(ndpi-static-lib,
  [  --with-ndpi-static-lib=DIR       Search the specified directory for nDPI static library],
  [
        AC_LINEARIZE_PATH($withval, withval=$absdir)
        NDPI_CUST_STATIC_LIB=$withval
  ])

if test x"$NDPI_CUST_STATIC_LIB" != x""; then
  AC_MSG_CHECKING(your own nDPI library)
  if test -r $NDPI_CUST_STATIC_LIB/libndpi.a; then
    AC_MSG_RESULT(ok)
    NDPI_CUST_STATIC_LIB_FOUND="yes"
  else
    AC_MSG_RESULT(no)
    AC_MSG_ERROR(ERROR: unable to find nDPI library in $NDPI_CUST_STATIC_LIB)
  fi
fi

AC_MSG_CHECKING(whether to enable nDPI support)
AC_ARG_ENABLE(ndpi,
  [  --enable-ndpi                    Enable nDPI support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([NDPI], [libndpi >= 2.0], [
      SUPPORTS="${SUPPORTS} ndpi"
      USING_NDPI="yes"

      if test x"$NDPI_CFLAGS" != x""; then
        NDPI_CFLAGS_INST=`echo $NDPI_CFLAGS | sed 's/ $//'`
        NDPI_CFLAGS_INST="$NDPI_CFLAGS_INST/libndpi"
      else
        NDPI_CFLAGS_INST=""
      fi
      PMACCT_CFLAGS="$PMACCT_CFLAGS $NDPI_CFLAGS $NDPI_CFLAGS_INST"

      AC_DEFINE(WITH_NDPI, 1)
      _save_LIBS="$LIBS"
      LIBS="$LIBS $NDPI_LIBS"
      AC_CHECK_LIB([ndpi], [ndpi_init_detection_module])
      LIBS="$_save_LIBS"
      _save_CFLAGS="$CFLAGS"
      CFLAGS="$CFLAGS $NDPI_CFLAGS"
      AC_CHECK_HEADER([libndpi/ndpi_main.h])
      CFLAGS="$_save_CFLAGS"

      dnl XXX: to be improved: avoid linking both static and dynamic libs
      if test x"$NDPI_CUST_STATIC_LIB_FOUND" = x"yes"; then
        NDPI_LIBS_STATIC="$NDPI_CUST_STATIC_LIB/libndpi.a"
      elif test -r /usr/lib/libndpi.a; then
        NDPI_LIBS_STATIC="/usr/lib/libndpi.a"
      elif test -r /usr/local/lib/libndpi.a; then
        NDPI_LIBS_STATIC="/usr/local/lib/libndpi.a"
      elif test -r /usr/local/nDPI/lib/libndpi.a; then
        NDPI_LIBS_STATIC="/usr/local/nDPI/lib/libndpi.a"
      else
        AC_MSG_ERROR([ERROR: missing nDPI static library])
      fi

      AC_SUBST([NDPI_LIBS_STATIC])
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
  [
    AC_MSG_RESULT(no)
  ]
)
dnl finish: nDPI handling

if test x"$USING_DLOPEN" = x"yes"; then
	AC_DEFINE(HAVE_DLOPEN, 1)
else
	# Adding linking to libdl here 1) if required and 2) in case of --disable-so
	if test x"$USING_MYSQL" = x"yes" -o x"$USING_SQLITE3" = x"yes"; then
		AC_CHECK_LIB([dl], [dlopen], [LIBS="${LIBS} -ldl"], [AC_MSG_ERROR([
		  ERROR: missing libdl devel.
		])])
	fi
fi

AC_CHECK_LIB([z], [deflate], [
	LIBS="${LIBS} -lz"
	AC_DEFINE(HAVE_ZLIB, 1)]
)

LIBS="${LIBS} -lpthread"

dnl Checks for header files.
AC_HEADER_STDC
AC_HEADER_SYS_WAIT
AC_CHECK_HEADERS([getopt.h sys/select.h sys/time.h])

dnl Checks for typedefs, structures, and compiler characteristics.
AC_CHECK_TYPE(u_int64_t, [AC_DEFINE(HAVE_U_INT64_T, 1)])
AC_CHECK_TYPE(u_int32_t, [AC_DEFINE(HAVE_U_INT32_T, 1)])
AC_CHECK_TYPE(u_int16_t, [AC_DEFINE(HAVE_U_INT16_T, 1)])
AC_CHECK_TYPE(u_int8_t, [AC_DEFINE(HAVE_U_INT8_T, 1)])
AC_CHECK_TYPE(uint64_t, [AC_DEFINE(HAVE_UINT64_T, 1)])
AC_CHECK_TYPE(uint32_t, [AC_DEFINE(HAVE_UINT32_T, 1)])
AC_CHECK_TYPE(uint16_t, [AC_DEFINE(HAVE_UINT16_T, 1)])
AC_CHECK_TYPE(uint8_t, [AC_DEFINE(HAVE_UINT8_T, 1)])

AC_MSG_CHECKING([whether to enable 64bit counters])
AC_ARG_ENABLE(64bit,
        [  --enable-64bit                   Enable 64bit counters (default: yes)],
	[
          if test x$enableval = x"yes" ; then
            AC_MSG_RESULT(yes)
            AC_DEFINE(HAVE_64BIT_COUNTERS, 1)
          else
            AC_MSG_RESULT(no)
          fi
        ],
	[
          AC_MSG_RESULT(yes)
	  AC_DEFINE(HAVE_64BIT_COUNTERS, 1)
	  COMPILE_ARGS="${COMPILE_ARGS} '--enable-64bit'"
	]
)

AC_MSG_CHECKING(whether to enable NFLOG support)
AC_ARG_ENABLE(nflog,
  [  --enable-nflog                   Enable NFLOG support (default: no)],
  [ case "$enableval" in
  yes)
    AC_MSG_RESULT(yes)
    PKG_CHECK_MODULES([NFLOG], [libnetfilter_log >= 1], [
      SUPPORTS="${SUPPORTS} nflog"
      USING_NFLOG="yes"
      AC_DEFINE(WITH_NFLOG, 1)
    ])
    ;;
  no)
    AC_MSG_RESULT(no)
    ;;
  esac ],
AC_MSG_RESULT(no))

AC_MSG_CHECKING(whether to link IPv4/IPv6 traffic accounting accounting binaries)
AC_ARG_ENABLE(traffic-bins,
	[  --enable-traffic-bins            Link IPv4/IPv6 traffic accounting binaries (default: yes)],
	[
	  if test x$enableval = x"yes" ; then
	    AC_MSG_RESULT(yes)
	    AC_DEFINE(HAVE_TRAFFIC_BINS, 1)
	    USING_TRAFFIC_BINS="yes"
	  else
	    AC_MSG_RESULT(no)
	  fi
	],
	[
	  AC_MSG_RESULT(yes)
	  AC_DEFINE(HAVE_TRAFFIC_BINS, 1)
	  USING_TRAFFIC_BINS="yes"
	  COMPILE_ARGS="${COMPILE_ARGS} '--enable-traffic-bins'"
	]
)

AC_MSG_CHECKING(whether to link BGP daemon binaries)
AC_ARG_ENABLE(bgp-bins,
        [  --enable-bgp-bins                Link BGP daemon binaries (default: yes)],
        [
          if test x$enableval = x"yes" ; then
            AC_MSG_RESULT(yes)
            AC_DEFINE(HAVE_BGP_BINS, 1)
	    USING_BGP_BINS="yes"
          else
            AC_MSG_RESULT(no)
          fi
        ],
        [
          AC_MSG_RESULT(yes)
          AC_DEFINE(HAVE_BGP_BINS, 1)
	  USING_BGP_BINS="yes"
          COMPILE_ARGS="${COMPILE_ARGS} '--enable-bgp-bins'"
        ]
)

AC_MSG_CHECKING(whether to link BMP daemon binaries)
AC_ARG_ENABLE(bmp-bins,
        [  --enable-bmp-bins                Link BMP daemon binaries (default: yes)],
        [
          if test x$enableval = x"yes" ; then
            AC_MSG_RESULT(yes)
            AC_DEFINE(HAVE_BMP_BINS, 1)
	    USING_BMP_BINS="yes"
          else
            AC_MSG_RESULT(no)
          fi
        ],
        [
          AC_MSG_RESULT(yes)
          AC_DEFINE(HAVE_BMP_BINS, 1)
	  USING_BMP_BINS="yes"
          COMPILE_ARGS="${COMPILE_ARGS} '--enable-bmp-bins'"
        ]
)

AC_MSG_CHECKING(whether to link Streaming Telemetry daemon binaries)
AC_ARG_ENABLE(st-bins,
        [  --enable-st-bins                 Link Streaming Telemetry daemon binaries (default: yes)],
        [
          if test x$enableval = x"yes" ; then
            AC_MSG_RESULT(yes)
            AC_DEFINE(HAVE_ST_BINS, 1)
	    USING_ST_BINS="yes"
          else
            AC_MSG_RESULT(no)
          fi
        ],
        [
          AC_MSG_RESULT(yes)
          AC_DEFINE(HAVE_ST_BINS, 1)
	  USING_ST_BINS="yes"
          COMPILE_ARGS="${COMPILE_ARGS} '--enable-st-bins'"
        ]
)

dnl Checks for library functions.
AC_TYPE_SIGNAL

AC_CHECK_FUNCS([strlcpy vsnprintf setproctitle mallopt tdestroy])

dnl Check for SO_REUSEPORT
AC_CHECK_DECL([SO_REUSEPORT],
	AC_DEFINE(HAVE_SO_REUSEPORT, 1, [Check if kernel supports SO_REUSEPORT]),,
		[
		  #include <sys/types.h>
		  #include <sys/socket.h>
		]
)

dnl final checks
dnl trivial solution to portability issue 
AC_DEFINE_UNQUOTED(COMPILE_ARGS, "$COMPILE_ARGS")
CFLAGS="${CFLAGS} ${INCLUDES}"
INCLUDES=""

echo "
PLATFORM ..... : `uname -m`
OS ........... : `uname -rs` (`uname -n`)
COMPILER ..... : ${CC}
CFLAGS ....... : ${CFLAGS}
LIBS ......... : ${LIBS}
LDFLAGS ...... : ${LDFLAGS}
PLUGINS ...... : ${PLUGINS}
SUPPORTS ..... : ${SUPPORTS}

Now type 'make' to compile the source code.

Wanting to get in touch with other pmacct users?
Join the pmacct mailing-list with an email to pmacct-discussion-subscribe@pmacct.net

Need for documentation and examples?
Start by reading the README.md file

Star, watch or contribute to the project on GitHub:
https://github.com/pmacct/pmacct

"

AC_SUBST([EXTRABIN])
AC_SUBST([PMACCT_CFLAGS])

AM_CONDITIONAL([WITH_MYSQL], [test x"$USING_MYSQL" = x"yes"])
AM_CONDITIONAL([WITH_PGSQL], [test x"$USING_PGSQL" = x"yes"])
AM_CONDITIONAL([WITH_MONGODB], [test x"$USING_MONGODB" = x"yes"])
AM_CONDITIONAL([WITH_SQLITE3], [test x"$USING_SQLITE3" = x"yes"])
AM_CONDITIONAL([WITH_RABBITMQ], [test x"$USING_RABBITMQ" = x"yes"])
AM_CONDITIONAL([WITH_ZMQ], [test x"$USING_ZMQ" = x"yes"])
AM_CONDITIONAL([WITH_KAFKA], [test x"$USING_KAFKA" = x"yes"])
AM_CONDITIONAL([USING_SQL], [test x"$USING_SQL" = x"yes"])
AM_CONDITIONAL([WITH_AVRO], [test x"$USING_AVRO" = x"yes"])
AM_CONDITIONAL([WITH_NDPI], [test x"$USING_NDPI" = x"yes"])
AM_CONDITIONAL([WITH_NFLOG], [test x"$USING_NFLOG" = x"yes"])
AM_CONDITIONAL([USING_TRAFFIC_BINS], [test x"$USING_TRAFFIC_BINS" = x"yes"])
AM_CONDITIONAL([USING_BGP_BINS], [test x"$USING_BGP_BINS" = x"yes"])
AM_CONDITIONAL([USING_BMP_BINS], [test x"$USING_BMP_BINS" = x"yes"])
AM_CONDITIONAL([USING_ST_BINS], [test x"$USING_ST_BINS" = x"yes"])
AC_OUTPUT([ Makefile \
	    src/Makefile src/nfprobe_plugin/Makefile \
	    src/sfprobe_plugin/Makefile src/bgp/Makefile \
	    src/tee_plugin/Makefile src/isis/Makefile \
	    src/bmp/Makefile src/telemetry/Makefile \
	    src/ndpi/Makefile examples/lg/Makefile ])
