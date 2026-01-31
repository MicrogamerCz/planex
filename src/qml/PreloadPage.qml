// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.components as PComp

import org.kde.planex

Item {
    id: page

    ColumnLayout {
        anchors {
            left: parent.left
            right: parent.right
            verticalCenter: parent.verticalCenter
            margins: Kirigami.Units.gridUnit * 5
        }
        spacing: Kirigami.Units.largeSpacing //Kirigami.Units.gridUnit

        PComp.Label {
            Layout.alignment: Qt.AlignHCenter
            text: flatpak.preloadMessage
        }
        PComp.ProgressBar {
            Layout.fillWidth: true
            value: flatpak.preloadPercent
            indeterminate: value < 0
        }
        PComp.Button {
            text: "Cancel"
            Layout.alignment: Qt.AlignHCenter
            onClicked: root.close()
        }
    }
}
