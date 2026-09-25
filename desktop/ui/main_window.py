import os
import sys

if sys.platform == "win32":
    import winreg
else:
    winreg = None

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from backend.config import VER
from desktop.host_controller import HostController
from desktop.theme import ACCENT, DANGER, SUCCESS
from desktop.ui.settings_dialog import SettingsDialog

STARTUP_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
STARTUP_VALUE = "SmartDesk"


def app_resource_path(relative: str) -> str:
    base = getattr(
        sys,
        "_MEIPASS",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
    )
    return os.path.join(base, relative)


def startup_command() -> str:
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}" --background'
    python = sys.executable
    return f'"{python}" -m desktop.main --background'


def startup_enabled() -> bool:
    if sys.platform != "win32" or winreg is None:
        return False
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, STARTUP_VALUE)
            return True
    except (FileNotFoundError, OSError):
        return False


def set_startup(enabled: bool) -> None:
    if sys.platform != "win32" or winreg is None:
        return
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY) as key:
        if enabled:
            winreg.SetValueEx(key, STARTUP_VALUE, 0, winreg.REG_SZ, startup_command())
        else:
            try:
                winreg.DeleteValue(key, STARTUP_VALUE)
            except FileNotFoundError:
                pass


class MainWindow(QMainWindow):
    def __init__(self, controller: HostController):
        super().__init__()
        self.controller = controller
        self._quitting = False
        self._last_pairing = None
        self._fade_effects = []

        icon_path = app_resource_path("desktop/resources/smartdesk_icon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("SmartDesk")
        self.setMinimumSize(960, 680)
        self.resize(1080, 760)

        self._build_ui()
        self._build_tray()
        self._connect_signals()

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()

        self.controller_snapshot = self.controller.snapshot()

    def _build_ui(self):
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(28, 24, 28, 20)
        root_layout.setSpacing(18)
        self.setCentralWidget(root)

        header = QHBoxLayout()
        header.setSpacing(14)

        logo = QLabel()
        logo.setPixmap(QIcon(app_resource_path("desktop/resources/smartdesk_icon.png")).pixmap(54, 54))
        logo.setFixedSize(54, 54)
        header.addWidget(logo)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        title = QLabel("SmartDesk")
        title.setObjectName("title")
        title_box.addWidget(title)
        subtitle = QLabel("Wireless productivity controller")
        subtitle.setObjectName("subtitle")
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch(1)

        self.status_dot = QLabel()
        self.status_dot.setFixedSize(11, 11)
        self.status_text = QLabel("STARTING")
        self.status_text.setObjectName("value")
        status_wrap = QHBoxLayout()
        status_wrap.setSpacing(8)
        status_wrap.addWidget(self.status_dot)
        status_wrap.addWidget(self.status_text)
        header.addLayout(status_wrap)

        root_layout.addLayout(header)

        body = QGridLayout()
        body.setHorizontalSpacing(18)
        body.setVerticalSpacing(18)
        body.setColumnStretch(0, 3)
        body.setColumnStretch(1, 2)

        pair_card = QFrame()
        pair_card.setObjectName("card")
        pair_layout = QVBoxLayout(pair_card)
        pair_layout.setContentsMargins(26, 24, 26, 24)
        pair_layout.setSpacing(14)

        self.pair_section = QLabel("PAIRING")
        self.pair_section.setObjectName("sectionLabel")
        pair_layout.addWidget(self.pair_section)

        self.hero = QLabel("Host is ready")
        self.hero.setObjectName("heroText")
        pair_layout.addWidget(self.hero)

        self.pair_subtitle = QLabel("Open SmartDesk on your phone and enter the code below.")
        self.pair_subtitle.setObjectName("muted")
        self.pair_subtitle.setWordWrap(True)
        pair_layout.addWidget(self.pair_subtitle)

        self.pair_code = QLabel("------")
        self.pair_code.setObjectName("pairCode")
        self.pair_code.setAlignment(Qt.AlignCenter)
        pair_layout.addSpacing(7)
        pair_layout.addWidget(self.pair_code)

        self.copy_button = QPushButton("Copy code")
        self.copy_button.setObjectName("accent")
        self.copy_button.clicked.connect(self.copy_pairing_code)
        pair_layout.addWidget(self.copy_button, 0, Qt.AlignCenter)

        self.expiry = QProgressBar()
        self.expiry.setRange(0, 100)
        self.expiry.setTextVisible(False)
        pair_layout.addSpacing(5)
        pair_layout.addWidget(self.expiry)

        self.expiry_text = QLabel("Waiting for host…")
        self.expiry_text.setAlignment(Qt.AlignCenter)
        self.expiry_text.setObjectName("muted")
        pair_layout.addWidget(self.expiry_text)

        device = QFrame()
        device.setObjectName("softCard")
        device_layout = QVBoxLayout(device)
        device_layout.setContentsMargins(16, 14, 16, 14)
        device_layout.setSpacing(4)

        device_header = QHBoxLayout()
        device_header.setSpacing(8)
        device_label = QLabel("CONTROLLER")
        device_label.setObjectName("sectionLabel")
        device_header.addWidget(device_label)
        device_header.addStretch(1)
        self.peer_status = QLabel("Waiting")
        self.peer_status.setObjectName("value")
        device_header.addWidget(self.peer_status)
        device_layout.addLayout(device_header)

        self.device_value = QLabel("No controller connected")
        self.device_value.setObjectName("muted")
        device_layout.addWidget(self.device_value)
        pair_layout.addStretch(1)
        pair_layout.addWidget(device)

        body.addWidget(pair_card, 0, 0, 2, 1)

        host_card = QFrame()
        host_card.setObjectName("card")
        host_layout = QVBoxLayout(host_card)
        host_layout.setContentsMargins(22, 20, 22, 20)
        host_layout.setSpacing(12)

        section = QLabel("HOST")
        section.setObjectName("sectionLabel")
        host_layout.addWidget(section)

        self.host_name = self._info_row(host_layout, "Computer")
        self.host_ip = self._info_row(host_layout, "Local IP")
        self.host_tcp = self._info_row(host_layout, "TCP")
        self.host_udp = self._info_row(host_layout, "Discovery")
        self.host_os = self._info_row(host_layout, "OS")
        self.host_version = self._info_row(host_layout, "Protocol")

        host_layout.addStretch(1)
        body.addWidget(host_card, 0, 1)

        session_card = QFrame()
        session_card.setObjectName("card")
        session_layout = QVBoxLayout(session_card)
        session_layout.setContentsMargins(22, 20, 22, 20)
        session_layout.setSpacing(12)

        section2 = QLabel("SESSION")
        section2.setObjectName("sectionLabel")
        session_layout.addWidget(section2)

        self.session_state = self._info_row(session_layout, "State")
        self.session_controller = self._info_row(session_layout, "Controller")
        self.session_uptime = self._info_row(session_layout, "Host uptime")

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        self.restart_button = QPushButton("Restart host")
        self.restart_button.setObjectName("accent")
        self.restart_button.clicked.connect(self.restart_host)
        buttons.addWidget(self.restart_button)

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        buttons.addWidget(self.settings_button)
        session_layout.addStretch(1)
        session_layout.addLayout(buttons)

        body.addWidget(session_card, 1, 1)
        root_layout.addLayout(body, 1)

        footer = QHBoxLayout()
        self.footer_status = QLabel("Starting SmartDesk host…")
        self.footer_status.setObjectName("footer")
        footer.addWidget(self.footer_status)
        footer.addStretch(1)
        tray_note = QLabel("Runs quietly in the system tray")
        tray_note.setObjectName("footer")
        footer.addWidget(tray_note)
        root_layout.addLayout(footer)

    def _info_row(self, parent_layout, label_text):
        row = QHBoxLayout()
        label = QLabel(label_text)
        label.setObjectName("muted")
        value = QLabel("—")
        value.setObjectName("value")
        value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row.addWidget(label)
        row.addStretch(1)
        row.addWidget(value)
        parent_layout.addLayout(row)
        return value

    def _build_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(app_resource_path("desktop/resources/smartdesk_icon.png")))
        self.tray.setToolTip("SmartDesk")

        from PySide6.QtWidgets import QMenu

        menu = QMenu(self)
        open_action = QAction("Open SmartDesk", self)
        open_action.triggered.connect(self.showNormal)
        menu.addAction(open_action)
        menu.addSeparator()
        self.tray_status_action = QAction("Server: starting…", self)
        self.tray_status_action.setEnabled(False)
        menu.addAction(self.tray_status_action)
        menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()

    def _connect_signals(self):
        self.controller.snapshot_changed.connect(self.apply_snapshot)
        self.controller.error.connect(self.host_error)
        self.controller.log_message.connect(self.footer_status.setText)

    def _tray_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.showNormal()
            self.raise_()
            self.activateWindow()

    def refresh(self):
        snapshot = self.controller.snapshot()
        if snapshot != self.controller_snapshot:
            self.controller_snapshot = snapshot
            self.apply_snapshot(snapshot)

    def apply_snapshot(self, snapshot):
        self.controller_snapshot = snapshot
        running = snapshot.get("running", False)
        active = snapshot.get("active", False)
        peers = snapshot.get("peer_count", 0)

        if not running:
            self._set_status("STOPPED", DANGER)
            self.hero.setText("Host is offline")
            self.footer_status.setText("SmartDesk host is stopped.")
            self.pair_code.setText("------")
            self.copy_button.setEnabled(False)
            self.expiry.setValue(0)
            self.expiry_text.setText("Start the host to generate a pairing code")
            self.peer_status.setText("Offline")
            self.device_value.setText("No controller connected")
            self.session_state.setText("Stopped")
            self.session_controller.setText("—")
        elif active:
            self._set_status("CONNECTED", SUCCESS)
            self.hero.setText("Controller connected")
            self.pair_subtitle.setText("The paired controller can control this computer over the LAN.")
            self.pair_code.setText("••• •••")
            self.copy_button.setEnabled(False)
            self.expiry.setValue(0)
            self.expiry_text.setText("Pairing is locked while a session is active")
            self.peer_status.setText("Connected")
            controller_ip = snapshot.get("controller_ip") or "Unknown device"
            self.device_value.setText(f"Authenticated controller  ·  {controller_ip}")
            self.session_state.setText("Active")
            self.session_controller.setText(controller_ip)
            self.footer_status.setText("SmartDesk is actively serving a controller.")
        else:
            self._set_status("ACTIVE", ACCENT)
            self.hero.setText("Host is ready")
            self.pair_subtitle.setText("Open SmartDesk on your phone and enter the code below.")
            code = snapshot.get("pairing_code") or "------"
            formatted = f"{code[:3]} {code[3:]}" if len(code) == 6 else code
            self.pair_code.setText(formatted)
            self.copy_button.setEnabled(len(code) == 6)
            remaining = snapshot.get("pairing_remaining", 0)
            timeout = max(1, self.controller.settings.pairing_timeout)
            percent = int(max(0, min(100, remaining * 100 / timeout)))
            self.expiry.setValue(percent)
            self.expiry_text.setText(f"Pairing code refreshes in {remaining}s")
            self.peer_status.setText("Waiting" if not peers else "Connecting")
            self.device_value.setText(
                f"{peers} network connection{'s' if peers != 1 else ''} detected" if peers else "No controller connected"
            )
            self.session_state.setText("Awaiting pairing")
            self.session_controller.setText("—")
            self.footer_status.setText("SmartDesk is ready for a controller.")

        self.host_name.setText(snapshot.get("hostname", "—"))
        self.host_ip.setText(snapshot.get("ip", "—"))
        self.host_tcp.setText(str(snapshot.get("tcp_port", "—")))
        self.host_udp.setText(str(snapshot.get("discovery_port", "—")))
        self.host_os.setText(f"{snapshot.get('os', '—')} {snapshot.get('os_version', '')}".strip())
        self.host_version.setText(VER)
        self.session_uptime.setText(self._format_uptime(snapshot.get("uptime", 0)))
        self.tray_status_action.setText(
            "Server: connected" if active else "Server: active" if running else "Server: stopped"
        )

    def _set_status(self, text, color):
        self.status_text.setText(text)
        self.status_dot.setStyleSheet(f"background: {color}; border-radius: 5px;")

    @staticmethod
    def _format_uptime(seconds):
        days, rem = divmod(max(0, int(seconds)), 86400)
        hours, rem = divmod(rem, 3600)
        minutes, secs = divmod(rem, 60)
        if days:
            return f"{days}d {hours}h"
        if hours:
            return f"{hours}h {minutes}m"
        if minutes:
            return f"{minutes}m {secs}s"
        return f"{secs}s"

    def copy_pairing_code(self):
        code = self.controller_snapshot.get("pairing_code")
        if code and len(code) == 6:
            QApplication.clipboard().setText(code)
            self.copy_button.setText("Copied")
            QTimer.singleShot(1200, lambda: self.copy_button.setText("Copy code"))

    def restart_host(self):
        self.restart_button.setEnabled(False)
        self.footer_status.setText("Restarting SmartDesk host…")
        import asyncio
        asyncio.create_task(self._restart_task())

    async def _restart_task(self):
        try:
            await self.controller.restart(self.controller.settings)
        except Exception as exc:
            self.host_error(str(exc))
        finally:
            self.restart_button.setEnabled(True)

    def open_settings(self):
        dialog = SettingsDialog(self.controller.settings, startup_enabled(), self)
        dialog.applied.connect(self.apply_settings)
        dialog.exec()

    def apply_settings(self, settings, startup):
        try:
            set_startup(startup)
        except OSError as exc:
            QMessageBox.warning(self, "Startup setting", f"Could not update Windows startup: {exc}")

        self.settings_button.setEnabled(False)
        self.restart_button.setEnabled(False)
        self.footer_status.setText("Applying settings…")
        import asyncio
        asyncio.create_task(self._apply_settings_task(settings))

    async def _apply_settings_task(self, settings):
        try:
            await self.controller.restart(settings)
        except Exception as exc:
            self.host_error(str(exc))
        finally:
            self.settings_button.setEnabled(True)
            self.restart_button.setEnabled(True)

    def host_error(self, message):
        self.footer_status.setText(f"Error: {message}")
        self._set_status("ERROR", DANGER)
        self.pair_code.setText("------")
        self.copy_button.setEnabled(False)
        if self.isVisible():
            QMessageBox.critical(self, "SmartDesk host error", message)

    def closeEvent(self, event):
        if self._quitting or not self.tray.isVisible():
            event.accept()
            return
        self.hide()
        self.tray.showMessage("SmartDesk", "The host is still running in the system tray.", QSystemTrayIcon.Information, 2200)
        event.ignore()

    def quit_application(self):
        self._quitting = True
        self.tray.hide()
        import asyncio
        asyncio.create_task(self._shutdown())

    async def _shutdown(self):
        try:
            await self.controller.stop()
        finally:
            QApplication.quit()
