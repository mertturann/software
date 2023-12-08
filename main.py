import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QListWidget, QRadioButton, QFileDialog
from PyQt6.QtCore import QFile
from functions import list_folders
from PyQt6.uic import loadUi

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI dosyasını yükle
        self.load_ui()
        self.initUiElements()
        self.interactions()

    def load_ui(self):
        # UI dosyasını yükleme
        loadUi("main.ui", self)

    def initUiElements(self):
        self.analiz = self.findChild(QListWidget, "listWidget")
        self.deprem = self.findChild(QListWidget, "listWidget_2")
        self.layer = self.findChild(QListWidget, "listWidget_3")
        self.browse = self.findChild(QPushButton, "pushButton")
        self.run = self.findChild(QPushButton, "pushButton_2")
        self.radio_analiz = self.findChild(QRadioButton, "radioButton")
        self.radio_deprem = self.findChild(QRadioButton, "radioButton_2")

    def interactions(self):
            self.browse.clicked.connect(self.browsedir)
      

    def check_radio_buttons(self):
        if self.radio_analiz.isChecked():
            print("Analiz radyo düğmesi seçildi.")
        elif self.radio_deprem.isChecked():
            print("Deprem radyo düğmesi seçildi.")
        else:
            print("Hiçbir radyo düğmesi seçilmedi.")


    def browsedir(self):
        HOME_PATH = os.path.expanduser('~\Documents\DEEPSOIL 7')
        self.browse = QFileDialog.getExistingDirectory(self,directory=HOME_PATH)
        print (self.browse)
        folders = list_folders(self.browse)
        self.analiz.addItems(folders)
        
def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
