# This file is part of MidiWatch.
# Copyright (C) 2025 cam84
#
# MidiWatch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MidiWatch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MidiWatch. If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)

from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt, QUrl, Slot

from midiwatch.gui.dialogs import AboutDialog
from midiwatch.constants import APP_NAME, APP_VERSION


class FooterWidget(QWidget):
    """Footer widget displaying version info and update notifications."""

    def __init__(self, parent=None):
        """Initialize the footer widget."""
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setObjectName("footer")
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Create and arrange child widgets."""
        version_lbl = QLabel(f"{APP_NAME} v{APP_VERSION}")

        # Separator 1 (hidden by default, visible if updated)
        self._separator_update = QLabel("/")
        self._separator_update.hide()

        self._update_btn = QPushButton()
        self._update_btn.setObjectName("updateNotification")
        self._update_btn.setFlat(True)
        self._update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_btn.hide()

        separator_lbl = QLabel("/")

        self._about_btn = QPushButton("about")
        self._about_btn.setObjectName("aboutButton")
        self._about_btn.setFlat(True)
        self._about_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout_hbox = QHBoxLayout()
        layout_hbox.setContentsMargins(0, 5, 0, 5)
        layout_hbox.addWidget(version_lbl, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout_hbox.addWidget(
            self._separator_update, alignment=Qt.AlignmentFlag.AlignVCenter
        )
        layout_hbox.addWidget(self._update_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_hbox.addWidget(separator_lbl, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout_hbox.addWidget(self._about_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout_hbox)

    def _setup_connections(self):
        """Connect signals to their respective slots."""
        self._update_btn.clicked.connect(self._open_update_link)
        self._about_btn.clicked.connect(self._on_about_clicked)

    @Slot(str, str)
    def show_update_notification(self, version: str, url: str) -> None:
        """Display update notification in the footer.

        Arguments:
            version: New version number.
            url: GitHub release page URL.
        """
        self._update_btn.setText(f"New ! {version}")
        self._update_url = url
        self._update_btn.show()
        self._separator_update.show()

    @Slot()
    def _on_about_clicked(self) -> None:
        """Open the About dialog."""
        parent = self.window()
        dialog = AboutDialog(parent)
        dialog.exec()

    @Slot()
    def _open_update_link(self) -> None:
        """Open the update release page in the default browser."""
        QDesktopServices.openUrl(QUrl(self._update_url))
