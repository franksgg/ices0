# CMake build for ices executable

set(ICES_COMMON_SOURCES
    ices.c
    log.c
    setup.c
    stream.c
    util.c
    mp3.c
    cue.c
    metadata.c
    id3.c
    signals.c
    crossfade.c
    replaygain.c
)

set(ICES_OPTIONAL_SOURCES)

if(HAVE_LIBXML)
    list(APPEND ICES_OPTIONAL_SOURCES ices_config.c)
endif()

if(HAVE_LIBLAME)
    list(APPEND ICES_OPTIONAL_SOURCES reencode.c)
endif()

if(HAVE_LIBVORBISFILE)
    list(APPEND ICES_OPTIONAL_SOURCES in_vorbis.c)
endif()

if(HAVE_LIBFAAD)
    list(APPEND ICES_OPTIONAL_SOURCES in_mp4.c)
endif()

if(HAVE_LIBFLAC)
    list(APPEND ICES_OPTIONAL_SOURCES in_flac.c)
endif()

add_executable(ices
    ${ICES_COMMON_SOURCES}
    ${ICES_OPTIONAL_SOURCES}
)

# Definitions from automake
# ICES_ETCDIR and ICES_MODULEDIR are used in code
# We pass full install paths defined in the top-level CMakeLists

target_compile_definitions(ices PRIVATE
    HAVE_CONFIG_H
    ICES_ETCDIR="${ICES_ETCDIR}"
    ICES_MODULEDIR="${ICES_MODULEDIR}"
)

# Includes

target_include_directories(ices PRIVATE
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_BINARY_DIR}
    ${SHOUT_INCLUDE_DIRS}
    ${XML2_INCLUDE_DIRS}
    ${VORBISFILE_INCLUDE_DIRS}
    ${FLAC_INCLUDE_DIRS}
)

# Link against playlist and detected libs

target_link_libraries(ices PRIVATE playlist ${ICES_LIBS})

# Install
install(TARGETS ices RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
