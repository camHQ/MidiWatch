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

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl

from midiwatch.constants import (
    APP_VERSION,
    APP_DESCRIPTION,
    COPYRIGHT_TEXT,
    GITHUB_REPO,
    LICENSE_URL,
)

SPACING = 10


class AboutWidget(QWidget):
    """Widget displaying application information."""

    def __init__(self, parent=None):
        """Initialize the About widget."""
        super().__init__(parent)
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Create and arrange child widgets."""
        icon_lbl = QLabel()
        icon_lbl.setPixmap(QPixmap(":/images/midiwatch-logo.svg"))

        version_lbl = QLabel(APP_VERSION)
        version_lbl.setProperty("class", "dialogText")

        desc_lbl = QLabel(APP_DESCRIPTION)
        desc_lbl.setProperty("class", "dialogText")

        self._github_repo_lbl = QLabel(f"<a href='{GITHUB_REPO}'>Source Code</a>")
        self._github_repo_lbl.setOpenExternalLinks(False)
        self._github_repo_lbl.setProperty("class", "dialogText")

        copyright_lbl = QLabel(COPYRIGHT_TEXT)
        copyright_lbl.setProperty("class", "dialogText")

        self._licence_lbl = QLabel(
            f"For more details, visit "
            f"<a href='{LICENSE_URL}'>GNU General Public License</a>"
        )
        self._licence_lbl.setOpenExternalLinks(False)
        self._licence_lbl.setProperty("class", "dialogText")

        layout_vbox = QVBoxLayout()
        layout_vbox.addStretch()

        # Icon + version
        layout_vbox.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_vbox.addSpacing(SPACING)
        layout_vbox.addWidget(version_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_vbox.addStretch()

        # Description
        layout_vbox.addWidget(desc_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_vbox.addSpacing(SPACING)
        layout_vbox.addWidget(
            self._github_repo_lbl, alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout_vbox.addStretch()

        # Footer
        layout_vbox.addWidget(copyright_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_vbox.addSpacing(SPACING)
        layout_vbox.addWidget(self._licence_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        layout_vbox.addStretch()

        self.setLayout(layout_vbox)

    def _setup_connections(self):
        """Connect signals to their respective slots."""
        self._github_repo_lbl.linkActivated.connect(self._open_link)
        self._licence_lbl.linkActivated.connect(self._open_link)

    def _open_link(self, url: str) -> None:
        """Open an external link in the default browser."""
        QDesktopServices.openUrl(QUrl(url))
