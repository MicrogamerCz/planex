import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami
import org.kde.plasma.core as PCore
import org.kde.plasma.components as PComp

import org.kde.planex

// Kirigami.ApplicationWindow {
PCore.Window {
    id: root

    title: qsTr("Simple Markdown viewer")

    minimumWidth: Kirigami.Units.gridUnit * 50
    maximumWidth: minimumWidth
    minimumHeight: Kirigami.Units.gridUnit * 35
    maximumHeight: minimumHeight
    visible: true

    // pageStack.initialPage: initPage

    QFlatpakMetadata {
        id: flatpak
    }

    PComp.Page {
        anchors.fill: parent
        ColumnLayout {
            anchors {
                left: parent.left
                right: parent.right
                verticalCenter: parent.verticalCenter
            }

            PComp.Label {
                text: flatpak.progressMessage
            }
            PComp.ProgressBar {
                Layout.fillWidth: true
                value: flatpak.progressPercent
                indeterminate: value < 0
            }

            opacity: (flatpak.progressPercent == 100) ? 0 : 1
            Behavior on opacity {
                NumberAnimation {}
            }
        }

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
                    Layout.fillWidth: true
                }

                PComp.Button {
                    Layout.alignment: Qt.AlignVCenter
                    text: "Install"
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

                    PComp.SwipeView {
                        id: screenshotSwipe
                        Layout.preferredHeight: Kirigami.Units.gridUnit * 25
                        Layout.fillWidth: true
                        Layout.fillHeight: true

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
                    PComp.PageIndicator {
                        Layout.alignment: Qt.AlignHCenter
                        count: screenshotSwipe.count
                        currentIndex: screenshotSwipe.currentIndex
                    }
                }
            }

            opacity: (flatpak.progressPercent == 100) ? 1 : 0
            Behavior on opacity {
                NumberAnimation {}
            }
        }
    }
}
