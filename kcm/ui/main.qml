// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2025 Micro <microgamercz@proton.me>

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCMUtils

KCMUtils.SimpleKCM {
    // Appstream referesh options - never (only when necessary), every N days/weeks, every boot
    Kirigami.FormLayout {
        Controls.ButtonGroup {
            id: asrGroup
        }

        RowLayout {
            id: neverRL
            Kirigami.FormData.label: "Appstream refresh frequency:"

            Controls.RadioButton {
                text: "Never"
                checked: kcm.config.frequencyType == 0
                onClicked: kcm.config.frequencyType = 0

                Controls.ButtonGroup.group: asrGroup
            }

            Kirigami.ContextualHelpButton {
                toolTipText: "Refreshes appstream metadata when you open a newly released flatpak. Can lead to outdated metainfo and delays preview"
            }
        }
        RowLayout {
            Controls.RadioButton {
                text: "Every session start"
                checked: kcm.config.frequencyType == 1
                onClicked: kcm.config.frequencyType = 1

                Controls.ButtonGroup.group: asrGroup
            }
        }
        Controls.RadioButton {
            text: "Regularly"
            checked: kcm.config.frequencyType == 2
            onClicked: kcm.config.frequencyType = 2

            Controls.ButtonGroup.group: asrGroup
        }

        Kirigami.Separator {
            Layout.fillWidth: true
        }

        ColumnLayout {
            Kirigami.FormData.label: "Refresh frequency:"
            Kirigami.FormData.buddyFor: intervalSpin
            visible: kcm.config.frequencyType == 2

            Controls.SpinBox {
                id: intervalSpin
                from: 1
                to: 52

                onValueModified: kcm.config.frequency = value
            }

            ColumnLayout {
                id: unitLayout

                Controls.RadioButton {
                    text: `Every ${intervalSpin.value > 1 ? intervalSpin.value : ""} day${intervalSpin.value > 1 ? "s" : ""}`
                    enabled: intervalSpin.value <= 31
                    checked: kcm.config.frequencyUnit == 0
                    onClicked: kcm.config.frequencyUnit = 0
                }
                Controls.RadioButton {
                    text: `Every ${intervalSpin.value > 1 ? intervalSpin.value : ""} week${intervalSpin.value > 1 ? "s" : ""}`
                    enabled: intervalSpin.value <= 52
                    checked: kcm.config.frequencyUnit == 1
                    onClicked: kcm.config.frequencyUnit = 1
                }
                Controls.RadioButton {
                    text: `Every ${intervalSpin.value > 1 ? intervalSpin.value : ""} month${intervalSpin.value > 1 ? "s" : ""}`
                    enabled: intervalSpin.value <= 12
                    checked: kcm.config.frequencyUnit == 2
                    onClicked: kcm.config.frequencyUnit = 2
                }
            }

            Kirigami.Separator {
                Layout.fillWidth: true
            }
        }

        Controls.Label {
            text: "Depends on user-space systemd service. May not work on non-systemd environments"
        }
    }
}
