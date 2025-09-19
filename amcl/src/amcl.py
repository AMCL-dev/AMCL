import sys

from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QLabel, QVBoxLayout, QWidget)

from harmony_ui.harmony_card import HarmonyCard
def main():

    print("PySide6已成功加载!")
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("AMCL")
    window.setGeometry(100, 100, 800, 600)

    central_widget = QWidget()
    layout = QVBoxLayout()

    label = QLabel("您的应用已成功启动!<br>")
    label.setWordWrap(True)
    layout.addWidget(label)

    harmony_card = HarmonyCard()
    layout.addWidget(harmony_card)

    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    window.show()

    return app.exec()

if __name__ == "__main__":
    sys.exit(main())