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

import os
import logging

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream, QTimer

from midiwatch.core.paths import Paths


logger = logging.getLogger(__name__)

QSS_PATH = Paths.style("main.qss")
DEFAULT_QSS_RELOAD_INTERVAL = 500


def load_stylesheet_from_resources(app: QApplication) -> None:
    """Load the QSS stylesheet from the Qt resources.

    Arguments:
        app: The QApplication instance to apply the stylesheet to.
    """
    qss_file = QFile(":/styles/main.qss")
    if qss_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        text_stream = QTextStream(qss_file)
        stylesheet = text_stream.readAll()
        qss_file.close()
        app.setStyleSheet(stylesheet)
        logger.info("Stylesheet loaded: %s", qss_file.fileName())
    else:
        logger.error(
            "Failed to load stylesheet from resources: %s", qss_file.errorString()
        )


def load_stylesheet_from_file(app: QApplication) -> None:
    """Load stylesheet from file and enable hot-reload in dev mode.

    Arguments:
        app: The QApplication instance to apply the stylesheet to.
    """
    try:
        with open(QSS_PATH, "r", encoding="utf-8") as f:
            stylesheet = f.read()
            app.setStyleSheet(stylesheet)
            logger.info("Stylesheet loaded: %s", QSS_PATH)
    except FileNotFoundError as error:
        logging.error("Failed to load stylesheet from file: %s", error)

    _setup_qss_autoreload(app)


def _setup_qss_autoreload(
    app: QApplication, interval: int = DEFAULT_QSS_RELOAD_INTERVAL
) -> None:
    """Setup automatic QSS reloading by monitoring file modification time.

    Arguments:
        app: The QApplication instance.
        interval: Check interval in milliseconds (default: 500ms).
    """

    # Dictionary to track the last known modification time of the QSS file
    state: dict[str, float] = {"last_mtime": 0.0}

    def check_qss_update() -> None:
        try:
            # Get the current modification time of the QSS file
            mtime = os.path.getmtime(QSS_PATH)

            # Only reload if the file has been modified since last check
            if mtime != state["last_mtime"]:
                state["last_mtime"] = mtime
                _reload_stylesheet(app)
                logger.info("Stylesheet reloaded: %s", QSS_PATH)
        except Exception as error:
            logger.error("QSS watcher error: %s", error)

    # Create and configure the timer for periodic file checking
    timer = QTimer()
    timer.timeout.connect(check_qss_update)
    timer.start(interval)

    # Store a reference to the timer on the app to prevent garbage collection
    # This keeps the timer alive for the lifetime of the application
    app._qss_reload_timer = timer  # type: ignore[attr-defined]


def _reload_stylesheet(app: QApplication) -> None:
    """Reload stylesheet from file (without setting up watcher again).

    Arguments:
        app: The QApplication instance to apply the stylesheet to.
    """
    try:
        with open(QSS_PATH, "r", encoding="utf-8") as f:
            stylesheet = f.read()
            app.setStyleSheet(stylesheet)
    except FileNotFoundError as error:
        logger.error("Failed to reload stylesheet from file: %s", error)
