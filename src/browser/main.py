from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from PySide6.QtCore import QSize


class Browser(QMainWindow):
    """Main window of the browser."""

    def __init__(self) -> None:
        """Initialize the browser."""
        super().__init__()
        self.set_window_title()
        self.resize_and_maximize_window()

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.browser = QWebEngineView()
        self.browser.setUrl("https://duckduckgo.com")

        layout.addWidget(self.browser)
        self.setCentralWidget(central_widget)

    def set_window_title(self) -> None:
        """Set the title of the window to 'web browser'.

        This is the default title of the window. When the user opens a new tab,
        the title of the window will be updated to the title of the web page.
        """
        self.setWindowTitle("web browser")

    def resize_and_maximize_window(self) -> None:
        """Resize the window to 80% of the screen size and maximize it."""
        screensize: QSize = self.screen().size() * self.screen().devicePixelRatio()
        self.resize(int(screensize.width() * 0.8), int(screensize.height() * 0.8))
        self.showMaximized()


def main() -> None:
    """Run the browser."""
    app = QApplication([])

    window = Browser()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
