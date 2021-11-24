import sqlite3
import sys

from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QApplication
from PyQt5 import uic


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.con = sqlite3.connect("coffee.db3")
        self.cur = self.con.cursor()

        self.tableWidget.cellDoubleClicked.connect(self.open)

        self.initUI()

    def initUI(self):
        res = self.cur.execute("""SELECT * FROM info""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def open(self):
        self.sf = Second(self.con, self)
        self.sf.show()

    def closeEvent(self, event):
        self.con.close()


class Second(QWidget):
    def __init__(self, connection, parent):
        super().__init__()
        self.con = connection
        self.parent = parent
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.btn.clicked.connect(self.create)

        self.titles = ['id', 'name', 'level', 'status', 'taste', 'price', 'value']

        self.dictionary = {}
        self.initUI()

    def initUI(self):
        res = self.con.cursor().execute("""SELECT * FROM info""").fetchall()
        self.table_second.setColumnCount(7)
        self.table_second.setRowCount(0)
        for i, row in enumerate(res):
            self.table_second.setRowCount(
                self.table_second.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_second.setItem(
                    i, j, QTableWidgetItem(str(elem)))

        self.table_second.itemChanged.connect(self.item_changed)

    def item_changed(self, item):
        row = self.table_second.currentRow()
        id = QTableWidgetItem(self.table_second.item(row, 0)).text()

        if not item.text():
            return
        if not self.con.cursor().execute("""SELECT * FROM info WHERE id = ?""", (int(id),)).fetchone():
            self.dictionary[self.titles[item.column()]] = item.text()
            if len(self.dictionary.keys()) == 7:
                que = f"""INSERT INTO info("""
                vals = """) VALUES("""

                for i, j in self.dictionary.items():
                    if i == 'price' or i == 'value' or i == 'id':
                        vals += f"{int(j)},"
                    else:
                        vals += f"'{j}',"
                    que += f"{i},"

                que = que[:-1]
                que += vals[:-1]
                que += ")"
                self.con.cursor().execute(que)

        else:
            que = f"""UPDATE info 
                       SET {self.titles[item.column()]} = ?
                       WHERE id = ?"""
            self.con.cursor().execute(que, (item.text(), int(id)))
        self.con.commit()

        self.parent.initUI()

    def create(self):
        pr = self.table_second.rowCount()

        self.table_second.setRowCount(pr + 1)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
