# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

import configparser
import io
import sys

import gi
from planex.qflatpakfetchworker import QFlatpakWorker

# from qflatpakfetchworker import QFlatpakWorker

gi.require_version("AppStream", "1.0")
from gi.repository import AppStream
from PySide6.QtCore import Property, QObject, Qt, QThread, QTimer, Signal, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "org.kde.planex"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class QFlatpakMetadata(QObject):
    preloadChanged = Signal()
    metadataChanged = Signal()
    loaded = Signal()
    finished = Signal()

    def __init__(self, skipReload=True):
        super().__init__()

        self._preload_message = "Refreshing..."
        self._preload_percent = -1  # Any negative progress is indereminate
        self.preloadChanged.emit()
        self._downloading = False

        self.loaded.connect(lambda: print("loaded"))

        self.worker: QFlatpakWorker = QFlatpakWorker()
        self.app: AppStream.Component | None = None

        self.work_thread = QThread()

        if sys.argv[1].endswith(".flatpakref"):
            with io.open(sys.argv[1]) as file:
                data = file.read()
                self.worker.flatpak_ref = data

                self.config = configparser.ConfigParser()
                self.config.read_string(data)

                self.app_id = self.config.get("Flatpak Ref", "Name")
                self.prepare_worker()

                if not self.fetch_component():
                    self.reload()

    def prepare_worker(self):
        self.worker.progress.connect(self.preload_callback)
        self.worker.finished.connect(self.work_thread.quit)

        self.worker.app_id = self.app_id
        self.worker.remote_name = self.config.get("Flatpak Ref", "SuggestRemoteName")
        self.worker.is_runtime = self.config.get("Flatpak Ref", "IsRuntime") == "true"
        self.worker.branch = self.config.get("Flatpak Ref", "Branch")

        self.worker.moveToThread(self.work_thread)

    def fetch_component(self) -> bool:
        pool = AppStream.Pool()
        pool.load()
        components: AppStream.ComponentBox = pool.get_components_by_id(self.app_id)  # pyright: ignore[reportAttributeAccessIssue]

        if components.get_size() == 0:
            return False

        self.app = components.index_safe(0)
        QTimer.singleShot(0, self.loaded.emit)
        QTimer.singleShot(0, self.metadataChanged.emit)

        return True

    def preload_callback(self, status: str, progress: int):
        self._preload_message = status
        self._preload_percent = progress
        self.preloadChanged.emit()
        return True

    def reload(self) -> None:
        self.work_thread.started.connect(
            self.worker.sync, Qt.ConnectionType.SingleShotConnection
        )
        self.worker.finished.connect(
            self.fetch_component, Qt.ConnectionType.SingleShotConnection
        )

        self.work_thread.start()

    @Slot()
    def installPackage(self):
        self._downloading = True
        self.preloadChanged.emit()

        self.work_thread.started.connect(
            self.worker.install_flatpak, Qt.ConnectionType.SingleShotConnection
        )
        self.worker.finished.connect(
            self.finished, Qt.ConnectionType.SingleShotConnection
        )

        self.work_thread.start()

    @Property(bool, notify=preloadChanged)
    def downloading(self):
        return self._downloading

    @Property(str, notify=preloadChanged)
    def preloadMessage(self):
        return self._preload_message

    @Property(int, notify=preloadChanged)
    def preloadPercent(self):
        return self._preload_percent

    @Property(str, notify=metadataChanged)
    def icon(self):
        if self.app:
            return self.app.get_icons()[0].get_url()
        else:
            return ""

    @Property(str, notify=metadataChanged)
    def name(self):
        if self.app:
            return self.app.get_name()
        else:
            return ""

    @Property(str, notify=metadataChanged)
    def developer(self):
        if self.app:
            dev = self.app.get_developer()  # pyright: ignore[reportAttributeAccessIssue]
            return dev.get_name()
        else:
            return ""

    @Property(bool, notify=metadataChanged)
    def verifiedDeveloper(self):
        if self.app:
            return self.app.get_custom_value("flathub::verification::verified")
        else:
            return False

    @Property(str, notify=metadataChanged)
    def summary(self):
        if self.app:
            return self.app.get_summary()
        else:
            return ""

    @Property(str, notify=metadataChanged)
    def description(self):
        if self.app:
            return self.app.get_description()
        else:
            return ""

    @Property(list, notify=metadataChanged)
    def screenshots(self):
        if self.app:
            images = []
            _screenshots = self.app.get_screenshots_all()  # pyright: ignore[reportAttributeAccessIssue]
            for screen in _screenshots:
                images.append(screen.get_images_all()[0].get_url())
            return images
        else:
            return ""
