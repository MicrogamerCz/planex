import configparser
import io

import gi

gi.require_version("AppStream", "1.0")
gi.require_version("Flatpak", "1.0")
from gi.repository import AppStream, Flatpak
from PySide6.QtCore import QObject, QThread, Signal, Slot


class QFlatpakWorker(QObject):
    progressChanged = Signal(str, int)
    finished = Signal(str)
    # error = Signal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    @Slot()
    def run(self):
        with io.open(self.file_path) as file:
            data = file.read()
            config = configparser.ConfigParser()
            config.read_string(data)
            remote_name = config.get("Flatpak Ref", "SuggestRemoteName")
            app_id = config.get("Flatpak Ref", "Name")

            # install = Flatpak.Installation.new_system(None)
            # install.update_appstream_full_sync(
            # remote_name, progress=self.callback, cancellable=None
            # )
            # install.update_appstream_sync(remote_name)
            self.callback("", 100, False, None)
            self.finished.emit(app_id)

    def callback(self, status: str, progress: int, estimate: bool, data):
        self.progressChanged.emit(status, progress)
        return True
