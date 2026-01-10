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

import sys
import platformdirs
from pathlib import Path


class Paths:
    """Manage project directory structure and provide dynamic paths."""

    base: Path = Path(__file__).resolve().parent.parent.parent
    midiwatch_dir: Path = base / "midiwatch"
    resources_dir: Path = midiwatch_dir / "gui" / "resources"
    fonts: Path = resources_dir / "fonts"
    images: Path = resources_dir / "images"
    styles: Path = resources_dir / "styles"
    logs: Path = base / "logs"

    @classmethod
    def font(cls, filename: str) -> str:
        """Return the absolute path of an font file.

        Args:
            filename: Name of the font file.

        Returns:
            str: Absolute path of the file.
        """
        return str(cls.fonts / filename)

    @classmethod
    def image(cls, filename: str) -> str:
        """Return the absolute path of an image file.

        Args:
            filename: Name of the image file.

        Returns:
            str: Absolute path to the file.
        """
        return str(cls.images / filename)

    @classmethod
    def style(cls, filename: str) -> str:
        """Return the absolute path of an qss file.

        Args:
            filename: Name of the qss file.

        Returns:
            str: Absolute path to the file.
        """
        return str(cls.styles / filename)

    @classmethod
    def log(cls, filename: str) -> str:
        """Return the appropriate log file path based on execution environment.

        Arguments:
            filename: Name of the log file.

        Returns:
            str: Absolute path to the log file.
        """
        if getattr(sys, "frozen", False):
            log_dir = platformdirs.user_log_path(appname="midiwatch")
        else:
            log_dir = cls.logs
        log_dir.mkdir(parents=True, exist_ok=True)
        return str(log_dir / filename)
