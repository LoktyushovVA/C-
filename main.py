import psycopg2
from config import host, user, password, db_name
from windows import *
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from db import *

try:

    openDatabase()

    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec_())


except Exception as _ex:
    print("[INFO] Error in main ", _ex)
finally:
    if dbc.dbcon:
        dbc.dbcon.close()
        print("[INFO] PostgreSQL connection closed")
