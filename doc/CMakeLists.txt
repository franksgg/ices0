# Installation for documentation

set(edit_sed_script
    "s|@sysconfdir@|${CMAKE_INSTALL_FULL_SYSCONFDIR}|g; \
     s|@moddir@|${ICES_MODULEDIR}|g; \
     s|@VERSION@|${PROJECT_VERSION}|g; \
     s|@PACKAGE@|${PROJECT_NAME}|g"
)

# In CMake we can use configure_file for simple @VAR@ replacements 
# if the input file uses that syntax.
# doc/ices.1.in uses @sysconfdir@, @moddir@, @VERSION@, @PACKAGE@.
# However, it might be easier to just use configure_file if we define those variables.

set(sysconfdir ${CMAKE_INSTALL_FULL_SYSCONFDIR})
set(moddir ${ICES_MODULEDIR})
set(VERSION ${PROJECT_VERSION})
set(PACKAGE ${PROJECT_NAME})

configure_file(ices.1.in ices.1 @ONLY)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/ices.1 DESTINATION ${CMAKE_INSTALL_MANDIR}/man1)
install(FILES icesmanual.html DESTINATION ${CMAKE_INSTALL_DOCDIR})
