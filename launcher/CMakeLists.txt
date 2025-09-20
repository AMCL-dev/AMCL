cmake_minimum_required(VERSION 4.0)
project(AMCLLauncher)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(OUTPUT_DIR ${CMAKE_SOURCE_DIR}/../dist/amcl)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${OUTPUT_DIR})

file(MAKE_DIRECTORY ${OUTPUT_DIR})


if(WIN32)
    add_executable(AMCL WIN32
            main.cpp
            platform.cpp
    )

    set_target_properties(AMCL PROPERTIES
            LINK_FLAGS "/SUBSYSTEM:WINDOWS"
    )
else()
    add_executable(AMCL
            main.cpp
            platform.cpp
    )
endif()

if(WIN32)
    find_package(unofficial-wintoast CONFIG REQUIRED)
    target_link_libraries(AMCL PRIVATE unofficial::wintoast::wintoast)
endif()

if(APPLE)
    find_library(COREFOUNDATION_LIBRARY CoreFoundation)
    target_link_libraries(AMCL PRIVATE ${COREFOUNDATION_LIBRARY})
endif()

target_include_directories(AMCL PRIVATE
        include
)

target_link_libraries(AMCL PRIVATE
        $<$<PLATFORM_ID:Windows>:user32>
        $<$<PLATFORM_ID:Linux>:X11>
)

if(MSVC)
    target_compile_options(AMCL PRIVATE /utf-8)
else()
    target_compile_options(AMCL PRIVATE -finput-charset=UTF-8)
endif()