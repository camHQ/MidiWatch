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
from PySide6.QtCore import Qt

from midiwatch.gui.dialogs import AboutDialog
from midiwatch.constants import APP_NAME, APP_VERSION


class FooterWidget(QWidget):
    def __init__(self, parent=None):
        """Initialize the footer widget."""
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setObjectName("footer")
        self._setup_ui()

    def _setup_ui(self):
        """Create and arrange child widgets."""
        version_lbl = QLabel(f"{APP_NAME} v{APP_VERSION}")

        separator_lbl = QLabel("/")

        about_btn = QPushButton("about")
        about_btn.setFlat(True)
        about_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        about_btn.clicked.connect(self._on_about_clicked)

        layout_hbox = QHBoxLayout()
        layout_hbox.setContentsMargins(0, 5, 0, 5)
        layout_hbox.addWidget(version_lbl, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout_hbox.addWidget(separator_lbl, alignment=Qt.AlignmentFlag.AlignVCenter)
        layout_hbox.addWidget(about_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout_hbox)

    def _on_about_clicked(self) -> None:
        parent = self.window()
        dialog = AboutDialog(parent)
        dialog.exec()
