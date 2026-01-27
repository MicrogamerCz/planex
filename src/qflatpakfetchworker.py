import configparser
import io

import gi
from gi.repository.Gio import Cancellable

gi.require_version("AppStream", "1.0")
gi.require_version("Flatpak", "1.0")
from gi.repository import Flatpak
from PySide6.QtCore import QObject, Signal, Slot


class QFlatpakWorker(QObject):
    preloadChanged = Signal(str, int)
    finished = Signal(str)

    def __init__(self, file_path, skipReload):
        super().__init__()
        self.file_path = file_path
        self.skipReload = skipReload

    @Slot()
    def run(self):
        with io.open(self.file_path) as file:
            data = file.read()
            config = configparser.ConfigParser()
            config.read_string(data)
            remote_name = config.get("Flatpak Ref", "SuggestRemoteName")
            app_id = config.get("Flatpak Ref", "Name")

            if not self.skipReload:
                install = Flatpak.Installation.new_system(None)
                install.update_appstream_full_sync(
                    remote_name, progress=self.callback, cancellable=None
                )
            self.finished.emit(app_id)

    def callback(self, status: str, progress: int, estimate: bool, data):
        self.preloadChanged.emit(status, progress)
        return True
