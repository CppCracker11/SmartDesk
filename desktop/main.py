import argparse
import asyncio
import sys

from PySide6.QtWidgets import QApplication
from qasync import QEventLoop

from desktop.host_controller import HostController
from desktop.theme import apply_theme
from desktop.ui.main_window import MainWindow, app_resource_path
from PySide6.QtGui import QIcon


def parse_args():
    parser = argparse.ArgumentParser(description="SmartDesk desktop host")
    parser.add_argument("--background", action="store_true", help="Start minimized to the system tray")
    return parser.parse_args()


async def run_app(args):
    controller = HostController()
    window = MainWindow(controller)

    try:
        await controller.start()
    except Exception as exc:
        window.show()
        window.raise_()
        window.activateWindow()
        window.host_error(str(exc))
        return

    if args.background:
        window.hide()
    else:
        window.show()
        window.raise_()
        window.activateWindow()

    quit_event = asyncio.Event()
    app.aboutToQuit.connect(quit_event.set)
    await quit_event.wait()


def main():
    args = parse_args()
    app = QApplication(sys.argv)
    app.setApplicationName("SmartDesk")
    app.setOrganizationName("SmartDesk")
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon(app_resource_path("desktop/resources/smartdesk_icon.png")))
    apply_theme(app)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    task = loop.create_task(run_app(args))
    task.add_done_callback(lambda fut: fut.exception() if not fut.cancelled() else None)

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
