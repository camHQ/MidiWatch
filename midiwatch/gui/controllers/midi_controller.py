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

import logging

from PySide6.QtCore import QObject, Signal, Slot

from midiwatch.core.midi.constants import NO_DEVICE_TEXT
from midiwatch.gui.threads import MidiListenerThread
from midiwatch.core.midi import MidiPortManager, MidiConnectionError


logger = logging.getLogger(__name__)


class MidiController(QObject):
    """Controller that manages the MIDI input port and listener thread.

    Responsibilities:
        - Open or Close the selected MIDI input port.
        - Start or stop the MidiListenerThread accordingly
        - Emit a signal when listening state change.
    """

    listening_changed = Signal(bool)

    def __init__(
        self, port_manager: MidiPortManager, midi_listener: MidiListenerThread
    ) -> None:
        """Initialize the controller with its dependencies.

        Arguments:
            port_manager: The manager used to open and close MIDI input ports.
            midi_listener: The thread that listens for incoming MIDI messages.
        """
        super().__init__()
        self._port_manager = port_manager
        self._midi_listener = midi_listener
        logger.debug("MidiController initialized")

    @Slot(str)
    def configure_input(self, input_name: str) -> None:
        """Open or close the MIDI input and start or stop listening.

        If 'input_name' is not NO_DEVICE_TEXT, opens the port and starts the MIDI
        listener thread; otherwise closes the port and stops the listener.

        Arguments:
            input_name: Name of the selected MIDI input or NO_DEVICE_TEXT.
        """
        if input_name != NO_DEVICE_TEXT:
            try:
                logger.info("Configuring MIDI input: '%s'", input_name)

                # Stop the thread first (if active)
                if self._midi_listener.isRunning():
                    self._stop_listening()

                # Open the new port (automatically closes the old one)
                self._port_manager.open_input(input_name)

                # Start the thread
                self._start_listening()

            except MidiConnectionError:
                logger.warning("Could not configure MIDI input '%s'", input_name)
        else:
            try:
                # Stop the thread first (if active)
                if self._midi_listener.isRunning():
                    self._stop_listening()

                # Close the port
                self._port_manager.close_input()

            except MidiConnectionError:
                logger.warning("Could not close MIDI input", input_name)

    def _start_listening(self) -> None:
        """Start the MIDI listener thread and emit listening_changed(True)."""
        self._midi_listener.start()
        self.listening_changed.emit(True)

    def _stop_listening(self) -> None:
        """Stop the MIDI listener thread and emit listening_changed(False)."""
        self._midi_listener.stop()
        self.listening_changed.emit(False)
