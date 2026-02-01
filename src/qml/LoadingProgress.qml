// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

import QtQuick
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import org.kde.plasma.components as PComp
import org.kde.planex

ColumnLayout {
    id: progress
    spacing: Kirigami.Units.largeSpacing

    property bool showHideButton: false

    PComp.Label {
        Layout.alignment: Qt.AlignHCenter
        text: flatpak.preloadMessage
    }
    PComp.ProgressBar {
        Layout.fillWidth: true
        value: flatpak.preloadPercent
        indeterminate: value < 0
        to: 100
    }

    RowLayout {
        Layout.alignment: Qt.AlignHCenter
        spacing: Kirigami.Units.mediumSpacing

        PComp.Button {
            visible: progress.showHideButton
            text: "Hide"
            // onClicked: root.close()
        }
        PComp.Button {
            text: "Cancel"
            onClicked: root.close()
        }
    }
}
