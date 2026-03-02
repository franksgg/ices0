cmake_minimum_required(VERSION 3.10)
project(ices VERSION 0.6.2 LANGUAGES C)

# Set the source directory for CMake to find custom modules if any
# list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

include(CheckIncludeFiles)
include(CheckFunctionExists)
include(CheckSymbolExists)
include(CheckTypeSize)
include(CheckCSourceCompiles)
include(CMakePushCheckState)
include(GNUInstallDirs)

# Options
option(WITH_XML "Enable libxml2 support" ON)
option(WITH_PYTHON "Enable python scripting support" ON)
option(WITH_PERL "Enable perl scripting support" ON)
option(WITH_LAME "Enable support for reencoding with lame" ON)
option(WITH_VORBIS "Enable support for vorbis transcoding" ON)
option(WITH_FAAD "Enable support for MP4 (AAC) transcoding" ON)
option(WITH_FLAC "Enable support for FLAC transcoding" ON)

# Configure header
set(ICES_ETCDIR "${CMAKE_INSTALL_FULL_SYSCONFDIR}")
set(ICES_MODULEDIR "${CMAKE_INSTALL_FULL_LIBDIR}/ices")

# Checks for headers
check_include_files(errno.h HAVE_ERRNO_H)
check_include_files(fcntl.h HAVE_FCNTL_H)
check_include_files(signal.h HAVE_SIGNAL_H)
check_include_files("sys/signal.h" HAVE_SYS_SIGNAL_H)
check_include_files("sys/socket.h" HAVE_SYS_SOCKET_H)
check_include_files("sys/stat.h" HAVE_SYS_STAT_H)
check_include_files("sys/time.h" HAVE_SYS_TIME_H)
check_include_files("sys/types.h" HAVE_SYS_TYPES_H)
check_include_files(unistd.h HAVE_UNISTD_H)
check_include_files(sys/wait.h HAVE_SYS_WAIT_H)
check_include_files(stdint.h HAVE_STDINT_H)
check_include_files(stdlib.h HAVE_STDLIB_H)
check_include_files(stdio.h HAVE_STDIO_H)
check_include_files(string.h HAVE_STRING_H)
check_include_files(strings.h HAVE_STRINGS_H)
check_include_files(inttypes.h HAVE_INTTYPES_H)

# Checks for types
check_type_size(pid_t PID_T)
if(NOT HAVE_PID_T)
  set(pid_t int)
endif()

check_type_size(size_t SIZE_T)
if(NOT HAVE_SIZE_T)
  set(size_t "unsigned int")
endif()

# Checks for functions
check_function_exists(strftime HAVE_STRFTIME)
check_function_exists(vsnprintf HAVE_VSNPRINTF)
check_function_exists(setsid HAVE_SETSID)
check_function_exists(setlinebuf HAVE_SETLINEBUF)

# Checks for libraries
find_package(PkgConfig REQUIRED)

# Shout (Required)
pkg_check_modules(SHOUT REQUIRED shout)
check_include_files(shout/shout.h HAVE_SHOUT_SHOUT_H)
include_directories(${SHOUT_INCLUDE_DIRS})

set(ICES_LIBS ${SHOUT_LIBRARIES})
set(ICES_CFLAGS ${SHOUT_CFLAGS})

# XML (Optional)
if(WITH_XML)
    pkg_check_modules(XML2 libxml-2.0)
    if(XML2_FOUND)
        set(HAVE_LIBXML 1)
        include_directories(${XML2_INCLUDE_DIRS})
        list(APPEND ICES_LIBS ${XML2_LIBRARIES})
        list(APPEND ICES_CFLAGS ${XML2_CFLAGS})
    endif()
endif()

# Python (Optional)
if(WITH_PYTHON)
    find_package(PythonLibs)
    if(PYTHONLIBS_FOUND)
        set(HAVE_LIBPYTHON 1)
        include_directories(${PYTHON_INCLUDE_DIRS})
        list(APPEND ICES_LIBS ${PYTHON_LIBRARIES})
    endif()
endif()

