cmake_minimum_required(VERSION 3.15...4.0)
set(CMAKE_POLICY_VERSION_MINIMUM 3.5)

project(pylottie-convert LANGUAGES CXX C)


set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(RLOTTIE_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(RLOTTIE_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(RLOTTIE_BUILD_SHARED OFF CACHE BOOL "" FORCE)
set(RLOTTIE_BUILD_STATIC ON CACHE BOOL "" FORCE)

set(PYBIND11_LTO_CXX_FLAGS "" CACHE STRING "" FORCE)
set(HAS_FLTO_AUTO FALSE CACHE BOOL "" FORCE)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION OFF CACHE BOOL "" FORCE)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG QUIET)

add_subdirectory(rlottie)

pybind11_add_module(_pylottie MODULE NO_EXTRAS src/bindings.cpp src/lottie_engine.cpp)
target_link_libraries(_pylottie PRIVATE rlottie)

if(UNIX AND NOT APPLE)
    string(REPLACE "-Wl,--no-undefined" "" CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS}")
    string(REPLACE "-Wl,--no-undefined" "" CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS}")

    get_target_property(RLOTTIE_LIBS rlottie INTERFACE_LINK_LIBRARIES)
    if(RLOTTIE_LIBS)
        list(REMOVE_ITEM RLOTTIE_LIBS "-Wl,--no-undefined")
        set_target_properties(rlottie PROPERTIES INTERFACE_LINK_LIBRARIES "${RLOTTIE_LIBS}")
    endif()

    target_link_options(_pylottie PRIVATE
            "-Wl,--allow-shlib-undefined"
            "-Wl,--unresolved-symbols=ignore-all"
    )

    set_target_properties(_pylottie PROPERTIES LINK_FLAGS "-Wl,--allow-shlib-undefined")
endif()
install(TARGETS _pylottie DESTINATION pylottie_convert)