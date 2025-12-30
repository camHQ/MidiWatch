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

import logging.config

from midiwatch.core.paths import Paths

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "default",
            "filename": Paths.log("midiwatch.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 6,
            "encoding": "utf-8",
            "utc": False,
        },
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["file", "console"]},
        "midiwatch": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "propagate": False,
        },
    },
}


def setup_logging() -> None:
    """Initialize logging from config dict."""
    logging.config.dictConfig(LOGGING)
