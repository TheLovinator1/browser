from PySide6.QtCore import QSize
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class Browser(QMainWindow):
    def __init__(self) -> None:
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
        self.setWindowTitle("Blue Archive watching machine")

    def resize_and_maximize_window(self) -> None:
        screensize: QSize = self.screen().size() * self.screen().devicePixelRatio()
        self.resize(int(screensize.width() * 0.8), int(screensize.height() * 0.8))
        self.showMaximized()


def main() -> None:
    app = QApplication([])

    window = Browser()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
