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

from PySide6.QtWidgets import QWidget, QButtonGroup, QHBoxLayout, QSizePolicy

from PySide6.QtCore import Signal

from midiwatch.gui.widgets import LabeledButton


class ViewSelector(QWidget):
    """Widget for selecting between different table views."""

    view_changed = Signal(int)

    def __init__(self):
        """Initialize the view selector with toggle buttons."""
        super().__init__()

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """Create and arrange the view selection buttons."""
        human_lbtn = LabeledButton("HUMAN")
        human_lbtn.set_checkable(True)
        human_lbtn.set_checked(True)

        hex_lbtn = LabeledButton("HEX")
        hex_lbtn.set_checkable(True)

        binary_lbtn = LabeledButton("BINARY")
        binary_lbtn.set_checkable(True)

        self._group_button = QButtonGroup()
        self._group_button.addButton(human_lbtn.button, 0)
        self._group_button.addButton(hex_lbtn.button, 1)
        self._group_button.addButton(binary_lbtn.button, 2)

        layout_hbox = QHBoxLayout()
        layout_hbox.setContentsMargins(0, 0, 0, 0)
        layout_hbox.setSpacing(16)
        layout_hbox.addWidget(human_lbtn)
        layout_hbox.addWidget(hex_lbtn)
        layout_hbox.addWidget(binary_lbtn)

        self.setLayout(layout_hbox)

    def _setup_connections(self):
        self._group_button.idClicked.connect(self.view_changed.emit)
