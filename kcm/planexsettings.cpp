// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2025 Micro <microgamercz@proton.me>

#include "planexsettings.h"

#include <KPluginFactory>

K_PLUGIN_CLASS_WITH_JSON(PlanexSettings, "kcm_planex.json")

PlanexSettings::PlanexSettings(QObject *parent, const KPluginMetaData &data)
    : KQuickConfigModule(parent, data)
{
    setButtons(Help | Apply | Default);
}

#include "planexsettings.moc"
