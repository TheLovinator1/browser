from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QWidget

if TYPE_CHECKING:
    from PySide6.QtCore import QSize


class Browser(QMainWindow):
    """Main window of the browser."""

    def __init__(self) -> None:
        """Initialize the browser."""
        super().__init__()
        self.set_window_title()
        self.resize_and_maximize_window()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_window_title)

        self.setCentralWidget(self.tabs)

        self.add_new_tab("https://duckduckgo.com", "New Tab")

        self.create_toolbar()

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

    def add_new_tab(self, url: str, label: str) -> None:
        """Add a new tab with the given URL and label."""
        browser = QWebEngineView()
        browser.setUrl(url)

        tab_index: int = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(tab_index)

    def close_current_tab(self, index: int) -> None:
        """Close the tab at the given index."""
        min_tabs = 2
        if self.tabs.count() < min_tabs:
            return

        self.tabs.removeTab(index)

    def update_window_title(self, index: int) -> None:
        """Update the window title based on the current tab."""
        current_browser: QWidget = self.tabs.widget(index)
        if isinstance(current_browser, QWebEngineView):
            self.setWindowTitle(current_browser.page().title())

    def create_toolbar(self) -> None:
        """Create the toolbar with navigation actions."""
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab("https://duckduckgo.com", "New Tab"))
        toolbar.addAction(new_tab_action)


def main() -> None:
    """Run the browser."""
    app = QApplication([])

    window = Browser()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
