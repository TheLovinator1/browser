from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QTabWidget,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from PySide6.QtCore import QPoint, QSize, QUrl

logging.basicConfig(level=logging.INFO)


class Browser(QMainWindow):
    """Main window of the browser."""

    def __init__(self) -> None:
        """Initialize the browser."""
        super().__init__()
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
        self.add_new_tab("about:blank", "Blank")

        self.create_shortcuts()
        self.add_new_tab_button()

    def resize_and_maximize_window(self) -> None:
        """Resize the window to 80% of the screen size and maximize it."""
        screensize: QSize = self.screen().size() * self.screen().devicePixelRatio()
        self.resize(int(screensize.width() * 0.8), int(screensize.height() * 0.8))
        self.showMaximized()

    def add_new_tab(self, url: str, label: str) -> None:
        """Add a new tab with the given URL and label."""
        view = QWebEngineView()
        view.setUrl(url)
        # view.urlChanged.connect(self.update_url_bar)
        view.titleChanged.connect(lambda title: self.update_tab_and_window_title(view, title))

        tab_index: int = self.tabs.addTab(view, label)
        self.tabs.setCurrentIndex(tab_index)

    def build_github_data_display_page(self, github_username: str, github_repo: str) -> QWidget:
        """Create a custom page to display GitHub data."""
        custom_page = QWidget()
        layout = QVBoxLayout()

        try:
            self.build_github_repo_contents_display(github_username, github_repo, layout)
        except requests.RequestException:
            error_label = self._create_error_label("Failed to fetch data", "Failed to fetch data from the API.")
            layout.addWidget(error_label)

        custom_page.setLayout(layout)
        custom_page.setStyleSheet("background-color: #222; color: white;")
        return custom_page

    def build_github_repo_contents_display(self, github_username: str, github_repo: str, layout: QVBoxLayout) -> None:
        """Build the display for the contents of a GitHub repository."""
        response: requests.Response = requests.get(
            url=f"http://localhost:8000/api/github/repos/{github_username}/{github_repo}/contents/",
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()

        # Add GitHub/username/repo on top of the page
        title_label = QLabel(f"<h1>GitHub/{github_username}/{github_repo}</h1>")
        layout.addWidget(title_label)

        list_widget = QListWidget()
        for item in data:
            self.add_github_item_display(list_widget, item)
        layout.addWidget(list_widget)

    def add_github_item_display(self, list_widget: QListWidget, item: dict[str, str]) -> None:
        """Add a label to the layout with information about a GitHub item."""
        size_info: str = f" ({item['size']} bytes)" if int(item["size"]) > 0 else ""
        list_item = QListWidgetItem(f"{item['name']}{size_info} ({item['sha']})")
        list_widget.addItem(list_item)

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
        else:
            self.setWindowTitle(self.tabs.tabText(index))

    def update_tab_and_window_title(self, view: QWebEngineView, title: str) -> None:
        """Update the tab and window title based on the web page title."""
        index: int = self.tabs.indexOf(view)
        if index != -1:
            self.tabs.setTabText(index, title)
            if self.tabs.currentWidget() == view:
                self.setWindowTitle(title)

    def create_shortcuts(self) -> None:
        """Create keyboard shortcuts for various actions."""
        close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab_shortcut.activated.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))

        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(lambda: self.add_new_tab("about:blank", "New Tab"))

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
        new_tab_button.clicked.connect(lambda: self.add_new_tab("about:blank", "New Tab"))
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
            self.load_github_repo_page(url)
            current_browser.setUrl(url)

    def load_github_repo_page(self, url: str) -> None:
        """Load a custom page for a GitHub repository if the URL matches the expected format."""
        if not url.startswith("GitHub/"):
            return
        try:
            self._create_github_repo_tab(url)
        except ValueError:
            error_label = self._create_error_label(
                "Invalid GitHub URL format",
                "Invalid GitHub URL format. Expected format: GitHub/username/repo",
            )
            current_layout: QLayout | None = self.tabs.currentWidget().layout()
            if current_layout is not None:
                current_layout.addWidget(error_label)
            else:
                logging.exception("Current widget has no layout to add the error label.")

    def _create_error_label(self, exception_message: str, error_message: str) -> QLabel:
        logging.exception(exception_message)
        result = QLabel(error_message)
        result.setStyleSheet("color: red;")
        return result

    def _create_github_repo_tab(self, url: str) -> None:
        """Create a new tab for the GitHub repository and set the URL bar."""
        _, github_username, github_repo = url.split("/", 2)
        custom_page: QWidget = self.build_github_data_display_page(
            github_username=github_username,
            github_repo=github_repo,
        )
        current_index: int = self.tabs.currentIndex()
        self.tabs.removeTab(current_index)
        self.tabs.insertTab(current_index, custom_page, f"GitHub/{github_username}/{github_repo}")
        self.tabs.setCurrentIndex(current_index)
        self.setWindowTitle(f"GitHub/{github_username}/{github_repo}")
        self.url_bar.setText(f"GitHub/{github_username}/{github_repo}")

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
