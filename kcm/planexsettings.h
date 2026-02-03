// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2025 Micro <microgamercz@proton.me>

#pragma once

#include <KQuickConfigModule>
#include <KQuickManagedConfigModule>
#include "planexconfig.h"

class PlanexSettings : public KQuickManagedConfigModule
{
    Q_OBJECT

    Q_PROPERTY(PlanexConfig *config READ config CONSTANT)

    public:
        PlanexSettings(QObject *parent, const KPluginMetaData &data);

    PlanexConfig *config() const;

    private:
        PlanexConfig *m_config;
};
