import QtQuick
import org.kde.kirigami as Kirigami
import org.kde.plasma.core as PCore
import org.kde.plasma.components as PComp
import org.kde.layershell as LS

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
        onFinished: root.close()
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
        onActivated: root.close()
    }
}
