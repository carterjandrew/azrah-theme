include(ECMMarkNonGuiExecutable)

set(CMAKE_AUTOMOC ON)

add_executable(kcursorgen)
set_target_properties(kcursorgen PROPERTIES OUTPUT_NAME azrah-kcursorgen)

ecm_mark_nongui_executable(kcursorgen)

target_sources(kcursorgen PRIVATE
    main.cpp
    kcursorgen.cpp
)
target_link_libraries(kcursorgen Qt6::Core Qt6::Svg)

install(TARGETS kcursorgen)
