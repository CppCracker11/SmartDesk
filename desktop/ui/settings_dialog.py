from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QFormLayout, QLabel, QSpinBox, QVBoxLayout

from desktop.theme import BORDER, MUTED


class SettingsDialog(QDialog):
    applied = Signal(object, bool)

    def __init__(self, settings, startup_enabled, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SmartDesk Settings")
        self.setMinimumWidth(430)

        root = QVBoxLayout(self)
        root.setContentsMargins(26, 26, 26, 22)
        root.setSpacing(18)

        title = QLabel("Host settings")
        title.setObjectName("dialogTitle")
        root.addWidget(title)

        subtitle = QLabel("Changes restart the SmartDesk host and invalidate the current session.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"color: {MUTED};")
        root.addWidget(subtitle)

        form = QFormLayout()
        form.setHorizontalSpacing(22)
        form.setVerticalSpacing(14)

        self.tcp = QSpinBox()
        self.tcp.setRange(1, 65535)
        self.tcp.setValue(settings.tcp_port)
        form.addRow("TCP port", self.tcp)

        self.discovery = QSpinBox()
        self.discovery.setRange(1, 65535)
        self.discovery.setValue(settings.discovery_port)
        form.addRow("Discovery port", self.discovery)

        self.pairing = QSpinBox()
        self.pairing.setRange(15, 3600)
        self.pairing.setValue(settings.pairing_timeout)
        self.pairing.setSuffix(" s")
        form.addRow("Pairing timeout", self.pairing)

        self.session = QSpinBox()
        self.session.setRange(60, 86400)
        self.session.setValue(settings.session_timeout)
        self.session.setSuffix(" s")
        form.addRow("Session timeout", self.session)

        root.addLayout(form)

        self.startup = QCheckBox("Launch SmartDesk when Windows starts")
        self.startup.setChecked(startup_enabled)
        root.addWidget(self.startup)

        note = QLabel("SmartDesk remains LAN-only; this setting only controls local Windows startup.")
        note.setWordWrap(True)
        note.setStyleSheet(f"color: {MUTED}; border-top: 1px solid {BORDER}; padding-top: 12px;")
        root.addWidget(note)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        self.buttons.rejected.connect(self.reject)
        self.buttons.clicked.connect(self._button_clicked)
        root.addWidget(self.buttons)

    def _button_clicked(self, button):
        if button == self.buttons.button(QDialogButtonBox.Apply):
            self._apply()

    def _apply(self):
        from desktop.host_controller import HostSettings

        settings = HostSettings(
            tcp_port=self.tcp.value(),
            discovery_port=self.discovery.value(),
            pairing_timeout=self.pairing.value(),
            session_timeout=self.session.value(),
        )
        self.applied.emit(settings, self.startup.isChecked())
        self.accept()
