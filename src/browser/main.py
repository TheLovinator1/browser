from PySide6.QtCore import QSize
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


def main() -> None:
    app = QApplication([])

    window = QMainWindow()
    window.setWindowTitle("Blue Archive watching machine")

    # Set window size to screen size
    screensize: QSize = window.screen().size() * window.screen().devicePixelRatio()
    window.resize(int(screensize.width() * 0.8), int(screensize.height() * 0.8))
    window.showMaximized()

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    browser = QWebEngineView()
    browser.setUrl("https://duckduckgo.com")

    layout.addWidget(browser)
    window.setCentralWidget(central_widget)

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
