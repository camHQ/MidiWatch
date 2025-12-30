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

from .constants import MIDI_CC_NAMES, PITCH_MAX, MIDI_MAX_VALUE, MIDI_NOTE_DETAILS


class MidiMessageFormatter:
    """Format MIDI messages in various representations (human, hexadecimal, binary)."""

    _FORMATTERS = {
        # Channel Voice Messages.
        "note_off": "_format_note_message",
        "note_on": "_format_note_message",
        "polytouch": "_format_polytouch_message",
        "control_change": "_format_control_change_message",
        "program_change": "_format_program_change_message",
        "aftertouch": "_format_aftertouch_message",
        "pitchwheel": "_format_pitchwheel_message",
        # System common messages.
        "quarter_frame": "_format_quarter_frame_message",
        "songpos": "_format_songpos_message",
        "song_select": "_format_song_select_message",
        "sysex": "_format_sysex_message",
    }

    def format_message_human(self, msg_data: dict) -> dict:
        """Format a MIDI message as human-readable strings.

        Transforms raw MIDI message data into a user-friendly format suitable for
        display. For message types with specific formatting logic (e.g., Note On/Off,
        Control Change, System Common messages), dedicated formatting methods are
        dispatched via the _FORMATTERS registry. All other message types (e.g., System
        Real-Time messages) receive automatic formatting: the type name is capitalized
        and no additional detail is provided.

        Channel indexing is adjusted from 0-based to 1-based for display.

        Arguments:
            msg_data: Raw MIDI message data from mido.

        Returns:
            dict: Formatted message with keys:
                - "type": Human-readable message type name
                - "channel": 1-based channel number (if applicable, empty otherwise)
                - "note": Note name with octave (e.g., "C4 (60)") for note messages
                - "detail": Additional context (velocity %, CC name, position, etc.)
        """
        raw_type: str = msg_data.get("type", "unknown")

        # Adjust channel to 1-based indexing for display
        if "channel" in msg_data:
            msg_data["channel"] = msg_data["channel"] + 1

        if raw_type in self._FORMATTERS:
            method_name = self._FORMATTERS[raw_type]
            getattr(self, method_name)(msg_data)
        else:
            msg_data["type"] = raw_type.replace("_", " ").title()
            msg_data["detail"] = ""

        return msg_data

    def format_message_hex(self, msg_data: dict) -> dict:
        """Format MIDI message bytes as hexadecimal strings.

        Extracts up to 3 MIDI bytes (status byte and 2 data bytes) and formats them as
        hexadecimal strings (e.g., "0xFF").

        Arguments:
            msg_data: Dictionary containing a "bytes" key with raw MIDI byte values.

        Returns:
            dict: Mapping with keys "status_byte", "data_byte_1", "data_byte_2"
                  containing hex string representations. Missing bytes are empty
                  strings.
        """
        keys = ["status_byte", "data_byte_1", "data_byte_2"]
        values = []
        msg_bytes = msg_data.get("bytes", [])

        for i in range(3):
            try:
                byte = msg_bytes[i]
                values.append(f"0x{byte:02X}")
            except IndexError:
                # No byte available at this index
                values.append("")

        return dict(zip(keys, values))

    def format_message_binary(self, msg_data: dict) -> dict:
        """Format MIDI message bytes as binary strings.

        Extracts up to 3 MIDI bytes (status byte and 2 data bytes) and formats them as
        binary strings (e.g., "11111111").

        Arguments:
            msg_data: Dictionary containing a "bytes" key with raw MIDI byte values.

        Returns:
            dict: Mapping with keys "status_byte", "data_byte_1", "data_byte_2"
                  containing binary string representations (8 bits each). Missing bytes
                  are empty strings.
        """
        keys = ["status_byte", "data_byte_1", "data_byte_2"]
        values = []
        msg_bytes = msg_data.get("bytes", [])

        for i in range(3):
            try:
                byte = msg_bytes[i]
                values.append(f"{byte:08b}")
            except IndexError:
                # No byte available at this index
                values.append("")

        return dict(zip(keys, values))

    def _format_note_message(self, msg_data: dict) -> None:
        """Format Note On/Off messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        midi_note = msg_data.get("note")
        raw_type: str = msg_data.get("type", "unknown")

        if midi_note is not None and midi_note in MIDI_NOTE_DETAILS:
            note_name = MIDI_NOTE_DETAILS[midi_note]["name"]
            note_octave = MIDI_NOTE_DETAILS[midi_note]["octave"]
            msg_data["note"] = f"{note_name}{note_octave} ({midi_note})"

        velocity = msg_data.get("velocity", 0)
        percentage = (velocity / MIDI_MAX_VALUE) * 100
        msg_data["type"] = raw_type.replace("_", " ").title()
        msg_data["detail"] = f"Velocity: {percentage:.0f}% ({velocity})"

    def _format_polytouch_message(self, msg_data: dict) -> None:
        """Format Polyphonic Aftertouch messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        midi_note = msg_data.get("note")
        pressure = msg_data.get("value", 0)
        percentage = (pressure / MIDI_MAX_VALUE) * 100
        msg_data["type"] = "Polyphonic Touch"
        msg_data["detail"] = f"{midi_note} → {percentage:.0f}% ({pressure})"

    def _format_control_change_message(self, msg_data: dict) -> None:
        """Format Control Change messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        ctrl = msg_data.get("control", None)
        value = msg_data.get("value", None)
        if ctrl is not None:
            name = MIDI_CC_NAMES.get(ctrl, f"CC {ctrl}")
            msg_data["type"] = f"Control Change {ctrl}"
            msg_data["detail"] = f"{name}: {value}"

    def _format_program_change_message(self, msg_data: dict) -> None:
        """Format Program Change messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        program = msg_data.get("program", 0)
        msg_data["type"] = "Program Change"
        msg_data["detail"] = f"Program: {program}"

    def _format_aftertouch_message(self, msg_data: dict) -> None:
        """Format Aftertouch messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        value = msg_data.get("value", 0)
        percentage = (value / MIDI_MAX_VALUE) * 100
        msg_data["type"] = "Aftertouch"
        msg_data["detail"] = f"{percentage:.0f}% ({value})"

    def _format_pitchwheel_message(self, msg_data: dict) -> None:
        """Format Pitch Wheel messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        pitch = msg_data.get("pitch", 0)
        percentage = (pitch / PITCH_MAX) * 100
        msg_data["type"] = "Pitch Bend"
        msg_data["detail"] = f"Pitch: {percentage:.0f}% ({pitch})"

    def _format_quarter_frame_message(self, msg_data: dict) -> None:
        """Format MTC Quarter Frame messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        frame_type = msg_data.get("frame_type", 0)
        frame_value = msg_data.get("frame_value", 0)

        # Names readable according to MIDI specification
        type_names = {
            0: "Frames LS",
            1: "Frames MS",
            2: "Seconds LS",
            3: "Seconds MS",
            4: "Minutes LS",
            5: "Minutes MS",
            6: "Hours LS",
            7: "Hours MS",
        }

        type_name = type_names.get(frame_type, f"Type {frame_type}")

        msg_data["type"] = "MTC Quarter Frame"
        msg_data["detail"] = f"{type_name}: {frame_value}"

    def _format_songpos_message(self, msg_data: dict) -> None:
        """Format Song Position messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        pos = msg_data.get("pos", 0)
        msg_data["type"] = "Song Position"
        msg_data["detail"] = f"Position: {pos}"

    def _format_song_select_message(self, msg_data: dict) -> None:
        """Format Song Select messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        song = msg_data.get("song", 0)
        msg_data["type"] = "Song Select"
        msg_data["detail"] = f"Song: {song}"

    def _format_sysex_message(self, msg_data: dict) -> None:
        """Format System Exclusive messages.

        Arguments:
            msg_data: MIDI message dictionary to format in-place.
        """
        data = msg_data.get("data", ())
        byte_count = len(data)
        msg_data["type"] = "System Exclusive"
        msg_data["detail"] = f"Data: {byte_count} bytes"
