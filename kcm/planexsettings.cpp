// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2025 Micro <microgamercz@proton.me>

#include "planexsettings.h"
#include "planexconfig.h"

#include <KPluginFactory>
#include <qobject.h>
#include <qqml.h>

K_PLUGIN_CLASS_WITH_JSON(PlanexSettings, "kcm_planex.json")

PlanexSettings::PlanexSettings(QObject *parent, const KPluginMetaData &data)
    : KQuickManagedConfigModule(parent, data), m_config(new PlanexConfig(this))
{
    // load();
    registerSettings(m_config);
    // qmlRegisterAnonymousType<PlanexConfig>("org.kde.planex.private", 1);
    // qmlRegisterUncreatableType<PlanexConfig>("org.kde.planex.private", 1, 0, "Config", QStringLiteral("None"));

    setButtons(Help | Apply | Default);
}
PlanexConfig *PlanexSettings::config() const {
    return m_config;
}

#include "planexsettings.moc"
