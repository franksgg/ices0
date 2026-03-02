# CMake build for libplaylist

add_library(playlist STATIC
    playlist.c
    pm_builtin.c
    pm_script.c
    rand.c
)

# Optional modules
if(HAVE_LIBPYTHON)
    target_sources(playlist PRIVATE pm_python.c)
endif()

if(HAVE_LIBPERL)
    target_sources(playlist PRIVATE pm_perl.c)
endif()

target_include_directories(playlist
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_LIST_DIR}
        ${CMAKE_SOURCE_DIR}/src
    PRIVATE
        ${CMAKE_BINARY_DIR}
)

target_compile_definitions(playlist PRIVATE HAVE_CONFIG_H)

# Define ICES_MODULEDIR macro as used in automake
# This is mainly needed for playlist modules resolving
# but it is also defined for the main target explicitly.
