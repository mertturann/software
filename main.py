import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QListWidget, QRadioButton, QFileDialog, QMessageBox
from PyQt6.QtCore import QFile
from PyQt6.QtGui import QIcon
from functions import list_folders, list_files, get_layers, getcurrentime, check_files
from PyQt6.uic import loadUi
from draw import multi_analysis, draw_combined_graph, draw_test, multi_deprem, draw_deprem
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

        self.setWindowIcon(QIcon("icon.png")) 
        self.setWindowTitle("DeepSoil Analiz")

    def initUiElements(self):
        self.analiz = self.findChild(QListWidget, "listWidget")
        self.deprem = self.findChild(QListWidget, "listWidget_2")
        self.layer = self.findChild(QListWidget, "listWidget_3")
        self.browse = self.findChild(QPushButton, "pushButton")
        self.draw = self.findChild(QPushButton, "pushButton_2")
        self.temizle = self.findChild(QPushButton, "pushButton_3")
        self.radio_analiz = self.findChild(QRadioButton, "radioButton_2")
        self.radio_deprem = self.findChild(QRadioButton, "radioButton")
        self.radio_layer = self.findChild(QRadioButton, "radioButton_3")
        


    def interactions(self):
            self.trigger_radio()
            self.browse.clicked.connect(self.browsedir)
            self.analiz.currentItemChanged.connect(self.init_analiz)
            self.deprem.currentItemChanged.connect(self.init_layer)
            self.radio_analiz.clicked.connect(self.trigger_radio)
            self.radio_deprem.clicked.connect(self.trigger_radio)
            self.radio_layer.clicked.connect(self.trigger_radio)
            self.draw.clicked.connect(self.run)
    
     
    def trigger_radio(self):
        if self.radio_analiz.isChecked():
            QMessageBox.information(self, "Bilgi", "Analiz Modundasınız, Bu modda birden çok analiz, bir deprem, bir layer seçebilirsiniz.")
            self.deprem.clear()
            self.layer.clear()
            self.analiz.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            self.deprem.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
            self.layer.setSelectionMode(QListWidget.SelectionMode.SingleSelection)  
        elif self.radio_deprem.isChecked():
            QMessageBox.information(self, "Bilgi", "Deprem Modundasınız, Bu modda yalnızca bir analiz, birden çok deprem, ve bir layer seçebilirsiniz.")
            self.deprem.clear()
            self.layer.clear()
            self.analiz.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
            self.deprem.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            self.layer.setSelectionMode(QListWidget.SelectionMode.SingleSelection)  
        elif self.radio_layer.isChecked():
            QMessageBox.information(self, "Bilgi", "Layer Modundasınız, Bu modda yalnızca bir analiz, bir deprem, birden çok layer seçebilirsiniz.")
            self.deprem.clear()
            self.layer.clear()
            self.analiz.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
            self.deprem.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
            self.layer.setSelectionMode(QListWidget.SelectionMode.MultiSelection)  
        else:
            print("...")    


    def browsedir(self):
        self.analiz.clear()
        HOME_PATH = os.path.expanduser('~\\Documents\\DEEPSOIL 7')
        self.browse = QFileDialog.getExistingDirectory(self,directory=HOME_PATH)
        folders = list_folders(self.browse)
        self.analiz.addItems(folders)

    def run(self):
        if self.radio_analiz.isChecked():
            self.draw_multi_analysis()
        elif self.radio_deprem.isChecked():
            self.draw_multi_deprem()    
            
    
    def draw_multi_analysis(self):
        dirs = []
        labels = []
        layer = (self.layer.selectedItems()[0]).text()
        deprem = (self.deprem.selectedItems()[0]).text()
        selected_items = self.analiz.selectedItems()
        basedir = self.browse
        for item in selected_items:
            if not check_files(folder=f"{basedir}/{item.text()}",file=deprem):
                QMessageBox.critical(self,"Hata",f"{basedir}/{item.text()} Dizininde {deprem} dosyası yok. ANALİZ BAŞLAMAYACAK.")
                return
            else:    
                dirs.append(f"{basedir}/{item.text()}")               
        for label in selected_items:
            labels.append(label.text())
        y, input_motion = multi_analysis(folders=dirs,deprem=deprem,layer=layer,column="PSA (g)")
        draw_test(y_values=y,graphname=getcurrentime(),title=deprem,input_motion=input_motion,labels=labels) 

    def draw_multi_deprem(self):
        path = self.browse
        layer = (self.layer.selectedItems()[0]).text()
        dizin = (self.analiz.selectedItems()[0]).text()
        folder = f"{path}/{dizin}"
        depremler = self.deprem.selectedItems()
        secili_depremler = [item.text() for item in depremler]
        labels = [((item.text()).replace("Results_profile_0_motion_A-","")).replace(".xlsx","") for item in depremler]                         
        sonuclar = multi_deprem(folder_path=folder,file_names=secili_depremler,sheet_name=layer,column_name="PSA (g)")
        print (sonuclar)
        draw_deprem(y_values=sonuclar,graphname=getcurrentime(),title=f"Analiz: {dizin}, Layer: {layer}",labels=labels)
        


    def init_analiz(self):
        self.deprem.clear()
        text = self.analiz.currentItem()
        filespath = f"{self.browse}/{text.text()}"
        files = list_files(filespath)
        self.deprem.addItems(files)

    def init_layer(self):
        self.layer.clear()
        analiz = self.analiz.currentItem()
        deprem = self.deprem.currentItem()
        if analiz is not None and deprem is not None:
            path = f"{self.browse}/{analiz.text()}/{deprem.text()}"
            layers = get_layers(path)
            self.layer.addItems(layers)
        else:
            return
        
        
def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