# Perl (Optional)
if(WITH_PERL)
    find_package(Perl)
    if(PERL_FOUND)
        execute_process(COMMAND ${PERL_EXECUTABLE} -MExtUtils::Embed -e ccopts OUTPUT_VARIABLE PERL_CFLAGS)
        execute_process(COMMAND ${PERL_EXECUTABLE} -MExtUtils::Embed -e ldopts OUTPUT_VARIABLE PERL_LDFLAGS)
        string(STRIP "${PERL_CFLAGS}" PERL_CFLAGS)
        string(STRIP "${PERL_LDFLAGS}" PERL_LDFLAGS)

        # Verify we can actually link against perl (check perl_construct)
        if(PERL_LDFLAGS)
            cmake_push_check_state()
            set(CMAKE_REQUIRED_FLAGS "${PERL_CFLAGS}")
            separate_arguments(PERL_LDFLAGS_LIST UNIX_COMMAND "${PERL_LDFLAGS}")
            set(CMAKE_REQUIRED_LIBRARIES ${PERL_LDFLAGS_LIST})
            check_function_exists(perl_construct HAVE_PERL_CONSTRUCT)
            cmake_pop_check_state()

            if(HAVE_PERL_CONSTRUCT)
                set(HAVE_LIBPERL 1)
                set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${PERL_CFLAGS}")
                list(APPEND ICES_LIBS ${PERL_LDFLAGS_LIST})
            endif()
        endif()
    endif()
endif()

# LAME (Optional)
if(WITH_LAME)
    find_path(LAME_INCLUDE_DIR lame/lame.h)
    find_library(LAME_LIBRARY mp3lame)
    if(LAME_INCLUDE_DIR AND LAME_LIBRARY)
        set(HAVE_LIBLAME 1)
        set(HAVE_LAME_LAME_H 1)
        include_directories(${LAME_INCLUDE_DIR})
        list(APPEND ICES_LIBS ${LAME_LIBRARY})
        
        # Check for lame_decode_exit
        cmake_push_check_state()
        set(CMAKE_REQUIRED_LIBRARIES ${LAME_LIBRARY})
        check_function_exists(lame_decode_exit HAVE_LAME_DECODE_EXIT)
        cmake_pop_check_state()
    else()
        find_path(LAME_INCLUDE_DIR lame.h)
        if(LAME_INCLUDE_DIR AND LAME_LIBRARY)
            set(HAVE_LIBLAME 1)
            include_directories(${LAME_INCLUDE_DIR})
            list(APPEND ICES_LIBS ${LAME_LIBRARY})
        endif()
    endif()
endif()

# Vorbis (Optional) - depends on LAME in autotools
if(WITH_VORBIS AND HAVE_LIBLAME)
    pkg_check_modules(VORBISFILE vorbisfile)
    if(VORBISFILE_FOUND)
        set(HAVE_LIBVORBISFILE 1)
        include_directories(${VORBISFILE_INCLUDE_DIRS})
        list(APPEND ICES_LIBS ${VORBISFILE_LIBRARIES})
        list(APPEND ICES_CFLAGS ${VORBISFILE_CFLAGS})
    endif()
endif()

# FAAD / MP4V2 (Optional) - depends on LAME in autotools
if(WITH_FAAD AND HAVE_LIBLAME)
    find_path(FAAD_INCLUDE_DIR faad.h)
    find_library(FAAD_LIBRARY faad)
    find_library(MP4V2_LIBRARY mp4v2)
    if(FAAD_INCLUDE_DIR AND FAAD_LIBRARY AND MP4V2_LIBRARY)
        set(HAVE_LIBFAAD 1)
        include_directories(${FAAD_INCLUDE_DIR})
        list(APPEND ICES_LIBS ${FAAD_LIBRARY} ${MP4V2_LIBRARY})
    endif()
endif()

# FLAC (Optional) - depends on LAME in autotools
if(WITH_FLAC AND HAVE_LIBLAME)
    pkg_check_modules(FLAC flac)
    if(FLAC_FOUND)
        set(HAVE_LIBFLAC 1)
        include_directories(${FLAC_INCLUDE_DIRS})
        list(APPEND ICES_LIBS ${FLAC_LIBRARIES})
        list(APPEND ICES_CFLAGS ${FLAC_CFLAGS})
    endif()
endif()

# Final LIBS
list(APPEND ICES_LIBS m)

# config.h generation
configure_file(config.h.cmake.in config.h)
include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

add_subdirectory(src/playlist)
add_subdirectory(src)
add_subdirectory(doc)
add_subdirectory(conf)

# Installation of config and docs could be added here
