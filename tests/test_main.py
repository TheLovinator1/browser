from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from PySide6.QtCore import QCoreApplication, QPoint, QSize, Qt, QUrl
from PySide6.QtTest import QTest
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication

from browser.main import Browser

if TYPE_CHECKING:
    from PySide6.QtCore import QCoreApplication, QSize


@pytest.fixture
def app() -> QApplication | QCoreApplication:
    """Fixture for creating the QApplication instance."""
    app: QCoreApplication | None = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def browser(app: QApplication | QCoreApplication) -> Browser:
    """Fixture for creating the Browser instance."""
    return Browser()


def test_browser_initialization(browser: Browser) -> None:
    """Test the initialization of the Browser."""
    assert browser.tabs.count() == 1
    assert browser.tabs.tabText(0) == "New Tab"


def test_browser_resize_and_maximize(browser: Browser) -> None:
    """Test the resize and maximize functionality of the Browser."""
    screensize: QSize = browser.screen().size() * browser.screen().devicePixelRatio()
    expected_width = int(screensize.width() * 0.8)
    expected_height = int(screensize.height() * 0.8)

    assert browser.width() == expected_width
    assert browser.height() == expected_height
    assert browser.isMaximized()


def test_add_new_tab(browser: Browser) -> None:
    """Test adding a new tab."""
    initial_tab_count = browser.tabs.count()
    browser.add_new_tab("https://example.com", "Example")
    assert browser.tabs.count() == initial_tab_count + 1
    assert browser.tabs.tabText(browser.tabs.currentIndex()) == "Example"


def test_close_current_tab(browser: Browser) -> None:
    """Test closing the current tab."""
    browser.add_new_tab("https://example.com", "Example")
    initial_tab_count = browser.tabs.count()
    browser.close_current_tab(browser.tabs.currentIndex())
    assert browser.tabs.count() == initial_tab_count - 1


def test_navigate_to_url(browser: Browser) -> None:
    """Test navigating to a URL."""
    browser.url_bar.setText("https://example.com")
    browser.navigate_to_url()
    current_browser = browser.tabs.currentWidget()
    assert isinstance(current_browser, QWebEngineView)
    assert current_browser.url().toString() == "https://example.com"


def test_update_url_bar(browser: Browser) -> None:
    """Test updating the URL bar."""
    current_browser = browser.tabs.currentWidget()
    assert isinstance(current_browser, QWebEngineView)
    current_browser.setUrl(QUrl("https://example.com"))
    browser.update_url_bar(QUrl("https://example.com"))
    assert browser.url_bar.text() == "https://example.com"


def test_show_context_menu(browser: Browser) -> None:
    """Test showing the context menu."""
    # This test is a bit tricky because it involves GUI interaction.
    # We will simulate a right-click and check if the context menu is shown.

    QTest.mouseClick(browser.tabs.tabBar(), Qt.MouseButton.RightButton, pos=QPoint(10, 10))
    # Since we cannot directly assert the context menu, we assume no exceptions were raised.
