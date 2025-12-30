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
    QDialog,
    QPushButton,
    QButtonGroup,
    QStackedLayout,
    QVBoxLayout,
    QHBoxLayout,
)

from midiwatch.gui.widgets.about_widget import AboutWidget
from midiwatch.gui.widgets.credits_widget import CreditsWidget


class AboutDialog(QDialog):
    """Dialog displaying application information and credits."""

    def __init__(self, parent=None):
        """Initialize the 'About' dialog."""
        super().__init__(parent)
        self.setWindowTitle("About MidiWatch")
        self.setModal(True)
        self.setFixedSize(500, 400)

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Create and arrange widgets."""
        about_btn = QPushButton("About")
        about_btn.setCheckable(True)
        about_btn.setChecked(True)
        about_btn.setProperty("class", "dialogTabButton")

        credits_btn = QPushButton("Credits")
        credits_btn.setCheckable(True)
        credits_btn.setProperty("class", "dialogTabButton")

        self._button_group = QButtonGroup()
        self._button_group.addButton(about_btn, 0)
        self._button_group.addButton(credits_btn, 1)

        button_layout = QHBoxLayout()
        button_layout.addWidget(about_btn)
        button_layout.addSpacing(8)
        button_layout.addWidget(credits_btn)

        about_stack = AboutWidget()
        credits_stack = CreditsWidget()

        self._stack_layout = QStackedLayout()
        self._stack_layout.addWidget(about_stack)
        self._stack_layout.addWidget(credits_stack)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(self._stack_layout)
        self.setLayout(main_layout)

    def _setup_connections(self):
        """Connect signals to slots."""
        self._button_group.idClicked.connect(self._set_current_stack)

    def _set_current_stack(self, index: int) -> None:
        """Switch to the selected stack page."""
        self._stack_layout.setCurrentIndex(index)
