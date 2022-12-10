from PyQt5.QtWidgets import *
from view2 import *
import main2

excel = "excel"
csv = "csv"

class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.setupUi(self)
        self.buttonExcel.clicked.connect(lambda: self.excel())
        self.buttonCSV.clicked.connect(lambda: self.csv())
        self.radMovie.setChecked(True)

    def excel(self):

        if self.radMovie.isChecked():
            main2.scrapeMovie(excel)
        else:
            main2.scrapeBook(excel)
    def csv(self):
        if self.radMovie.isClicked():
            main2.scrapeMovie(csv)
        else:
            main2.scrapeBook(csv)
