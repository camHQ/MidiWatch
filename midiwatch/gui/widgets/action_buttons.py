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

from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Signal

from midiwatch.gui.widgets import LabeledButton


class ActionButtons(QWidget):
    """Widget containing action buttons for clearing and exporting data.

    Signals:
        clear_clicked: Emitted when the clear button is clicked.
        export_clicked: Emitted when the export button is clicked.

    """

    clear_clicked = Signal()
    export_clicked = Signal()

    def __init__(self):
        """Initialize the action buttons widget."""
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._setup_ui()

    def _setup_ui(self):
        """Create and arrange child widgets."""
        clear_lbtn = LabeledButton("CLEAR")
        clear_lbtn.clicked.connect(self.clear_clicked.emit)

        export_lbtn = LabeledButton("EXPORT")
        export_lbtn.clicked.connect(self.export_clicked.emit)

        layout_hbox = QHBoxLayout()
        layout_hbox.setContentsMargins(0, 0, 0, 0)
        layout_hbox.setSpacing(16)
        layout_hbox.addWidget(clear_lbtn)
        layout_hbox.addWidget(export_lbtn)

        self.setLayout(layout_hbox)
