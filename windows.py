from forms import pril_nir
from line_forms import OneLine, Drop ,AddLineForm,Updatingline
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtCore import Qt
from db import *

class TableClass():
    cRow = -1
    cRec = ("", "")
    wparent = None

    def setColortoRow(self, table, rowIndex, b_color, f_color):
        for j in range(table.columnCount()):
            table.item(rowIndex, j).setBackground(b_color)
            table.item(rowIndex, j).setForeground(f_color)

    def rowselection(self):
        r = self.tableWidget.currentRow()
        self.selectirow(r)

    def selectirow(self, r):
        try:
            self.setColortoRow(self.tableWidget, r, QtGui.QColor(0x0000FF),QtGui.QColor(0xFFFFFF))
            if self.cRow != -1 and self.cRow != r:
                self.setColortoRow(self.tableWidget, self.cRow, QtGui.QColor(0xFFFFFF),QtGui.QColor(0x000000))
            self.cRow = r
            if QtWidgets.QMainWindow in self.__class__.__bases__:
                self.statusBar().showMessage(f'Строка {r + 1}')
                self.cRec = (self.tableWidget.item(r, 0).text(), self.tableWidget.item(r, 1).text())
                # print(self.cRec)
        except BaseException:
            print("something wrong! try again")
            return

    def FillTable(self, table):
        if len(table) == 0:
            print("empty table")
            self.tableWidget.setRowCount(0)
            return

        n, m = len(table[0]), len(table)

        self.tableWidget.setRowCount(m)
        for i in range(0, m):
            j = 0
            for cname in table[0].keys():
                item = QtWidgets.QTableWidgetItem(str(table[i][cname]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)
                j += 1

    def SetUpTable(self, table):
        n, m = len(table[0]), len(table)
        self.tableWidget.setColumnCount(n)
        # self.tableWidget.setHorizontalHeaderLabels(GetTupleOfFullName(table[0].keys()))
        self.tableWidget.setHorizontalHeaderLabels(table[0].keys())

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.verticalHeader().setVisible(False)

        self.tableWidget.clicked.connect(self.rowselection)
        self.FillTable(table)

    def closeEvent(self, event):

        if "mdi" in dir(self.wparent):
            self.wparent.mdi.closeAllSubWindows()


class MainWindow(QtWidgets.QMainWindow, pril_nir.Ui_MainWindow, TableClass):


    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.action.triggered.connect(self.open)
        self.action_2.triggered.connect(self.open2)
        self.action_3.triggered.connect(self.open3)
        self.action_4.triggered.connect(self.open4)

        self.button_add.clicked.connect(self.add_line)
        self.button_edit.clicked.connect(self.edit_line)
        self.form_window=None
        self.button_drop.clicked.connect(self.drop_line)

    def drop_line(self):
        self.form_window = Drop(self)
        self.form_window.show()

    def add_line(self):
        self.form_window = AddLineForm(self)
        self.form_window.show()

    def edit_line(self):
        self.form_window = Updatingline(self)
        self.form_window.show()

    def find_line(self,cvuz,rnw):
        cvuzes = self.tableWidget.findItems(str(cvuz), Qt.MatchExactly)
        cvuzesind = tuple((pr.row()) for pr in cvuzes)
        print("find " + str(cvuz)+ ' | ' + rnw)
        for i in cvuzesind:
            if self.tableWidget.item(i,1).text()==rnw:
                print(i)
                self.selectirow(i)
                self.tableWidget.scrollToItem(self.tableWidget.item(i,0))
                return i


    def open(self):
        self.SetUpTable(GetNir())

    def open2(self):
        self.SetUpTable(GetFin())

    def open3(self):
        self.SetUpTable(GetRub())

    def open4(self):
        self.SetUpTable(Getvuz())

    def UpdNirTable(self):
        self.FillTable(GetNir())
