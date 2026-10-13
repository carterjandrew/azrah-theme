### configuration plugin
add_definitions(-DTRANSLATION_DOMAIN=\"azrah_style_config\")
set(kstyle_breeze_config_PART_SRCS breezestyleconfig.cpp)

set(kstyle_breeze_config_PART_SRCS ${kstyle_breeze_config_PART_SRCS} breezestyleconfigmodule.cpp)

kconfig_add_kcfg_files(kstyle_breeze_config_PART_SRCS ../breezestyleconfigdata.kcfgc)
set(kstyle_breeze_config_PART_FORMS ui/breezestyleconfig.ui)
ki18n_wrap_ui(kstyle_breeze_config_PART_FORMS_HEADERS ${kstyle_breeze_config_PART_FORMS})

kcoreaddons_add_plugin(azrahstyleconfig SOURCES
    ${kstyle_breeze_config_PART_SRCS}
    ${kstyle_breeze_config_PART_FORMS_HEADERS}
    INSTALL_NAMESPACE "kstyle_config"
)

target_link_libraries(azrahstyleconfig
    PUBLIC
        Qt6::Core
        Qt6::Gui
        Qt6::Widgets
)

if(HAVE_QTDBUS)
    target_link_libraries(azrahstyleconfig
        PUBLIC
            Qt6::DBus
    )
endif()

target_link_libraries(azrahstyleconfig
    PUBLIC
        KF6::CoreAddons
        KF6::ConfigCore
        KF6::ConfigWidgets
        KF6::I18n
)
if(QT_MAJOR_VERSION STREQUAL "6")
    target_link_libraries(azrahstyleconfig
        PUBLIC
    KF6::KCMUtils
)
endif()
kcmutils_generate_desktop_file(azrahstyleconfig)

set(azrah_settings_SOURCES main.cpp)
add_executable(azrah-settings ${azrah_settings_SOURCES})
target_link_libraries(azrah-settings Qt6::Core Qt6::Gui Qt6::Widgets)
target_link_libraries(azrah-settings KF6::I18n KF6::KCMUtils KF6::CoreAddons)

set_target_properties(azrah-settings PROPERTIES OUTPUT_NAME azrah-settings6)

install(TARGETS azrah-settings ${KDE_INSTALL_TARGETS_DEFAULT_ARGS})

# icon
install(FILES sc-apps-breeze-settings.svgz
    DESTINATION ${KDE_INSTALL_ICONDIR}/hicolor/scalable/apps
    RENAME azrah-settings.svgz)

# kcmshell6 < 6.27.0 doesn't know the --smoke-test param, so skip this test for
# now.
# TODO: Drop this when KF6_MIN_VERSION >= 6.27.0
if(KF6KCMUtils_VERSION VERSION_GREATER_EQUAL "6.27.0")
    add_test(NAME azrahstyleconfig_smoketest COMMAND kcmshell6 -style Azrah --smoke-test kstyle_config/azrahstyleconfig)
    set_tests_properties(azrahstyleconfig_smoketest PROPERTIES
        ENVIRONMENT_MODIFICATION "QT_PLUGIN_PATH=path_list_prepend:${CMAKE_BINARY_DIR}/bin;QT_QPA_PLATFORM=set:offscreen"
    )
endif()
