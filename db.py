from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel
import sys
#!!!


from psycopg2.extras import DictCursor

from config import host, user, password, db_name

import psycopg2

class dbc():
    dbcon = None

def openDatabase():
    try:
        con = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, cursor_factory=DictCursor)
        print("database '" +db_name+"' is open")
        #con.autocommit = True
        dbc.dbcon = con

        return con
    except BaseException as _ex:
        print("[INFO] Error while connect db ", _ex)
        return None

def GetNir():
    with dbc.dbcon.cursor() as cur:
        query = f"select * from nir;"
        # print(query)
        cur.execute(query)
        table = cur.fetchall()
        return table

def GetFin():
    with dbc.dbcon.cursor() as cur:
        query = f"select codvuz as код_вуза,z2 as сокращенное_наименование,z3 as плановый_объем_финансирования,z18 as фактический_объем_финансирования,numworks as количество_НИР from f();"
        # print(query)
        cur.execute(query)
        table = cur.fetchall()
        return table

def GetRub():
    with dbc.dbcon.cursor() as cur:
        query = f"select codrub as код_рубрики,rubrika as наименование_рубрики from grn order by 1;"
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