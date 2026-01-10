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

from PySide6.QtWidgets import (
    QWidget,
    QTableView,
    QHeaderView,
    QAbstractItemView,
    QStackedLayout,
)
from PySide6.QtCore import Qt, Slot

from midiwatch.gui.models import (
    MidiMessageHumanModel,
    MidiMessageHexModel,
    MidiMessageBinaryModel,
)


class HumanTableView(QTableView):
    """Specialized table view for human-readable MIDI messages."""

    def __init__(self, model: MidiMessageHumanModel) -> None:
        """Initialize the human-readable table view."""
        super().__init__()
        self.setModel(model)

        self._setup_ui()

    def _setup_ui(self):
        """Configure view settings and column widths."""
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)
        self.setAlternatingRowColors(False)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        header.setFixedHeight(32)
        header.resizeSection(0, 150)  # Type
        header.resizeSection(1, 100)  # Channel
        header.resizeSection(2, 90)  # Note
        header.resizeSection(3, 160)  # Detail
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )


class HexTableView(QTableView):
    """Specialized table view for hexadecimal MIDI messages."""

    def __init__(self, model: MidiMessageHexModel) -> None:
        """Initialize the hexadecimal table view."""
        super().__init__()
        self.setModel(model)

        self._setup_ui()

    def _setup_ui(self):
        """Configure view settings and column widths."""
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setFixedHeight(32)
        header.resizeSection(0, 150)
        header.resizeSection(1, 150)
        header.resizeSection(2, 150)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )


class BinaryTableView(QTableView):
    """Specialized table view for binary MIDI messages."""

    def __init__(self, model: MidiMessageBinaryModel) -> None:
        """Initialize the binary table view."""
        super().__init__()
        self.setModel(model)

        self._setup_ui()

    def _setup_ui(self):
        """Configure view settings and column widths."""
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(False)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setFixedHeight(32)
        header.resizeSection(0, 150)
        header.resizeSection(1, 150)
        header.resizeSection(2, 150)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )


class TableStackManager(QWidget):
    """Manages a stack of table views."""

    def __init__(
        self,
        human_view: HumanTableView,
        hex_view: HexTableView,
        binary_view: BinaryTableView,
    ) -> None:
        """Initialize with the table views to manage."""
        super().__init__()

        self._human_view = human_view
        self._hex_view = hex_view
        self._binary_view = binary_view

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self) -> None:
        """Create the stacked layout with table views."""
        self._stack_layout = QStackedLayout()
        self._stack_layout.setContentsMargins(0, 0, 0, 0)
        self._stack_layout.addWidget(self._human_view)
        self._stack_layout.addWidget(self._hex_view)
        self._stack_layout.addWidget(self._binary_view)

        self.setLayout(self._stack_layout)

    def _setup_connections(self) -> None:
        """Connect model signals for auto-scrolling."""
        self._human_view.model().rowsInserted.connect(
            lambda parent, first, last: self._human_view.scrollToBottom()
        )
        self._hex_view.model().rowsInserted.connect(
            lambda parent, first, last: self._hex_view.scrollToBottom()
        )
        self._binary_view.model().rowsInserted.connect(
            lambda parent, first, last: self._binary_view.scrollToBottom()
        )

    @Slot(int)
    def set_current_view(self, view_index: int) -> None:
        """Switch the current displayed view in the stacked layout.

        Arguments:
            view_index: Index of the view to display in the stack
        """
        self._stack_layout.setCurrentIndex(view_index)
