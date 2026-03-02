# Installation for configuration files

# The Makefile.am says:
# sysconf_DATA = ices.conf.dist
# mod_DATA = ices.py.dist ices.pm.dist ices.sh.dist
# and ices.conf.dist is usually generated from ices.conf.dist.in (but Makefile.am doesn't show it explicitly)
# actually ices.conf.dist is NOT in the file list, but ices.conf.dist.in is.

# Wait, in the project structure I see:
# conf/ices.conf.dist.in
# but Makefile.am says sysconf_DATA = ices.conf.dist

# Let's check if ices.conf.dist exists or if it's generated.
# Usually configure.ac handles it:
# AC_CONFIG_FILES([... conf/ices.conf.dist ...])

set(sysconfdir ${CMAKE_INSTALL_FULL_SYSCONFDIR})
set(moddir ${ICES_MODULEDIR})
set(VERSION ${PROJECT_VERSION})
set(PACKAGE ${PROJECT_NAME})

configure_file(ices.conf.dist.in ices.conf.dist @ONLY)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/ices.conf.dist DESTINATION ${CMAKE_INSTALL_SYSCONFDIR})

install(FILES ices.py.dist ices.pm.dist ices.sh.dist DESTINATION ${ICES_MODULEDIR})
