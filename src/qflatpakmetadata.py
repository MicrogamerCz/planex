import sys

import gi

from qflatpakfetchworker import QFlatpakWorker

gi.require_version("AppStream", "1.0")
gi.require_version("Flatpak", "1.0")
from gi.repository import AppStream, Flatpak
from PySide6.QtCore import Property, QObject, QThread, Signal, Slot
from PySide6.QtQml import QmlElement, QmlSingleton

QML_IMPORT_NAME = "org.kde.planex"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class QFlatpakMetadata(QObject):
    progressChanged = Signal()
    metadataChanged = Signal()

    def __init__(self):
        super().__init__()

        self._progress_message = "Refreshing..."
        self._progress_percent = -1  # Any negative progress is indereminate
        self.progressChanged.emit()

        self.app: AppStream.Component | None = None

        self.work_thread = QThread()

        if len(sys.argv) < 2:
            return  # TODO: Print error message

        if sys.argv[1].endswith(".flatpakref"):
            self.flatpakref_init(sys.argv[1])

        super().__init__()

    def flatpakref_init(self, ref: str) -> None:
        self.worker = QFlatpakWorker(ref)

        self.worker.moveToThread(self.work_thread)

        self.work_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.work_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.work_thread.finished.connect(self.work_thread.deleteLater)

        self.worker.progressChanged.connect(self.progress_callback)
        self.worker.finished.connect(self.refresh_finished)

        self.work_thread.start()

    def progress_callback(self, status: str, progress: int):
        self._progress_message = status
        self._progress_percent = progress
        self.progressChanged.emit()
        return True

    def refresh_finished(self, app_id: str):
        pool = AppStream.Pool()
        pool.load()
        components: AppStream.ComponentBox = pool.get_components_by_id(app_id)  # pyright: ignore[reportAttributeAccessIssue]
        self.app = components.index_safe(0)
        self.metadataChanged.emit()

    @Property(str, notify=progressChanged)
    def progressMessage(self):
        return self._progress_message

    @Property(int, notify=progressChanged)
    def progressPercent(self):
        return self._progress_percent

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

    # @Slot(result=str)
    # def mdFormat(self):
    # return ""
