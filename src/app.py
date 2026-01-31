#!/usr/bin/env python3

import os
import signal
import sys

from planex.qflatpakmetadata import QFlatpakMetadata  # noqa: F401
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

os.environ["QT_WAYLAND_SHELL_INTEGRATION"] = "layer-shell"


def main():
    if len(sys.argv) < 2:
        return

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Needed to close the app with Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    base_path = os.path.abspath(os.path.dirname(__file__))
    url = QUrl(f"file://{base_path}/qml/Main.qml")
    engine.load(url)

    if len(engine.rootObjects()) == 0:
        quit()

    app.exec()


if __name__ == "__main__":
    main()
