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

from PySide6.QtCore import QThread, Signal

from mido.messages import Message
from midiwatch.core.midi import MidiPortManager, MidiConnectionError


logger = logging.getLogger(__name__)


class MidiListenerThread(QThread):
    """Background thread for listening to incoming MIDI messages.

    This thread continuously polls the MIDI input port for incoming messages and emits
    them via Qt signals.

    Signals:
        message_received (dict): Emitted when a MIDI message is received.
            The dict contains the message data and raw bytes.

    Attributes:
        _port_manager (MidiPortManager): Manager providing access to the MIDI
            input port.
    """

    message_received = Signal(dict)

    def __init__(self, port_manager: MidiPortManager) -> None:
        """Initialize the MIDI listener thread.

        Arguments:
            port_manager: The manager used to acess the MIDI input port.
        """
        super().__init__()
        self._port_manager = port_manager
        logger.debug("MidiListenerThread initialized")

    def run(self):
        """Main thread loop for listening to MIDI messages.

        Continuously polls the MIDI input port for pending messages and emits them via
        the message_received signal. The loop runs until an interruption is requested or
        a MidiConnectionError occurs.
        """
        logger.info("MidiListenerThread is running")

        while not self.isInterruptionRequested():
            try:
                for msg in self._port_manager.input_port.iter_pending():
                    msg: Message
                    msg_data = msg.dict().copy()
                    msg_data["bytes"] = msg.bytes()
                    self.message_received.emit(msg_data)

            except MidiConnectionError:
                break

            self.msleep(10)

    def stop(self):
        """Request the thread to stop and wait for it to finish.

        If the thread is not running, this method returns immediately. Otherwise, it
        requests interruption and blocks until the thread has fully terminated.
        """
        if not self.isRunning():
            return

        self.requestInterruption()
        self.wait()
        logger.info("MidiListenerThread stopped")
