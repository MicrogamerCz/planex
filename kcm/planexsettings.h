// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2025 Micro <microgamercz@proton.me>

#pragma once

#include <KQuickConfigModule>

class PlanexSettings : public KQuickConfigModule
{
    Q_OBJECT
    public:
        PlanexSettings(QObject *parent, const KPluginMetaData &data);
};
