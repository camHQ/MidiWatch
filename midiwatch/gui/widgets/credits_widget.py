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

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PySide6.QtCore import Qt, QFile, QTextStream, QStringConverter


logger = logging.getLogger(__name__)


class CreditsWidget(QWidget):
    """Widget displaying credits information."""

    def __init__(self, parent=None):
        """Initialize the Credits widget."""
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Create and arrange child widgets."""
        credits_txt = ""

        credits_file = QFile(":/legal/CREDITS.txt")
        if credits_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            text_stream = QTextStream(credits_file)
            text_stream.setEncoding(QStringConverter.Encoding.Utf8)
            credits_txt = text_stream.readAll()
            logger.info("Credits file loaded: %s", credits_file.fileName())
            credits_file.close()
        else:
            logger.error("Failed to load Credits file: %s", credits_file.errorString())

        credits_pte = QPlainTextEdit()
        credits_pte.setReadOnly(True)
        credits_pte.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        credits_pte.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        credits_pte.setPlainText(credits_txt)
        credits_pte.setObjectName("creditsPlainText")

        layout_vbox = QVBoxLayout()
        layout_vbox.addWidget(credits_pte)

        self.setLayout(layout_vbox)
