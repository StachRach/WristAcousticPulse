import sys
import os

from PyQt5.QtCore import QSize, QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog

from data_aquisition import data_aquisition, save_to_file


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        self.temp = data_aquisition(150, 0.2)
        self.progress.emit(self.temp)
        self.finished.emit()


class Window(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.worker = None
        self.thread = None
        self.data = None
        self.setWindowTitle("HR Analysis")
        self.resize(QSize(400, 300))

        widget = QWidget(self)
        self.setCentralWidget(widget)

        self.button = QPushButton('Collect data')
        self.button.clicked.connect(self.collect_data)

        self.button2 = QPushButton('Save to file (.csv)')
        self.button2.setEnabled(False)
        self.button2.clicked.connect(self.btn_clicked)
        
        self.label = QLabel('Data will appear here.')
        self.label2 = QLabel('')

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

        self.worker.progress.connect(self.show_last_five)

        self.thread.finished.connect(self.toggle_available_btn)

    def show_last_five(self, d):
        self.data = d
        self.label.setText(f'{d[-5]}\n{d[-4]}\n{d[-3]}\n{d[-2]}\n{d[-1]}\n')

    def toggle_available_btn(self):
        self.button.setEnabled(True)
        self.button2.setEnabled(True)

    def btn_clicked(self):
        fileName, _ = QFileDialog.getSaveFileName(self,"Save",os.getcwd(),"CSV Files (*.csv)")

        try:
            save_to_file(self.data, fileName)
            self.label2.setText(f'Data have been saved as .csv file.')
        except:
            self.label2.setText(f'An error occured while saving data.')
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())
