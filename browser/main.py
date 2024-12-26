from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, cast

from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QMessageBox, QTabWidget, QToolBar, QWidget

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
        self.create_shortcuts()
        self.create_menu()

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

    def create_toolbar(self) -> None:
        """Create the toolbar with navigation actions."""
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.add_new_tab("https://duckduckgo.com", "New Tab"))
        toolbar.addAction(new_tab_action)

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

    def create_menu(self) -> None:
        """Create the menu bar with a help menu."""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        help_menu: QMenu = menu_bar.addMenu("Help")

        shortcuts_action = QAction("Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

    def show_shortcuts(self) -> None:
        """Show a message box with the keyboard shortcuts silently."""
        import logging

        logging.info("Displaying keyboard shortcuts silently.")
        shortcuts: str = (
            "Ctrl+T: Open a new tab\n"
            "Ctrl+W: Close the current tab\n"
            "Ctrl+Q: Close the browser\n"
            "Ctrl+R: Reload the current tab"
        )
        try:
            self.display_keyboard_shortcuts(shortcuts)
        except Exception:
            logging.exception("Failed to display shortcuts")

    def display_keyboard_shortcuts(self, shortcuts: str) -> None:
        """Display the keyboard shortcuts in a message box."""
        msg: QMessageBox = QMessageBox(self)
        msg.setWindowTitle("Keyboard Shortcuts")
        msg.setIcon(QMessageBox.Icon.NoIcon)
        msg.setText(shortcuts)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


def main() -> None:
    """Run the browser."""
    app = QApplication([])

    window = Browser()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
