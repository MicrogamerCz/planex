// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import org.kde.plasma.components as PComp
import org.kde.planex

Item {
    ColumnLayout {
        id: dataLayout
        anchors.fill: parent
        anchors.margins: Kirigami.Units.gridUnit

        RowLayout {
            Layout.preferredHeight: Kirigami.Units.gridUnit * 3.75
            Layout.fillWidth: true
            Layout.fillHeight: false
            spacing: Kirigami.Units.largeSpacing

            Image {
                Layout.alignment: Qt.AlignVCenter
                Layout.preferredHeight: 64
                Layout.preferredWidth: 64

                source: flatpak.icon
            }

            ColumnLayout {
                Layout.fillHeight: true

                PComp.Label {
                    font.bold: true
                    font.pixelSize: 22

                    text: flatpak.name
                }

                RowLayout {
                    PComp.Label {
                        text: flatpak.developer
                    }
                    Kirigami.Icon {
                        source: "preflight-verifier"
                        Layout.preferredHeight: 16
                        Layout.preferredWidth: 16
                    }
                }
            }

            Item {
                Layout.fillHeight: true
                Layout.fillWidth: true
                visible: !flatpak.downloading

                RowLayout {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter

                    PComp.Button {
                        text: "Install" // TODO: Update label and function if the app is installed or there's a newer version available
                        onClicked: flatpak.installPackage()
                    }
                    PComp.Button {
                        text: "Close"
                        onClicked: root.close()
                    }
                }
            }
            // PComp.ProgressBar {
            //     Layout.fillWidth: true
            //     Layout.alignment: Qt.AlignVCenter
            //     visible: flatpak.downloading

            //     value: flatpak.preloadPercent
            //     indeterminate: value < 0
            // }
            LoadingProgress {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter

                visible: flatpak.downloading
                showHideButton: true
            }
        }
        Kirigami.Separator {
            Layout.fillWidth: true
        }

        PComp.ScrollView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.maximumWidth: parent.width
            Controls.ScrollBar.horizontal.policy: Controls.ScrollBar.AlwaysOff
            contentWidth: availableWidth

            ColumnLayout {
                width: parent.width
                spacing: Kirigami.Units.largeSpacing

                PComp.Label {
                    font.bold: true
                    font.pixelSize: 14
                    text: flatpak.summary
                }
                PComp.Label {
                    Layout.fillWidth: true
                    text: flatpak.description
                    wrapMode: Text.WordWrap
                }

                Keys.onPressed: event => {
                    print("Pressed");
                    enabled = (event.modifiers & Qt.ShiftModifier);
                }
                MouseArea {
                    id: screenshotSwipeArea
                    Layout.preferredHeight: Kirigami.Units.gridUnit * 25
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    enabled: false

                    /*onWheel: function (wheel) {
                        if (wheel.angleDelta.y > 0 && screenshotSwipe.currentIndex > 0)
                            screenshotSwipe.setCurrentIndex(screenshotSwipe.currentIndex - 1);
                        else if (wheel.angleDelta.y < 0 && screenshotSwipe.currentIndex < (screenshotSwipe.count - 1))
                            screenshotSwipe.setCurrentIndex(screenshotSwipe.currentIndex + 1);
                    }*/

                    PComp.SwipeView {
                        id: screenshotSwipe
                        anchors.fill: parent

                        Repeater {
                            model: flatpak.screenshots

                            Item {
                                Kirigami.LoadingPlaceholder {
                                    anchors.centerIn: parent
                                    visible: showcaseImage.status == Image.Loading
                                    progressBar.indeterminate: true
                                }
                                Image {
                                    id: showcaseImage
                                    anchors.fill: parent
                                    source: modelData
                                    asynchronous: true
                                    fillMode: Image.PreserveAspectFit
                                    cache: true
                                    antialiasing: true
                                }
                            }
                        }
                    }
                }
                PComp.PageIndicator {
                    Layout.alignment: Qt.AlignHCenter
                    count: screenshotSwipe.count
                    currentIndex: screenshotSwipe.currentIndex
                }
            }
        }
    }

    Shortcut {
        sequence: "Left"
        context: Qt.ApplicationShortcut
        onActivated: {
            if (screenshotSwipe.currentIndex > 0)
                screenshotSwipe.setCurrentIndex(screenshotSwipe.currentIndex - 1);
        }
    }
    Shortcut {
        sequence: "Right"
        context: Qt.ApplicationShortcut
        onActivated: {
            if (screenshotSwipe.currentIndex < (screenshotSwipe.count - 1))
                screenshotSwipe.setCurrentIndex(screenshotSwipe.currentIndex + 1);
        }
    }
}
