from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class ContactsModel:
    def __init__(self):
        self.model = self.create_model()

    @staticmethod
    def create_model():
        tableModel = QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Name", "Last_name", "Phone", "Email")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Horizontal, header)
        return tableModel

    def add_contact(self, data):
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column_index, field in enumerate(data):
            self.model.setData(self.model.index(rows, column_index + 1), field)
        self.model.submitAll()
        self.model.select()

    def delete_contact(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clear_contacts(self):
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
