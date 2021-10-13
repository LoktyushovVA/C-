from forms import pril_nir,  drop, add_form_m
from PyQt5 import QtWidgets,QtGui, QtCore
import re
import db


class OneLine(QtWidgets.QDialog, add_form_m.Ui_Dialog):
    def __init__(self,name,parent):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(name)
        self.parent = parent
        self.ctypes = "ФПР"
        self.cRec = ()
        self.setupfields()

    def commitrecord(self,action,oldnum = -1):
        # if self.check(oldnum):

        ctype = self.ctypes[self.CODTYPE.currentIndex()]
        grnti = self.GRNTI.text()
        if not self.GRNTI2.isHidden():
            grnti+= "; "+ self.GRNTI2.text()
        vuz, rnw = self.prog.currentText(), self.rnv.text()
        # if oldnum>-1:
        #     dbm.RemoveRecord(self.parent.cRec[0], self.parent.cRec[1])
        action(rnw,ctype,vuz,self.ruk.text(),self.NIR.toPlainText(),grnti,self.ruk2.text(),self.pfin.text(),oldRec = self.cRec)
        self.parent.UpdNirTable()
        cvuz = db.GetVuzDict(swap=True)[vuz]
        self.parent.find_line(cvuz, rnw)
        # self.parent.FillTable(dbm.GetTableNir(sort=self.parent.sorttype, desc=self.parent.sortdesc))
        # dbm.countNPROJ()
        # dbm.SumPFinInProg()
        self.close()

    def discard(self):
        self.close()


    def setupfields(self):
        self.finerror.setHidden(True)
        self.prog.addItem("")
        self.prog.addItems(db.GetVuzTuple())
        onlyInt = QtGui.QIntValidator()
        self.pfin.setValidator(onlyInt)
        self.rnv.setValidator(onlyInt)
        self.discardbtn.clicked.connect(self.discard)
        mask = "00.00.00;_"
        self.GRNTI.setInputMask(mask)
        self.GRNTI2.setInputMask(mask)
        self.GRNTI2.setHidden(True)
        self.grntibtn.setText("+")

        self.grntibtn.clicked.connect(self.togglegrnti)

    def togglegrnti(self):
        if self.grntibtn.text() == "+":
            self.GRNTI2.setHidden(False)
            self.grntibtn.setText("-")
        else:
            self.GRNTI2.setHidden(True)
            self.grntibtn.setText("+")


class Drop(QtWidgets.QDialog, drop.Ui_Dialog):
    def __init__(self,parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.cRow = parent.cRow
        names = ['cvuz','rnw', 'har', 'cokr', 'ruk', 'grn', 'fin','descr', 'dol']
        self.record = dict(zip(names,[self.parent.tableWidget.item(self.cRow, i).text() for i in range(0,9)]))
        print(self.record)

        self.drop_podt.clicked.connect(self.removerec)
        self.drop_otmena.clicked.connect(self.close)
        # self.drop_podt.setEnabled(False)


    def removerec(self):
        db.RemoveRecord(self.record['cvuz'], self.record['rnw'])
        self.parent.cRow = -1
        self.parent.UpdNirTable()
        self.close()


class AddLineForm(OneLine):
    def __init__(self,parent):
        super().__init__("Добавление записи",parent)
        self.savebtn.clicked.connect(self.saverecord)

    def saverecord(self):
        print('save click')
        self.commitrecord(db.AddLineToDB)




class Updatingline(OneLine):
    def __init__(self,parent):
        super().__init__("Редактирование записи",parent)
        self.savebtn.clicked.connect(self.saverecordfor_update)
        self.cRow = parent.cRow
        self.fillform()

    def fillform(self):
        table = self.parent.tableWidget
        if not (table.item(self.cRow, 0)):
            return
        names = ['cvuz','rnw', 'har', 'cokr', 'ruk', 'grn', 'fin','descr', 'dol']
        record = dict(zip(names,[table.item(self.cRow, i).text() for i in range(0,9)]))
        self.cRec =  (record['cvuz'],record['rnw'])
        self.prog.setCurrentText(record['cokr'])
        self.pfin.setText(str(record["fin"]))
        self.rnv.setText(record["rnw"])
        self.CODTYPE.setCurrentIndex(self.ctypes.find(record["har"]))
        self.ruk.setText(record["ruk"])
        self.ruk2.setText(record["dol"])
        self.NIR.setPlainText(record["descr"])
        grnti = record["grn"].strip()
        pattern = ";|,| "
        if any((c in set(pattern)) for c in grnti):
            grnti = re.split(pattern, grnti)
            if "" in grnti:
                grnti.remove("")
            self.togglegrnti()
            self.GRNTI.setText(grnti[0])
            self.GRNTI2.setText(grnti[1])
        else:
            self.GRNTI.setText(grnti)


    def saverecordfor_update(self):
        print('save click')
        self.commitrecord(db.EditRecordToDB)

