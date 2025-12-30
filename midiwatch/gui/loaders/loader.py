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

from PySide6.QtWidgets import QApplication

from .styles import load_stylesheet_from_resources, load_stylesheet_from_file
from .fonts import setup_application_fonts


def initialize_resources(app: QApplication, dev_mode: bool = False) -> None:
    """Initialize all GUI resources (fonts, styles).

    Loads application fonts and stylesheet. In development mode, loads the QSS from file
    with hot-reload enabled. In production mode, loads from compiled Qt resources.

    Arguments:
        app: The QApplication instance.
        dev_mode: If True, load stylesheet from file with hot-reload enabled.
                  If False, load stylesheet from compiled Qt resources.
    """
    setup_application_fonts()

    if dev_mode:
        load_stylesheet_from_file(app)
    else:
        load_stylesheet_from_resources(app)
