import sys
from os import walk
from shutil import copyfile
from os import listdir
from os.path import isfile, join
from PyQt5.QtCore import QEventLoop, QTime
from PyQt5.QtWidgets import (QWidget, QToolTip, QGridLayout,
    QPushButton, QApplication, QFileDialog, QVBoxLayout, QLineEdit, QHBoxLayout, QTextEdit)
from PyQt5 import QtGui


class Harvester(QWidget):
    def __init__(self):
        super().__init__()
        self.storage = Storage()
        self.load()
        self.initUI()

    def initUI(self):
        path_btn = self.register_file_button()
        file_btn = self.register_path_button()
        save_btn = self.register_save_button()
        run_btn = self.register_run_button()

        self.paths = QTextEdit(self)
        self.paths.setReadOnly(True)
        self.path_widget_update()

        self.files = QTextEdit(self)
        self.files.setReadOnly(True)
        self.file_widget_update()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(path_btn, 1, 0)
        grid.addWidget(file_btn, 1, 1)
        grid.addWidget(self.files, 2, 0, 1, 2)
        grid.addWidget(self.paths, 3, 0, 1, 2)
        grid.addWidget(save_btn, 4, 0)
        grid.addWidget(run_btn, 4, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Harvester')
        self.show()

    def register_path_button(self):
        btn = QPushButton('Add destination', self)
        btn.clicked.connect(self.path_selector)
        btn.setToolTip('Add directory to put files in')
        btn.resize(btn.sizeHint())
        return btn

    def register_file_button(self):
        btn = QPushButton('Add source', self)
        btn.clicked.connect(self.file_selector)
        btn.setToolTip('Add directory to get files from')
        btn.resize(btn.sizeHint())
        return btn

    def register_save_button(self):
        btn = QPushButton('Save', self)
        btn.clicked.connect(self.save)
        btn.setToolTip('Save options')
        btn.resize(btn.sizeHint())
        return btn

    def register_run_button(self):
        btn = QPushButton('Run', self)
        btn.clicked.connect(self.run)
        btn.setToolTip('Run copying')
        btn.resize(btn.sizeHint())
        return btn

    def run(self):
        for f in self.storage.files:
            for filename in listdir(f):
                if isfile(join(f,filename)):
                    for d in self.storage.dirs:
                        copyfile(join(f, filename), join(d, filename))

    def save(self):
        content = ['', '']
        content[0] = '===sub==='.join(self.storage.files)
        content[1] = '===sub==='.join(self.storage.dirs)
        content = '===main==='.join(content)
        with open('.options', 'w') as file:
            file.write(content)

    def load(self):
        with open('.options', 'r') as file:
            content = file.read()
        if content:
            content = content.split('===main===')
            self.storage.files = content[0].split('===sub===')
            self.storage.dirs = content[1].split('===sub===')

    def path_selector(self):
        self.storage.dirs.append(str(QFileDialog.getExistingDirectory(self, "Select Directory")))
        self.path_widget_update()

    def path_widget_update(self):
        text = ''
        for d in self.storage.dirs:
            text += d + '\n'
        self.paths.setPlainText(text)

    def file_selector(self):
        self.storage.files.append(str(QFileDialog.getExistingDirectory(self, "Select File")))
        self.file_widget_update()

    def file_widget_update(self):
        text = ''
        for d in self.storage.files:
            text += d + '\n'
        self.files.setPlainText(text)

class Storage:
    def __init__(self):
        self.files = []
        self.dirs = []


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Harvester()

    sys.exit(app.exec_())