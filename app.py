import sys
import time

from PyQt5.QtCore import QSize, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        for i in range(10):
            self.progress.emit(i + 1)
            time.sleep(1)
        self.finished.emit()


class Window(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.worker = None
        self.thread = None
        self.clicks = 0
        self.setWindowTitle("HR Analysis")
        self.resize(QSize(400, 300))

        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.button = QPushButton('Collect data')
        self.button.clicked.connect(self.collect_data)

        self.button2 = QPushButton('Save to file (.csv)')
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.btn_clicked)
        
        self.label = QLabel('Step: 0')
        self.label2 = QLabel('Clicks: 0')

        v_box = QVBoxLayout(widget)
        v_box.addWidget(self.button)
        v_box.addWidget(self.label)
        v_box.addWidget(self.button2)
        v_box.addWidget(self.label2)
        
    def collect_data(self):
        self.button.setEnabled(False)
        self.button2.setEnabled(False)

        self.thread = QThread()
        self.worker = Worker()

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        self.worker.progress.connect(lambda i: self.label.setText(f"Step: {i}"))

        self.thread.finished.connect(self.clear_labels)
        self.thread.finished.connect(self.toggle_available_btn)

    def toggle_available_btn(self):
        self.button.setEnabled(True)
        self.button2.setEnabled(True)

    def clear_labels(self):
        self.label.setText("Step: 0")
        self.label2.setText("Clicks: 0")
        self.clicks = 0

    def btn_clicked(self):
        self.clicks += 1
        self.label2.setText(f'Clicks: {self.clicks}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())
