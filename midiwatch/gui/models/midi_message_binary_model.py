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

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QObject

from midiwatch.core.midi import MidiMessageFormatter
from .constants import MAX_MESSAGES


class MidiMessageBinaryModel(QAbstractTableModel):
    """Table model for representing MIDI messages in binary format.

    Displays three columns: Status byte, Data byte 1, Data byte 2.
    Missing bytes are shown as empty strings.
    """

    COLUMNS = ["status byte", "data byte 1", "data byte 2"]

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._formatter = MidiMessageFormatter()
        self._messages = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._messages)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.COLUMNS)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str:
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self.COLUMNS[section].upper()
        return super().headerData(section, orientation, role)

    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> str | None:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        row, col = index.row(), index.column()
        message: dict = self._messages[row]

        data_keys = ["status_byte", "data_byte_1", "data_byte_2"]

        return message.get(data_keys[col])

    def add_message(self, msg_data: dict) -> None:
        """Add a new MIDI message to the model.

        Formats the raw MIDI message data as binary strings and appends it to the table.
        Automatically removes the oldest message if the maximum number of stored
        messages is exceeded.

        Arguments:
            msg_data (dict): Dictionary containing at least a "bytes" key with a list of
            up to 3 integers representing raw MIDI bytes.
        """
        formatted = self._formatter.format_message_binary(msg_data)

        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        self._messages.append(formatted)
        self.endInsertRows()

        if len(self._messages) > MAX_MESSAGES:
            self.beginRemoveRows(QModelIndex(), 0, 0)
            del self._messages[0]
            self.endRemoveRows()

    def get_messages(self) -> list:
        """Get all stared messages.

        Returns:
            list: List of message dictionaries
        """
        return self._messages.copy()

    def clear(self) -> None:
        """Remove all stored MIDI messages from the model."""
        self.beginResetModel()
        self._messages.clear()
        self.endResetModel()
