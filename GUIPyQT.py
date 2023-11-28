import os
import sys
import ctypes
from typing import Union
from general_downloader import run_main
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QPlainTextEdit, \
    QPushButton, QApplication, QWidget, QLabel


def open_file(msg, path):
    print(msg)
    os.startfile(path)


def open_folder(msg, path):
    print(msg)
    os.system(path)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 300
        self.initialisation_ui()
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.title = 'Ежедневное скачивание сигналов'
        self.setWindowTitle(self.title)

    def initialisation_ui(self):
        self.show_start_button = QPushButton('🚀 Запуск', self)
        self.show_start_button.setFont(QFont('Arial', 14))
        self.show_start_button.setFixedSize(315, 36)
        self.show_start_button.move(20, 125)
        self.show_start_button.clicked.connect(self.main_proc)

        self.show_input_excel_button = QPushButton('   🧾 Открыть excel lifefinance', self)
        self.show_input_excel_button.setStyleSheet("text-align: left;")
        self.show_input_excel_button.setFont(QFont('Arial', 14))
        self.show_input_excel_button.setFixedSize(315, 36)
        self.show_input_excel_button.move(20, 125)
        self.show_input_excel_button.clicked.connect(lambda: open_file(
            "Открываю excel файл, где хранится список ссылок для lifefinance\n",
            rf"{current_dir}\resources\БАЗА ДАННЫХ\litefinance hrefs.xlsx"))

        self.show_input_excel_button1 = QPushButton('   🧾 Открыть excel forex4you', self)
        self.show_input_excel_button1.setStyleSheet("text-align: left;")
        self.show_input_excel_button1.setFont(QFont('Arial', 14))
        self.show_input_excel_button1.setFixedSize(315, 36)
        self.show_input_excel_button1.move(20, 125)
        self.show_input_excel_button1.clicked.connect(lambda: open_file(
            "Открываю excel файл, где хранится список ссылок для forex4you\n",
            rf"{current_dir}\resources\БАЗА ДАННЫХ\forex4you hrefs.xlsx"))

        self.show_log_button = QPushButton('   🧾 Открыть логи', self)
        self.show_log_button.setStyleSheet("text-align: left;")
        self.show_log_button.setFont(QFont('Arial', 14))
        self.show_log_button.setFixedSize(315, 36)
        self.show_log_button.move(20, 125)
        self.show_log_button.clicked.connect(lambda: open_file(
            "Открываю log файл, где хранятся ошибки работы робота", rf"{current_dir}\main.log"))

        self.show_output_excel_button = QPushButton('   📁 Открыть папку lifefinance', self)
        self.show_output_excel_button.setFont(QFont('Arial', 14))
        self.show_output_excel_button.setStyleSheet("text-align: left;")
        self.show_output_excel_button.setFixedSize(315, 36)
        self.show_output_excel_button.move(20, 181)
        self.show_output_excel_button.clicked.connect(lambda: open_folder(
            "Открываю директорию, где хранятся сформированные файлы excel\n",
            rf"explorer.exe {current_dir}\resources\БАЗА ДАННЫХ\litefinance"))

        self.show_output_htm_button = QPushButton('   📂 Открыть папку forex4you', self)
        self.show_output_htm_button.setFont(QFont('Arial', 14))
        self.show_output_htm_button.setStyleSheet("text-align: left;")
        self.show_output_htm_button.setFixedSize(315, 36)
        self.show_output_htm_button.move(20, 237)
        self.show_output_htm_button.clicked.connect(lambda: open_folder(
            "Открываю директорию, где хранятся сформированные файлы htm\n",
            fr"explorer.exe {current_dir}\resources\БАЗА ДАННЫХ\forex4you"))

        self.text_edit = QPlainTextEdit()
        self.text_edit.setFixedSize(315, 315)
        self.text_edit.setFont(QFont('Arial', 8))
        sys.stdout = self

        vbox = QGridLayout()
        vbox.setSpacing(10)
        vbox.addWidget(self.show_input_excel_button, 1, 0)
        vbox.addWidget(self.show_input_excel_button1, 2, 0)
        vbox.addWidget(self.show_output_excel_button, 3, 0)
        vbox.addWidget(self.show_output_htm_button, 4, 0)
        vbox.addWidget(self.show_start_button, 6, 0)
        vbox.addWidget(self.show_log_button, 5, 0)
        vbox.addWidget(self.text_edit, 7, 0)
        self.setLayout(vbox)
        self.show()

    def write(self, text):
        self.text_edit.insertPlainText(text)

    def main_proc(self):
        run_main()


console_window = ctypes.windll.kernel32.GetConsoleWindow()
ctypes.windll.user32.ShowWindow(console_window, 6)  # скрываем консоль при запуске из батника

current_dir = os.path.dirname(os.path.abspath(__file__))

app = QApplication(sys.argv)
app.setStyle('Fusion')
ex = App()
ex.setFixedSize(400, 660)
ex.show()
sys.exit(app.exec_())
