from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel
import sys



from psycopg2.extras import DictCursor

from config import host, user, password, db_name

import psycopg2

class dbc():
    dbcon = None

def openDatabase():
    try:
        con = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, cursor_factory=DictCursor)
        print("database '" +db_name+"' is open")
        con.autocommit = True
        dbc.dbcon = con

        return con
    except BaseException as _ex:
        print("[INFO] Error while connect db ", _ex)
        return None




def GetNir():
    with dbc.dbcon.cursor() as cur:
        query = f'select codvuz as "код вуза",rnw as "номер НИР",f1 as "характер НИР",z2 as "сокращенное наименование вуза",f6 as "руководитель НИР",f10 as "коды темы по ГРНТИ",f18 as "плановый объем финансирования",f2 as "наименование НИР",f7 as "должность руководителя" from nir ;'
        # print(query)

        cur.execute(query)
        table = cur.fetchall()
        return table

def GetFin():
    with dbc.dbcon.cursor() as cur:
        query = f'select codvuz as "код вуза",z2 as "сокращенное наименование",z3 as "плановый объем финансирования",z18 as "фактический объем финансирования",numworks as "количество НИР" from f() order by z2;'
        # print(query)
        cur.execute(query)
        table = cur.fetchall()
        return table

def GetRub():
    with dbc.dbcon.cursor() as cur:
        query = f'select codrub as "код рубрики",rubrika as "наименование рубрики" from grn order by 1;'
        # print(query)
        cur.execute(query)
        table = cur.fetchall()
        return table

def Getvuz():
    with dbc.dbcon.cursor() as cur:
        query = f"select * from vuz_for_rus;"
        # print(query)
        cur.execute(query)
        table = cur.fetchall()
        return table


def GetVuzTuple():
    with dbc.dbcon.cursor() as cur:
        cur.execute("SELECT  z2 FROM f() order by z2")
        vuztup = ((row["z2"]) for row in cur.fetchall())
        return tuple(vuztup)

def GetVuzDict(swap = False):
    with dbc.dbcon.cursor() as cur:
        cur.execute("SELECT codvuz, z2 FROM f()")

        vdict = {row['z2']:row["codvuz"] for row in cur.fetchall()}  if swap else {row['codvuz']:row["z2"] for row in cur.fetchall()}
        return vdict




def AddLineToDB(rnw, har, cokr, ruk, grn, descr, dol, fin,oldRec = None):
    with dbc.dbcon.cursor() as cur:
        cur.execute(f"select codvuz from f() where z2 = '{cokr}'")
        cvuz = cur.fetchone()["codvuz"]
        q = f"select  add_line({cvuz},'{rnw}','{har}','{cokr}','{ruk}','{descr}','{grn}','{dol}',{fin})"
        print(q)
        cur.execute(q)
        # dbc.dbcon.commit()

def EditRecordToDB(rnw, har, cokr, ruk, grn, descr, dol, fin,oldRec):
    RemoveRecord(*oldRec)
    AddLineToDB(rnw, har, cokr, ruk, grn, descr, dol, fin)




def RemoveRecord(cvuz,rnw):
    with dbc.dbcon.cursor() as cur:
        cur.execute(f"select del({cvuz},'{rnw}');")
        dbc.dbcon.commit()
