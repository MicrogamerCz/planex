import configparser
import io
import sys

import gi

# from planex.qflatpakfetchworker import QFlatpakWorker
from qflatpakfetchworker import QFlatpakWorker

gi.require_version("AppStream", "1.0")
from gi.repository import AppStream
from PySide6.QtCore import Property, QObject, Qt, QThread, QTimer, Signal, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "org.kde.planex"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class QFlatpakMetadata(QObject):
    preloadChanged = Signal()
    preloadFinished = Signal()
    metadataChanged = Signal()

    def __init__(self, skipReload=True):
        super().__init__()

        self._preload_message = "Refreshing..."
        self._preload_percent = -1  # Any negative progress is indereminate
        self.preloadChanged.emit()
        self._downloading = False

        self.worker: QFlatpakWorker | None = None
        self.app: AppStream.Component | None = None

        self.work_thread = QThread()

        if len(sys.argv) < 2:
            return  # TODO: Print error message

        if sys.argv[1].endswith(".flatpakref"):
            self.flatpakref_init(sys.argv[1], skipReload)

    def flatpakref_init(self, ref: str, skip) -> None:
        if not self.worker:
            self.worker = QFlatpakWorker(ref, skip)

        self.worker.mode = 1
        self.worker.moveToThread(self.work_thread)

        self.work_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.work_thread.quit)

        self.worker.preloadChanged.connect(self.preload_callback)
        self.worker.finished.connect(self.refresh_finished)
        self.worker.finished.connect(self.preloadFinished)

        self.work_thread.start()

    def preload_callback(self, status: str, progress: int):
        self._preload_message = status
        self._preload_percent = progress
        self.preloadChanged.emit()
        return True

    def refresh_finished(self, app_id: str):
        pool = AppStream.Pool()
        pool.load()
        components: AppStream.ComponentBox = pool.get_components_by_id(app_id)  # pyright: ignore[reportAttributeAccessIssue]
        self.app = components.index_safe(0)
        self.metadataChanged.emit()

    @Slot()
    def install(self):
        if not self.worker:
            return

        self._downloading = True
        self.preloadChanged.emit()

        print("I'm downloading!")

        # self.worker.moveToThread(self.thread())
        self.worker.mode = 2
        # self.worker.moveToThread(self.work_thread)

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
