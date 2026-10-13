find_package(Python3 REQUIRED COMPONENTS Interpreter)
include(KDEInstallDirs)

set(AZRAH_PLASMA_THEME_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/azrah")
set(AZRAH_PLASMA_THEME_ASSETS
    widgets/background.svg
    solid/widgets/background.svg
    translucent/widgets/background.svg
    widgets/button.svg
    widgets/lineedit.svg
    widgets/listitem.svg
    widgets/viewitem.svg
    widgets/tabbar.svg
    widgets/scrollbar.svg
    widgets/slider.svg
    widgets/switch.svg
    widgets/checkmarks.svg
    widgets/radiobutton.svg
    widgets/tooltip.svg
)

set(AZRAH_PLASMA_THEME_OUTPUTS)
foreach(asset IN LISTS AZRAH_PLASMA_THEME_ASSETS)
    list(APPEND AZRAH_PLASMA_THEME_OUTPUTS "${AZRAH_PLASMA_THEME_BUILD_DIR}/${asset}")
endforeach()

add_custom_command(
    OUTPUT ${AZRAH_PLASMA_THEME_OUTPUTS}
    COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/generate_theme.py"
            --output "${AZRAH_PLASMA_THEME_BUILD_DIR}"
            --popup-border-width "${AZRAH_PLASMA_POPUP_BORDER_WIDTH}"
    DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/generate_theme.py"
    COMMENT "Generating Azrah Plasma theme assets"
    VERBATIM
)
add_custom_target(azrah-plasma-theme ALL DEPENDS ${AZRAH_PLASMA_THEME_OUTPUTS})

configure_file(metadata.json "${AZRAH_PLASMA_THEME_BUILD_DIR}/metadata.json" COPYONLY)

set(AZRAH_PLASMA_THEME_INSTALL_DIR "${KDE_INSTALL_DATADIR}/plasma/desktoptheme/azrah")
install(FILES "${AZRAH_PLASMA_THEME_BUILD_DIR}/metadata.json"
        DESTINATION "${AZRAH_PLASMA_THEME_INSTALL_DIR}")
foreach(asset IN LISTS AZRAH_PLASMA_THEME_ASSETS)
    get_filename_component(asset_dir "${asset}" DIRECTORY)
    install(FILES "${AZRAH_PLASMA_THEME_BUILD_DIR}/${asset}"
            DESTINATION "${AZRAH_PLASMA_THEME_INSTALL_DIR}/${asset_dir}")
endforeach()

if(BUILD_TESTING)
    add_test(
        NAME azrah-plasma-theme-contract
        COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/test_theme.py"
                --theme "${AZRAH_PLASMA_THEME_BUILD_DIR}"
                --popup-border-width "${AZRAH_PLASMA_POPUP_BORDER_WIDTH}"
    )
    set_tests_properties(azrah-plasma-theme-contract PROPERTIES
        DEPENDS azrah-plasma-theme
    )
endif()
