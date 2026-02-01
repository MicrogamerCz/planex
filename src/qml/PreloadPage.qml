// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

import QtQuick
import org.kde.kirigami as Kirigami

Item {
    id: page

    LoadingProgress {
        anchors {
            left: parent.left
            right: parent.right
            verticalCenter: parent.verticalCenter
            margins: Kirigami.Units.gridUnit * 5
        }
    }
}
