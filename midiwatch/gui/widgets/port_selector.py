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

import logging

from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal, Slot, QTimer


from midiwatch.core.midi.constants import NO_DEVICE_TEXT
from midiwatch.core.midi import MidiPortManager


logger = logging.getLogger(__name__)


class PortSelector(QWidget):
    """Widget for selecting MIDI input ports with automatic refresh."""

    port_changed = Signal(str)

    def __init__(self, port_manager: MidiPortManager) -> None:
        """Initialize the PortSelector widget.

        Arguments:
            port_manager: The manager used to retrieve MIDI input ports names.
        """
        super().__init__()

        self._port_manager = port_manager

        self._timer = QTimer()
        self._timer.setInterval(3000)
        self._timer.start()

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._setup_ui()
        self._setup_connections()

        logger.debug("PortSelector initialized")

    def _setup_ui(self) -> None:
        """Create and arrange child widgets."""
        midi_input_lbl = QLabel("MIDI INPUT")
        midi_input_lbl.setProperty("class", "toolBarLabel")
        self._midi_input_cbb = QComboBox()
        self._midi_input_cbb.setMinimumWidth(250)
        self._midi_input_cbb.setProperty("class", "comboBox")
        self._populate_port_list()

        layout_hbox = QVBoxLayout()
        layout_hbox.setContentsMargins(0, 0, 0, 0)
        layout_hbox.addWidget(midi_input_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_hbox.addWidget(self._midi_input_cbb)
        self.setLayout(layout_hbox)

    def _setup_connections(self) -> None:
        """Connect signals to their respective slots."""
        self._timer.timeout.connect(self._sync_port_selection)
        self._midi_input_cbb.currentTextChanged.connect(self.port_changed.emit)

    def _populate_port_list(self) -> None:
        """Fill the combo box with NO_DEVICE_TEXT and available port names."""
        self._midi_input_cbb.clear()
        self._midi_input_cbb.addItems([NO_DEVICE_TEXT] + self._port_manager.input_names)

    @Slot()
    def _sync_port_selection(self) -> None:
        """Refresh port list when the available ports change."""
        existing = [
            self._midi_input_cbb.itemText(i)
            for i in range(1, self._midi_input_cbb.count())
        ]

        if existing != self._port_manager.input_names:
            logger.debug("Port list changed, syncing ComboBox")

            current = self._midi_input_cbb.currentText()
            self._midi_input_cbb.blockSignals(True)
            self._populate_port_list()

            if current == NO_DEVICE_TEXT:
                index = self._midi_input_cbb.findText(NO_DEVICE_TEXT)
                logger.debug("'No device' still selected, no change needed.")
            elif current in self._port_manager.input_names:
                index = self._midi_input_cbb.findText(current)
                logger.debug("Port '%s' still available, keeping selection", current)
            else:
                index = self._midi_input_cbb.findText(NO_DEVICE_TEXT)
                logger.info(
                    "Port '%s' no longer available, reseting to 'No device'", current
                )
                self.port_changed.emit(NO_DEVICE_TEXT)

            self._midi_input_cbb.setCurrentIndex(index)
            self._midi_input_cbb.blockSignals(False)
