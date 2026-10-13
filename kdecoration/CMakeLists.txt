add_definitions(-DTRANSLATION_DOMAIN="azrah_kwin_deco")

################# includes #################
include_directories(${CMAKE_SOURCE_DIR}/libbreezecommon)
include_directories(${CMAKE_BINARY_DIR}/libbreezecommon)

################# newt target #################
### plugin classes
set(breezedecoration_SRCS
    breezebutton.cpp
    breezedecoration.cpp
    breezesettingsprovider.cpp
    breezeexceptionlist.cpp
)

### build library
kconfig_add_kcfg_files(breezedecoration_SRCS breezesettings.kcfgc)
add_library(azrahdecoration MODULE
    ${breezedecoration_SRCS}
    ${breezedecoration_config_PART_FORMS_HEADERS})

set_target_properties(azrahdecoration PROPERTIES
    OUTPUT_NAME org.kde.azrah
)

target_link_libraries(azrahdecoration
    PRIVATE
        breezecommon6
        Qt6::DBus
        KF6::CoreAddons
        KF6::ConfigGui
        KF6::GuiAddons
        KF6::I18n
        KF6::IconThemes
        KDecoration3::KDecoration
        KF6::ColorScheme
)

if(KDecoration3_VERSION VERSION_GREATER_EQUAL "6.8.0")
    target_compile_definitions(azrahdecoration PRIVATE AZRAH_HAVE_KDECORATION_STYLE)
endif()

install(TARGETS azrahdecoration DESTINATION ${KDE_INSTALL_PLUGINDIR}/${KDECORATION_PLUGIN_DIR})
install(FILES breezesettingsdata.kcfg DESTINATION ${KDE_INSTALL_KCFGDIR} RENAME azrah-decoration.kcfg)

add_subdirectory(config)
