add_library(
    ActsExamplesDetectorFaser2Telescope
    SHARED
    src/Faser2TelescopeDetector.cpp
    src/Faser2TelescopeDetectorElement.cpp
    src/BuildFaser2TelescopeDetector.cpp
)
target_include_directories(
    ActsExamplesDetectorFaser2Telescope
    PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
target_link_libraries(
    ActsExamplesDetectorFaser2Telescope
    PUBLIC ActsCore ActsExamplesFramework
)

install(
    TARGETS ActsExamplesDetectorFaser2Telescope
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

# Add the include directory for Faser2TelescopeDetector
target_include_directories(
    ActsExamplesDetectorFaser2Telescope
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include
)