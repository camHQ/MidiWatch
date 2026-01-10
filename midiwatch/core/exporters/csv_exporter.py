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

import csv
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


class CsvExporter:
    """Export MIDI messages to CSV format."""

    FIELDNAMES = ["Type", "Channel", "Note", "Detail", "Hex", "Binary"]

    def __init__(self, filepath: str) -> None:
        """Initialize CSV exporter."""
        self.filepath = Path(filepath)
        logger.debug("CsvExporter initialized with filepath: %s", self.filepath)

    def export_merged(
        self, human_msgs: list[dict], hex_msgs: list[dict], binary_msgs: list[dict]
    ) -> bool:
        """Export merged messages from 3 sources to CSV.

        Args:
            human_msgs: List of human-readable message dictionaries
            hex_msgs: List of hex message dictionaries
            binary_msgs: List of binary message dictionaries

        Returns:
            bool: True if export succeeded, False otherwise
        """
        logger.info(
            "Starting export to %s with %d messages", self.filepath, len(human_msgs)
        )
        try:
            merged = self._merge_messages(human_msgs, hex_msgs, binary_msgs)
            logger.debug("Merged %d messages", len(merged))

            self._write_csv(merged)
            logger.info("Export successful : %s", self.filepath)
            return True

        except IOError as e:
            logger.error("Failed to write CSV file: %s", self.filepath)
            return False
        except Exception as e:
            logger.error("Unexpected error during export: %s", e)
            return False

    def _merge_messages(
        self, human_msgs: list[dict], hex_msgs: list[dict], binary_msgs: list[dict]
    ) -> list[dict]:
        """Merge messages from 3 sources into unified dictionaries."""
        logger.debug("Merging messages from 3 sources")

        return [
            {
                "Type": h.get("type", ""),
                "Channel": h.get("channel", ""),
                "Note": h.get("note", ""),
                "Detail": h.get("detail", ""),
                "Hex": self._format_bytes(x),
                "Binary": self._format_bytes(b),
            }
            for h, x, b in zip(human_msgs, hex_msgs, binary_msgs)
        ]

    def _format_bytes(self, msg: dict) -> str:
        """Format message bytes to space-separated string."""
        return " ".join(
            filter(
                None,
                [
                    msg.get("status_byte", ""),
                    msg.get("data_byte_1", ""),
                    msg.get("data_byte_2", ""),
                ],
            )
        )

    def _write_csv(self, messages: list[dict]) -> None:
        """Write messages to CSV file."""
        logger.debug("Writing %d messages to CSV", len(messages))

        try:
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                writer.writerows(messages)
            logger.debug("CSV file written successfully: %s", self.filepath)

        except IOError as e:
            logger.error("IO error while writing CSV: %s", e)
            raise
