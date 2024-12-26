from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from PySide6.QtCore import QCoreApplication
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
    assert browser.windowTitle() == "web browser"
    assert browser.browser.url().toString() == "https://duckduckgo.com"


def test_browser_resize_and_maximize(browser: Browser) -> None:
    """Test the resize and maximize functionality of the Browser."""
    screensize: QSize = browser.screen().size() * browser.screen().devicePixelRatio()
    expected_width = int(screensize.width() * 0.8)
    expected_height = int(screensize.height() * 0.8)

    assert browser.width() == expected_width
    assert browser.height() == expected_height
    assert browser.isMaximized()


def test_browser_set_window_title(browser: Browser) -> None:
    """Test the set_window_title method of the Browser."""
    browser.set_window_title()
    assert browser.windowTitle() == "web browser"
