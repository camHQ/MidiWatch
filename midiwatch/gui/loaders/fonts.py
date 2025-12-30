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

from PySide6.QtGui import QFontDatabase


logger = logging.getLogger(__name__)


def load_font(font_path: str) -> str | None:
    """
    Load a custom font and return its family name.

    Args:
        font_path: The path to the font file.

    Returns:
        str | None: The family name of the loaded font, or None if loading failed.
    """
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        logger.error("Failed to load font: %s", font_path)
        return None

    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if not font_families:
        logger.error("No font family found in: %s", font_path)
        return None

    logger.info("Font loaded: %s", font_path)
    return font_families[0]


FONTS_TO_LOAD = [":/fonts/FiraCode.ttf", ":/fonts/Roboto.ttf"]


def setup_application_fonts() -> None:
    """
    Load application fonts.
    """
    for font_path in FONTS_TO_LOAD:
        load_font(font_path)
