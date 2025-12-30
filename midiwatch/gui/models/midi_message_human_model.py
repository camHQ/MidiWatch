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


class MidiMessageHumanModel(QAbstractTableModel):
    """Table model for representing MIDI messages in human-readable format.

    Displays four columns: Type, Channel, Note, and Detail. Messages are formatted with
    descriptive names, note names with octaves, velocity/pressure percentages, and
    control change names.
    """

    COLUMNS = ["type", "channel", "note", "detail"]

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

        data_keys = ["type", "channel", "note", "detail"]

        return message.get(data_keys[col])

    def add_message(self, msg_data: dict) -> None:
        """Insert a new MIDI message into the model."""

        formatted = self._formatter.format_message_human(msg_data)

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
