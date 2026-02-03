# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

kcmutils_add_qml_kcm(kcm_planex)

# kconfig_target_kcfg_file(kcm_planex
    # FILE planexconfig.kcfg
    # CONF_FILE planexconfig.kcfgc
    # CLASS_NAME PlanexConfig
# )
kconfig_add_kcfg_files(kcm_planex GENERATE_MOC planexconfig.kcfgc)

target_sources(kcm_planex PRIVATE
   planexsettings.cpp
   planexsettings.h
)
target_link_libraries(kcm_planex PRIVATE
    Qt::Quick
    KF6::CoreAddons
    KF6::KCMUtils
    KF6::KCMUtilsQuick
    KF6::I18n
)
