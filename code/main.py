import sys
import os
import subprocess
import pygame
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QTimer

class TempCleanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        pygame.mixer.init()

    def init_ui(self):
        self.setWindowIcon(QIcon(self.resource_path("assets/tm.ico")))
        self.setWindowTitle("Temp Clean")
        self.setGeometry(100, 100, 800, 450)
        self.setFixedSize(800, 450)

        self.bg_label = QLabel(self)
        pixmap = QPixmap(self.resource_path("assets/background.png"))
        if pixmap.isNull():
            print("Error: Background image not found!")
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)
        self.bg_label.setGeometry(0, 0, 800, 450)
        self.bg_label.lower()

        self.clean_button = QPushButton("CLEAN NOW", self)
        button_width = 200
        button_height = 70
        button_x = (self.width() - button_width) // 2 + 100
        button_y = (self.height() - button_height) // 2
        self.clean_button.setGeometry(button_x, button_y, button_width, button_height)

        self.clean_button.setStyleSheet(""" 
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C8FFE6, stop:1 #78B4FF);
                color: white;
                border-radius: 20px;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #A8E6C8, stop:1 #5C9EFF);
            }
        """)

        self.clean_button.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.clean_button.clicked.connect(self.clean_action)

        self.credits = QLabel('<a href="https://github.com/Shiruuukawa" style="color: black; text-decoration: none;"><b><u>by Shirukawa</u></b></a>', self)
        self.credits.setOpenExternalLinks(True)
        self.credits.setFont(QFont("Arial", 10))
        self.credits.setStyleSheet("color: black; text-decoration: none;")
        self.credits.move(10, 430)

        self.fade_in_animation()
        self.show()

    def resource_path(self, relative_path):
        """Get the absolute path of the bundled resources in the EXE."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def fade_in_animation(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()

    def clean_action(self):
        self.clean_button.setText("Cleaning...")
        self.clean_button.setEnabled(False)

        subprocess.run(["clean.bat"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

        QTimer.singleShot(2000, self.clean_completed)

    def clean_completed(self):
        self.clean_button.setText("✔ Cleaned!")
        self.clean_button.setStyleSheet("background-color: #4CAF50; color: white;")

        pygame.mixer.music.load(self.resource_path("assets/notification.wav"))
        pygame.mixer.music.play()

        QTimer.singleShot(3000, self.reset_button)

    def reset_button(self):
        self.clean_button.setText("CLEAN NOW")
        self.clean_button.setStyleSheet(""" 
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #C8FFE6, stop:1 #78B4FF);
                color: white;
                border-radius: 20px;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #A8E6C8, stop:1 #5C9EFF);
            }
        """)
        self.clean_button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TempCleanApp()
    sys.exit(app.exec())
