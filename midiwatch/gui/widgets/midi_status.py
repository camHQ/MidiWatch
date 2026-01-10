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

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QPaintEvent, QPainter, QBrush, QColor, QPen
from PySide6.QtCore import Qt, Slot, QTimer, QSize


logger = logging.getLogger(__name__)


class _IndicatorLight(QWidget):
    """A custom LED-style indicator light widget.

    Renders a rounded light that can be toggled between active/inactive states or
    flashed for visual feedback.
    """

    FLASH_DURATION = 90  # milliseconds

    def __init__(
        self, active_color: QColor, inactive_color: QColor, size: QSize = QSize(28, 10)
    ) -> None:
        super().__init__()

        self._active_color = active_color
        self._inactive_color = inactive_color
        self._is_active = False
        self._flash_timer = QTimer()

        self.setFixedSize(size)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self._active_color if self._is_active else self._inactive_color

        pen = QPen(Qt.PenStyle.NoPen)
        brush = QBrush()
        brush.setColor(QColor(color.darker()))
        brush.setStyle(Qt.BrushStyle.SolidPattern)

        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect(), self.height() / 2, self.width() / 2)

        brush.setColor(QColor(color))
        painter.setBrush(brush)

        rect = self.rect()
        padding = 0

        inner_rect = rect.adjusted(padding, padding, -padding, -padding)
        radius_x = (self.height() - 2 * padding) / 2
        radius_y = (self.width() - 2 * padding) / 2
        painter.drawRoundedRect(inner_rect, radius_x, radius_y)

    @Slot()
    def activate(self) -> None:
        self._is_active = True
        self.update()

    @Slot()
    def deactivate(self) -> None:
        self._is_active = False
        self.update()

    @Slot()
    def flashing(self) -> None:
        if not self._flash_timer.isActive():
            self._is_active = True
            self.update()
            self._flash_timer.singleShot(self.FLASH_DURATION, self._stop_flashing)

    def _stop_flashing(self) -> None:
        self._is_active = False
        self.update()


class MidiStatus(QWidget):
    """Display widget for MIDI connection and activity status indicators.

    Shows two LED lights: one for MIDI device connection (red/green) and one for
    incoming MIDI activity (dim/bright cyan). Provides methods to update connection
    state and signal activity pulses.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._setup_ui()
        logger.debug("MidiStatus initialized")

    def _setup_ui(self) -> None:
        """Create and arrange widgets."""
        connection_lbl = QLabel("CONNECTION")
        connection_lbl.setProperty("class", "statusLabel")
        activity_lbl = QLabel("ACTIVITY")
        activity_lbl.setProperty("class", "statusLabel")

        self._connection_light = _IndicatorLight(
            inactive_color=QColor("#FF3366"), active_color=QColor("#00E899")
        )
        self._activity_light = _IndicatorLight(
            inactive_color=QColor("#00D9FF").darker(250), active_color=QColor("#00D9FF")
        )

        connection_hbox = QHBoxLayout()
        connection_hbox.setContentsMargins(0, 0, 0, 0)
        connection_hbox.addWidget(connection_lbl, alignment=Qt.AlignmentFlag.AlignRight)
        connection_hbox.addWidget(self._connection_light)

        activity_hbox = QHBoxLayout()
        activity_hbox.setContentsMargins(0, 0, 0, 0)
        activity_hbox.addWidget(activity_lbl, alignment=Qt.AlignmentFlag.AlignRight)
        activity_hbox.addWidget(self._activity_light)

        main_vbox = QVBoxLayout()
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.addLayout(connection_hbox)
        main_vbox.addLayout(activity_hbox)

        self.setLayout(main_vbox)

    @Slot(bool)
    def set_connected(self, connected: bool) -> None:
        """Update MIDI device connection status.

        Arguments:
            connected: True if a MIDI device is connected, False otherwise.
        """
        if connected:
            logger.info("MIDI connection indicator: ON")
            self._connection_light.activate()
        else:
            logger.info("MIDI connection indicator: OFF")
            self._connection_light.deactivate()

    @Slot()
    def set_activity_flashing(self) -> None:
        """Flash the activity indicator to signal incoming MIDI activity."""
        self._activity_light.flashing()
