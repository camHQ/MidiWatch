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

import sys
import logging
import argparse

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from midiwatch.gui import MainWindow
from midiwatch.gui.loaders import initialize_resources
from midiwatch.gui.app import get_lock_file_path, try_acquire_lock
from midiwatch.core.logging_config import setup_logging
from midiwatch.constants import APP_NAME

from midiwatch.gui.resources import resources_rc


if sys.platform == "win32":
    try:
        from ctypes import windll

        myappid = "midiwatch.1.0.0"
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass


def main():
    """Application main entry point."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        prog="midiwatch", description="MidiWatch - MIDI port monitor"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Enable development mode with automatic QSS reloading",
    )
    args = parser.parse_args()

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"{'=' * 20} Starting MidiWatch {'=' * 20}")

    # Create Qt application
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName(APP_NAME)
    app.setDesktopFileName("com.github.camhq.MidiWatch")
    app.setWindowIcon(QIcon(":/images/midiwatch-icon.svg"))

    # Attempt to acquire the lock
    lock_file_path = get_lock_file_path()
    lock_file, lock_acquired = try_acquire_lock(lock_file_path)

    # Check if the lock was acquired
    if not lock_acquired:
        sys.exit(1)

    # Launch the main window
    window = MainWindow()

    # Initialize resources and apply stylesheet (after widgets creation)
    initialize_resources(app, dev_mode=args.dev)

    # Run the event loop
    exit_code = app.exec()

    # Release the lock after the application has closed
    lock_file.unlock()
    logger.info(f"{'=' * 20} Application closed {'=' * 20}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
