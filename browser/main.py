from __future__ import annotations

import contextlib
import logging
from typing import TYPE_CHECKING, cast

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QMenu, QTabWidget, QToolBar, QToolButton, QWidget

if TYPE_CHECKING:
    from PySide6.QtCore import QPoint, QSize, QUrl

logging.basicConfig(level=logging.INFO)


class Browser(QMainWindow):
    """Main window of the browser."""

    def __init__(self) -> None:
        """Initialize the browser."""
        super().__init__()
        self.set_window_title()
        self.resize_and_maximize_window()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.disconnect()
        self.tabs.currentChanged.connect(self.update_window_title)
        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_context_menu)

        self.setCentralWidget(self.tabs)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.create_toolbar()
        self.add_new_tab("https://duckduckgo.com", "New Tab")

        self.create_shortcuts()
        self.add_new_tab_button()

    def set_window_title(self) -> None:
        """Set the title of the window to 'web browser'.

        This is the default title of the window. When the user opens a new tab,
        the title of the window will be updated to the title of the web page.
        """
        with contextlib.suppress(Exception):
            self.setWindowTitle("web browser")

    def resize_and_maximize_window(self) -> None:
        """Resize the window to 80% of the screen size and maximize it."""
        screensize: QSize = self.screen().size() * self.screen().devicePixelRatio()
        self.resize(int(screensize.width() * 0.8), int(screensize.height() * 0.8))
        self.showMaximized()

    def add_new_tab(self, url: str, label: str) -> None:
        """Add a new tab with the given URL and label."""
        view = QWebEngineView()
        view.setUrl(url)
        view.urlChanged.connect(self.update_url_bar)

        tab_index: int = self.tabs.addTab(view, label)
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

    def create_shortcuts(self) -> None:
        """Create keyboard shortcuts for various actions."""
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))

        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(lambda: self.add_new_tab("https://duckduckgo.com", "New Tab"))

        close_browser_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        close_browser_shortcut.activated.connect(self.close)

        reload_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        reload_shortcut.activated.connect(
            lambda: cast(QWebEngineView, self.tabs.currentWidget()).reload()
            if isinstance(self.tabs.currentWidget(), QWebEngineView)
            else None
        )

    def add_new_tab_button(self) -> None:
        """Add a new tab button to the right of the tabs."""
        new_tab_button = QToolButton(self)
        new_tab_button.setText("+")
        new_tab_button.clicked.connect(lambda: self.add_new_tab("https://duckduckgo.com", "New Tab"))
        self.tabs.setTabBarAutoHide(False)
        self.tabs.setTabsClosable(True)
        self.tabs.tabBar().setMovable(True)
        self.tabs.tabBar().setTabsClosable(True)
        self.tabs.tabBar().tabCloseRequested.connect(self.close_current_tab)

        self.tabs.setCornerWidget(new_tab_button)

    def create_toolbar(self) -> None:
        """Create the toolbar with the URL bar."""
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)
        toolbar.addWidget(self.url_bar)

    def navigate_to_url(self) -> None:
        """Navigate to the URL entered in the URL bar."""
        current_browser: QWidget = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            url: str = self.url_bar.text()
            current_browser.setUrl(url)

    def update_url_bar(self, url: QUrl) -> None:
        """Update the URL bar with the current URL."""
        self.url_bar.setText(url.toString())

    def show_context_menu(self, position: QPoint) -> None:
        """Show the context menu on right-click."""
        context_menu = QMenu(self)
        close_tab_action = context_menu.addAction("Close Tab")
        close_tab_action.triggered.connect(lambda: self.close_current_tab(self.tabs.tabBar().tabAt(position)))
        context_menu.exec(self.tabs.mapToGlobal(position))


def main() -> None:
    """Run the browser."""
    app = QApplication([])

    window = Browser()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
