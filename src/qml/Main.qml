// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.plasma.core as PCore
import org.kde.plasma.components as PComp
import org.kde.layershell as LS
import org.kde.notification
import org.kde.planex

PCore.Window {
    id: root

    LS.Window.layer: LS.Window.LayerTop
    LS.Window.anchors: LS.Window.AnchorNone
    visible: true

    title: qsTr("Planex")

    minimumWidth: Kirigami.Units.gridUnit * 50
    maximumWidth: minimumWidth
    minimumHeight: Kirigami.Units.gridUnit * 35
    maximumHeight: minimumHeight

    QFlatpakMetadata {
        id: flatpak

        onLoaded: stack.currentIndex++
        onFinished: stopInstall()
    }

    PComp.Page {
        anchors.fill: parent
        PComp.SwipeView {
            id: stack
            anchors.fill: parent
            interactive: false

            PreloadPage {}
            PackagePage {}
        }
    }

    Shortcut {
        sequences: [StandardKey.Quit, "Esc"]
        context: Qt.ApplicationShortcut
        onActivated: {
            if (flatpak.downloading) {
                root.hide();
                notification.sendEvent();
            } else
                root.close();
        }
    }

    Notification {
        id: notification
        componentName: "planex"
        eventId: "flatpakInstall"
        title: "Installing package"
        text: `${flatpak.preloadMessage}\n<b>${prettyPrintProgress()}</b>`
        iconName: "flatpak-discover"
        flags: Notification.Persistent
        urgency: Notification.HighUrgency
        onClosed: root.show()

        actions: [
            NotificationAction {
                label: "Open"
                onActivated: notification.close()
            },
            NotificationAction {
                label: "Cancel"
                onActivated: flatpak.stopInstall()
            }
        ]

        function prettyPrintProgress() {
            if (flatpak.preloadPercent < 0)
                return "";

            const percent = flatpak.preloadPercent;
            let str = "# ".repeat(percent / 10);
            str += ((percent % 10 + 1) % 10);
            str += " _".repeat((100 - percent) / 10);
            str += ` (${flatpak.preloadPercent}%)`;
            return str;
        }
    }
}
