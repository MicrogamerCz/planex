# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Micro <microgamercz@proton.me>

import subprocess

import gi
from PySide6.QtCore import QObject, Signal

gi.require_version("Flatpak", "1.0")
from gi.repository import Flatpak


class QFlatpakWorker(QObject):
    progress = Signal(str, int)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self.flatpak_ref = self.app_id = self.remote_name = self.branch = ""
        self.is_runtime = False

        self.install = Flatpak.Installation.new_system(None)

    def callback(self, status: str, progress: int, estimate: bool, data):
        self.progress.emit(status, progress)
        return True

    def sync(self):
        self.install.update_appstream_full_sync(
            self.remote_name,
            progress=self.callback,  # pyright: ignore[reportArgumentType]
            cancellable=None,
        )
        self.finished.emit()

    def install_progress(
        self,
        transaction: Flatpak.Transaction,
        operation: Flatpak.TransactionOperation,
        progress: Flatpak.TransactionProgress,
    ):
        def on_progress_changed(p, *args):
            self.progress.emit(progress.get_status(), progress.get_progress())

        progress.connect("changed", on_progress_changed)

    def install_flatpak(self):
        transaction = Flatpak.Transaction.new_for_installation(self.install)
        transaction.add_install(
            self.remote_name,
            f"app/{self.app_id}/x86_64/stable",
        )
        transaction.connect("new-operation", self.install_progress)
        transaction.run()

        subprocess.Popen(
            ["flatpak", "run", self.app_id],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )

        self.finished.emit()
