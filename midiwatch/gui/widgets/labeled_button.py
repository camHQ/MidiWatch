# This file is part of MidiWatch.
# Copyright (C) 2025-2026 cam84
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

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, Signal


class LabeledButton(QWidget):
    """Widget consisting of a label above a square button.

    Signals:
        clicked: Emitted when the button is clicked.
    """

    clicked = Signal()

    def __init__(self, label_text: str, button_size: int = 28, parent=None) -> None:
        """Initialize the labeled button widget.

        Arguments:
            label_text: Text to display above the button.
            button_size: Size of the square button in pixels.
            parent: Optional parent widget.
        """
        super().__init__(parent)
        self._setup_ui(label_text, button_size)

    def _setup_ui(self, label_text: str, button_size: int) -> None:
        """Create and arrange child widgets."""

        label = QLabel(label_text)
        label.setProperty("class", "toolBarLabel")

        self.button = QPushButton()
        self.button.setFixedSize(button_size, button_size)
        self.button.setProperty("class", "squareButton")
        self.button.clicked.connect(self.clicked.emit)

        layout_vbox = QVBoxLayout()
        layout_vbox.setContentsMargins(0, 0, 0, 0)
        layout_vbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_vbox.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout_vbox)

    def set_checkable(self, checkable: bool) -> None:
        """Set whether the button is checkable (toggleable)."""
        self.button.setCheckable(checkable)

    def set_checked(self, checked: bool) -> None:
        """Set the checked state of the button."""
        self.button.setChecked(checked)

    def is_checked(self) -> bool:
        """Return whether the button is currently checked."""
        return self.button.isChecked()
