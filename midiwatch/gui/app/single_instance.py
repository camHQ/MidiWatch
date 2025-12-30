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

import os
import logging

from PySide6.QtCore import QStandardPaths, QLockFile


logger = logging.getLogger(__name__)


def get_lock_file_path() -> str:
    """
    Return the full path of the lock file.

    The lock file is placed in the system's temporary directory.

    Returns:
        str: Full path to the lock file
    """
    temp_dir = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.TempLocation
    )

    return os.path.join(temp_dir, "midiwatch.lock")


def try_acquire_lock(lock_file_path: str) -> tuple[QLockFile, bool]:
    """
    Attempt to acquire a lock for the application.

    Creates a lock that prevents multiple instances of the application from running
    simultaneously.

    Args:
        lock_file_path: Path to the lock file

    Returns:
        tuple[QLockFile, bool]:
            - QLockFile: the lock object
            - bool: True if lock acquired, False otherwise
    """
    lock_file = QLockFile(lock_file_path)
    lock_file.setStaleLockTime(30000)

    if lock_file.tryLock(100):
        logger.info("Lock acquired: %s", lock_file_path)
        return lock_file, True
    else:
        error = lock_file.error()

        if error == QLockFile.LockError.LockFailedError:
            logger.error("Another instance is already running (%s)", error.name)
        else:
            logger.error("Lock error: %s", error.name)

        return lock_file, False
