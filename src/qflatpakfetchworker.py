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
        self.mode = 0  # 0 is nothing, 1 is refresh, 2 is install
        self.install: Flatpak.Installation | None = None

    def callback(self, status: str, progress: int, estimate: bool, data):
        self.preloadChanged.emit(status, progress)
        return True

    def refreshAppstream(self):
        with io.open(self.file_path) as file:
            data = file.read()
            config = configparser.ConfigParser()
            config.read_string(data)
            self.app_id = config.get("Flatpak Ref", "Name")
            self.remote_name = config.get("Flatpak Ref", "SuggestRemoteName")
            self.is_runtime = config.get("Flatpak Ref", "IsRuntime") == "true"
            self.branch = config.get("Flatpak Ref", "Branch")

            self.install = Flatpak.Installation.new_system(None)
            if not self.skipReload:
                self.install.update_appstream_full_sync(
                    self.remote_name, progress=self.callback, cancellable=None
                )
            self.finished.emit(self.app_id)

    @Slot()
    def run(self):
        print("Started to run:", self.mode)
        match self.mode:
            case 0:
                return
            case 1:
                self.refreshAppstream()
            case 2:
                if not self.install:
                    return
                print("installing?")
                self.install.install(
                    self.remote_name,
                    Flatpak.RefKind.RUNTIME if self.is_runtime else Flatpak.RefKind.APP,
                    self.app_id,
                    branch=self.branch,
                    progress=self.callback,
                )
