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

from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Slot, QStandardPaths, QTimer

from .widgets import (
    PortSelector,
    MidiStatus,
    ViewSelector,
    HumanTableView,
    HexTableView,
    BinaryTableView,
    TableStackManager,
    ActionButtons,
    FooterWidget,
)

from .threads import MidiListenerThread, UpdateCheckerThread
from .controllers import MidiController
from .models import MidiMessageHumanModel, MidiMessageHexModel, MidiMessageBinaryModel
from midiwatch.core.midi import MidiPortManager
from midiwatch.core.exporters import CsvExporter
from midiwatch.constants import APP_VERSION


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._port_manager = MidiPortManager()
        self._midi_listener = MidiListenerThread(self._port_manager)
        self._midi_controller = MidiController(self._port_manager, self._midi_listener)

        self._human_model = MidiMessageHumanModel()
        self._hex_model = MidiMessageHexModel()
        self._binary_model = MidiMessageBinaryModel()

        self._human_view = HumanTableView(self._human_model)
        self._hex_view = HexTableView(self._hex_model)
        self._binary_view = BinaryTableView(self._binary_model)

        self._update_checker = None

        self._initialize_ui()

        QTimer.singleShot(3000, self._check_for_updates)

    def _initialize_ui(self) -> None:
        """Initialize UI"""
        self.setWindowTitle("MidiWatch")
        self.setFixedWidth(600)
        self.setMinimumHeight(720)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)

        self._setup_ui()
        self._setup_connections()

        self.show()

    def _setup_ui(self) -> None:
        """Create and arrange widgets in the main window."""

        # Header section: application title and MIDI status indicator
        main_title = QLabel()
        main_title.setPixmap(QPixmap(":/images/midiwatch-logo.svg"))
        main_title.setObjectName("mainTitle")
        self.midi_status = MidiStatus()
        header_hbox = QHBoxLayout()
        header_hbox.setContentsMargins(10, 0, 10, 0)
        header_hbox.addWidget(main_title, alignment=Qt.AlignmentFlag.AlignVCenter)
        header_hbox.addStretch()
        header_hbox.addWidget(self.midi_status)

        # ToolBar section : input port selector, view selector and actions buttons
        self._port_selector = PortSelector(self._port_manager)
        self._view_selector = ViewSelector()
        self._action_buttons = ActionButtons()

        toolbar_hbox = QHBoxLayout()
        toolbar_hbox.setContentsMargins(0, 0, 0, 0)
        toolbar_hbox.addWidget(self._port_selector)
        toolbar_hbox.addStretch()
        toolbar_hbox.addWidget(self._view_selector)
        toolbar_hbox.addStretch()
        toolbar_hbox.addWidget(self._action_buttons)

        # Content section : stacked table views
        self._table_stack = TableStackManager(
            human_view=self._human_view,
            hex_view=self._hex_view,
            binary_view=self._binary_view,
        )

        # Footer
        self._footer_fw = FooterWidget(self)

        # Main vertical layout containing all UI elements
        main_vbox = QVBoxLayout()
        main_vbox.setContentsMargins(16, 20, 16, 10)
        main_vbox.addLayout(header_hbox)
        main_vbox.addSpacing(48)
        main_vbox.addLayout(toolbar_hbox)
        main_vbox.addSpacing(24)
        main_vbox.addWidget(self._table_stack)
        main_vbox.addWidget(self._footer_fw, alignment=Qt.AlignmentFlag.AlignCenter)

        # Central widget of the main window
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        central_widget.setLayout(main_vbox)
        self.setCentralWidget(central_widget)

    def _setup_connections(self) -> None:
        """Connect signals to their respective slots."""

        # Update the MIDI connection status indicator.
        self._midi_controller.listening_changed.connect(self.midi_status.set_connected)

        # Blink the MIDI activity indicator on every received MIDI message.
        self._midi_listener.message_received.connect(
            self.midi_status.set_activity_flashing
        )

        # Add incoming MIDI messages to models.
        self._midi_listener.message_received.connect(self._human_model.add_message)
        self._midi_listener.message_received.connect(self._hex_model.add_message)
        self._midi_listener.message_received.connect(self._binary_model.add_message)

        # Connect port selection signal to update MIDI input configuration.
        self._port_selector.port_changed.connect(self._midi_controller.configure_input)

        # Link view selection buttons to switching of stacked table views.
        self._view_selector.view_changed.connect(self._table_stack.set_current_view)

        # Clear all messages from the models and update the associated table views.
        self._action_buttons.clear_clicked.connect(self._clear_models)

        # Export
        self._action_buttons.export_clicked.connect(self._export_models)

    @Slot()
    def _check_for_updates(self):
        """Launch update check in background thread."""
        self._update_checker = UpdateCheckerThread(APP_VERSION)
        self._update_checker.update_available.connect(
            self._footer_fw.show_update_notification
        )
        self._update_checker.start()

    @Slot()
    def _clear_models(self) -> None:
        """Clear all MIDI message models."""
        self._human_model.clear()
        self._hex_model.clear()
        self._binary_model.clear()

    @Slot()
    def _export_models(self) -> None:
        """Export MIDI messages to CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        default_filename = f"midiwatch_{timestamp}.csv"

        default_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation
        )
        default_path = f"{default_dir}/{default_filename}"

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            caption="Export MIDI Messages",
            dir=default_path,
            filter="CSV Files (*.csv)",
        )
        if filepath:
            human_msgs = self._human_model.get_messages()
            hex_msgs = self._hex_model.get_messages()
            binary_msgs = self._binary_model.get_messages()

            exporter = CsvExporter(filepath)
            success = exporter.export_merged(human_msgs, hex_msgs, binary_msgs)

            if not success:
                QMessageBox.critical(self, "Error", "The export failed")

    def closeEvent(self, event) -> None:
        self._midi_listener.stop()
        self._midi_listener.wait()
        event.accept()
