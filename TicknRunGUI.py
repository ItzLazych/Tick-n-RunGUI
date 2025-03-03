import webbrowser
import os, sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QScrollArea, QAction, QMessageBox, QFileDialog, QApplication
import pyperclip

class Blitz(QtWidgets.QMainWindow):
    def __init__(self, ** kwargs):
        super().__init__(**kwargs)
        self.textbox = QtWidgets.QTextEdit()

        self.textbox.setFont(QtGui.QFont('Consolas',11))

        self.count_ren = True
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.textbox)
        icon_path = os.path.join(sys._MEIPASS, 'IconTNR.ico')
        self.setWindowIcon(QIcon(icon_path))

        self.setCentralWidget(self.scroll)
        self.initUI()

    def initUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Файл')
        helpMenu = menubar.addMenu('Справка')

        copyFile_txt = QAction('Скопировать в буфер обмена', self)
        copyFile_txt.triggered.connect(self.copy_to_clipboard_as_txt)
        fileMenu.addAction(copyFile_txt)
        saveFile_txt = QAction('Сохранить файлом (.txt)', self)
        saveFile_txt.triggered.connect(self.save_file_as_txt)
        fileMenu.addAction(saveFile_txt)
        self.progressplus = QAction('Вставлять "+" в конце строки', self)
        self.progressplus.setCheckable(True)
        self.progressplus.setChecked(False)
        fileMenu.addAction(self.progressplus)
######################################################################
        helpMenu.addSeparator()

        about = QAction('О программе', self)
        about.triggered.connect(self.program_info)
        helpMenu.addAction(about)

        gethoob = QAction('Github страница', self)
        gethoob.triggered.connect(self.gethoob_web)
        helpMenu.addAction(gethoob)

        donatik = QAction('Поддержать разработчика', self)
        donatik.triggered.connect(self.donatik_web)
        helpMenu.addAction(donatik)

        self.setWindowTitle("Tick'n'RunGUI")
        self.show()

    def gethoob_web(self):
        webbrowser.open(f'https://github.com/ItzLazych/Tick-n-RunGUI', new=0)

    def donatik_web(self):
        webbrowser.open(f'https://www.donationalerts.com/r/itzlazych', new=0)

    def program_info(self):
        QMessageBox.information(self, "Tick'n'Run: сведения", "Программа для составления Tick'n'Run (Блицкриг) таблицы v0.4. Разработчик: Хилажев Артур (ItzLazych). Язык - Python (PyQt5)")

    def blitzkreig_generator(self):
        data = self.textbox.toPlainText()
        startpos = [int(num) for num in data.split("\n")]
        startpos.append(100)
        startpos.append(0)
        startpos = list(set(startpos))
        startpos.sort()
        startpos.reverse()
        num_startpos = len(startpos) - 2
        blitz = ""
        for stage in range(1, num_startpos + 1):
            blitz = blitz + f"Stage {stage}\n"
            for i in range(len(startpos) - stage):
                if self.progressplus.isChecked() and startpos[i] != 100:
                    blitz = blitz + f"{startpos[i + stage]} - {startpos[i]}+\n"
                else:
                    blitz = blitz + f"{startpos[i + stage]} - {startpos[i]}\n"
        blitz = blitz + f"Stage {stage + 1}\n0 - 100"
        return blitz


    def save_file_as_txt(self):

        fname, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', '', 'Все файлы (*);;Текстовые файлы (*.txt)')
        if fname:
            with open(fname, 'w', encoding='utf-8') as f:

                f.write(self.blitzkreig_generator())

    def copy_to_clipboard_as_txt(self):
        pyperclip.copy(self.blitzkreig_generator())



if __name__ == '__main__':
    app = QApplication([])
    blitz = Blitz()
    app.exec_()
