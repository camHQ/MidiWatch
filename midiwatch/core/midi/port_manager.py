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

import re
import platform
from typing import Callable
import logging

import mido
from mido.ports import BaseInput, BaseOutput


logger = logging.getLogger(__name__)

# Type aliases
PortList = list[str]


class MidiConnectionError(Exception):
    """Custom exception for MIDI connection errors."""


class PortNamesDescriptor:
    """Fetch and filter MIDI port names dynamically."""

    def __init__(self, get_ports_names_func: Callable[[], PortList]) -> None:
        """Initialize the descriptor with a function to fetch port names.

        Arguments:
            get_ports_names_func: A function that retrieves the list of MIDI port
            names.
        """
        self.get_port_names_func = get_ports_names_func

    def __get__(self, obj: object, owner: type) -> PortList:
        """Fetch and process the list of MIDI port names when the attribute is
        accessed.

        Arguments:
            obj: The instance of the class using the descriptor.
            owner: The owner class of the descriptor.

        Returns:
            list: A filtered and processed list of MIDI port names.
        """
        port_names = self.get_port_names_func()
        excluded_keywords = (
            owner.EXCLUDED_KEYWORDS if hasattr(owner, "EXCLUDED_KEYWORDS") else []
        )
        return self._filter_port_names(port_names, excluded_keywords)

    def _filter_port_names(
        self, port_names: PortList, excluded_keywords: list[str]
    ) -> PortList:
        """Filter port names based on excluded keywords and process them.

        Arguments:
            port_names: List of raw MIDI port names.
            excluded_keywords: List of keywords to exclude from the port names. Ports
            containing any of these keywords will be ignored.

        Returns:
            list: A filtered and processed list of port names.
        """
        return [
            self._process_port_names(port_name)
            for port_name in port_names
            if not any(keyword in port_name for keyword in excluded_keywords)
        ]

    @staticmethod
    def _process_port_names(port_name: str) -> str:
        """Process ALSA port names under Linux to remove port numbers, which can change
        between sessions.

        Arguments:
            port_name: The raw MIDI port name.

        Returns:
            str: The processed port name.
        """
        if platform.system() == "Linux":
            return re.sub(r" \d+:\d+$", "", port_name)
        return port_name


class UnsetPort:
    """Special class to represent an uninitialized MIDI port."""

    def __repr__(self):
        return "<UnsetPort>"


class MidiPortManager:
    """Handle MIDI input and output ports.

    Retrieve the names of available ports dynamically using the mido.get_input_names and
    mido.get_output_names methods.

    Attributes:
        EXCLUDED_KEYWORDS: List of keywords to exclude from the port names.
        input_names: Descriptor to fetch and filter MIDI input port names.
        output_names: Descriptor to fetch and filter MIDI output port names.
    """

    EXCLUDED_KEYWORDS = ["RtMidiOut Client", "RtMidiIn Client"]
    input_names = PortNamesDescriptor(mido.get_input_names)  # type: ignore
    output_names = PortNamesDescriptor(mido.get_output_names)  # type: ignore

    def __init__(self):
        """Initialize the MidiPortManager instance."""
        self._inport: BaseInput | UnsetPort = UnsetPort()
        self._outport: BaseOutput | UnsetPort = UnsetPort()
        logger.debug("MidiPortManager initialized")

    def open_input(self, port_name: str) -> None:
        """Open a MIDI input port if the given port name is available.

        Arguments:
            port_name: The name of the MIDI input port to open.
        """
        logger.debug("Attempting to open MIDI input port: '%s'.", port_name)

        try:
            # Close the previous port if it exists
            if not isinstance(self._inport, UnsetPort):
                self.close_input()

            # Open the new port
            self._inport = mido.open_input(port_name)  # type: ignore
            logger.info("MIDI input port '%s' opened successfully", port_name)

        except OSError as error:
            logger.warning("Failed to open MIDI input port '%s': %s", port_name, error)
            raise MidiConnectionError(f"Failed to open MIDI input port: {error}")
        except Exception as error:
            logger.warning(
                "Unexpected error while opening MIDI input port: '%s'", error
            )
            raise MidiConnectionError(f"Unexpected error: {error}")

    def open_output(self, port_name: str) -> None:
        """Open a MIDI output port if the given port name is available.

        Arguments:
            port_name: The name of the MIDI output port to open.
        """
        logger.debug("Attempting to open MIDI output port: '%s'.", port_name)

        try:
            # Close the previous port if it exists
            if not isinstance(self._outport, UnsetPort):
                self.close_output()

            # Open the new port
            self._outport = mido.open_output(port_name, autoreset=True)  # type: ignore
            logger.info("MIDI output port '%s' opened successfully", port_name)

        except OSError as error:
            logger.warning("Failed to open MIDI output port: '%s'", error)
            raise MidiConnectionError(f"Failed to open MIDI output port: {error}")
        except Exception as error:
            logger.warning(
                "Unexpected error while opening MIDI output port: '%s'", error
            )
            raise MidiConnectionError(f"Unexpected error: {error}")

    def close_input(self) -> None:
        """Close the currently opened MIDI input port, if any.

        Raises:
            MidiConnectionError: If an error occurs while closing the input port.
        """
        if not isinstance(self._inport, UnsetPort):
            try:
                self._inport.close()
                logger.info(
                    "MIDI input port '%s' closed successfully", self._inport.name
                )
                self._inport = UnsetPort()

            except Exception as error:
                logger.error("Failed to close MIDI input port: '%s'", error)
                raise MidiConnectionError(f"Failed to close MIDI input port: {error}")

    def close_output(self) -> None:
        """Close the currently opened MIDI output port, if any.

        Raises:
            MidiConnectionError: If an error occurs while closing the output port.
        """
        if not isinstance(self._outport, UnsetPort):
            try:
                self._outport.close()
                logger.info(
                    "MIDI output port '%s' closed successfully", self._outport.name
                )
                self._outport = UnsetPort()

            except Exception as error:
                logger.error("Failed to close MIDI output port: '%s'.", error)
                raise MidiConnectionError(f"Failed to close MIDI output port: {error}")

    @property
    def input_port(self) -> BaseInput:
        """Get the input port, ensuring it's properly set.

        Returns:
            BaseInput: The active MIDI input port.

        Raises:
            MidiConnectionError: If the input port hasn't been set yet.
        """
        if isinstance(self._inport, UnsetPort):
            raise MidiConnectionError(
                "Input port is not configured. Call open_input() first"
            )
        return self._inport

    @property
    def output_port(self) -> BaseOutput:
        """Get the output port, ensuring it's properly set.

        Returns:
            BaseOutput: The active MIDI output port.

        Raises:
            MidiConnectionError: If the output port hasn't been set yet.
        """
        if isinstance(self._outport, UnsetPort):
            raise MidiConnectionError(
                "Output port is not configured. Call open_output() first"
            )
        return self._outport
