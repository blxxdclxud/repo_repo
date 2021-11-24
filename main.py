import sqlite3
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QWidget, QTableView, QApplication
from PyQt5 import uic


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('coffee.db3')
        db.open()

        model = QSqlTableModel(self, db)
        model.setTable('info')
        model.select()

        self.table.setModel(model)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec())
