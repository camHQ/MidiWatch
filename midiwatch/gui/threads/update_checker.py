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

import requests, logging

from PySide6.QtCore import QThread, Signal

from midiwatch.constants import GITHUB_OWNER, APP_NAME, APP_VERSION

logger = logging.getLogger(__name__)


def get_latest_release(owner: str = GITHUB_OWNER, repo: str = APP_NAME) -> dict:
    """Fetch the latest release information from GitHub API.

    Arguments:
        owner: GitHub repository owner username.
        repo: GitHub repository name.

    Returns:
        Dictionary with release info (tag_name, html_url, name, success).
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{APP_NAME}/{APP_VERSION}",
    }

    logger.debug("Fetching latest release from GitHub: %s/%s", owner, repo)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data: dict = response.json()

        tag_name = data.get("tag_name")
        logger.info("Latest release fetched successfully: %s", tag_name)

        return {
            "tag_name": tag_name,
            "html_url": data.get("html_url"),
            "name": data.get("name"),
            "success": True,
        }
    except requests.exceptions.RequestException as error:
        logger.warning("Failed to fetch latest release: %s", error)
        return {
            "success": False,
            "error": str(error),
        }


def is_update_available(local_version: str, remote_version: str) -> bool:
    """Check if a newer version is available.

    Arguments:
        remote_version: Version tag from GitHub (e.g., "v1.0.1").
        local_version: Current application version.

    Returns:
       True if remote version is newer, False otherwise.
    """
    if not remote_version:
        return False

    normalized_remote_version = remote_version.lstrip("v")

    return normalized_remote_version > local_version


class UpdateCheckerThread(QThread):
    """Thread for checking GitHub updates without blocking the UI."""

    update_available = Signal(str, str)  # (normalized_remote_version, html_url)
    no_update = Signal()

    def __init__(self, local_version: str = APP_VERSION) -> None:
        """
        Initialize the update checker thread.

        Arguments:
            local_version: Current application version to compare against.
        """
        super().__init__()
        self.local_version = local_version
        logger.debug(
            "UpdateCheckerThread initialized with local version: %s", local_version
        )

    def run(self) -> None:
        """Execute the update check in a separate thread."""
        result: dict = get_latest_release()

        if result["success"]:
            remote_version: str = result["tag_name"]

            if is_update_available(self.local_version, remote_version):
                normalized_remote_version = remote_version.lstrip("v")
                logger.info(
                    "Update available: %s → %s",
                    self.local_version,
                    normalized_remote_version,
                )
                self.update_available.emit(remote_version, result["html_url"])
            else:
                logger.debug(
                    "Application is up to date (local: %s)", self.local_version
                )
                self.no_update.emit()
