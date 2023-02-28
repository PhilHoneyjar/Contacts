from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .model import ContactsModel


class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(1600, 800)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.contactsModel = ContactsModel()
        self.setup_UI()

    def setup_UI(self):
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()

        self.addButton = QPushButton("Add")
        self.addButton.clicked.connect(self.open_add_dialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.delete_contact)
        self.clearAllButton = QPushButton("Clear All")
        self.clearAllButton.clicked.connect(self.clear_contacts)

        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addStretch()
        layout.addWidget(self.clearAllButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def open_add_dialog(self):
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.add_contact(dialog.data)
            self.table.resizeColumnsToContents()

    def delete_contact(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return

        messageBox = QMessageBox.warning(
            self,
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.delete_contact(row)

    def clear_contacts(self):
        messageBox = QMessageBox.warning(
            self,
            "Do you want to remove all your contacts?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if messageBox == QMessageBox.Ok:
            self.contactsModel.clear_contacts()


class AddDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setup_UI()

    def setup_UI(self):
        self.nameField = QLineEdit()
        self.nameField.setObjectName("Name")
        self.last_nameField = QLineEdit()
        self.last_nameField.setObjectName("Last_name")
        self.phoneField = QLineEdit()
        self.phoneField.setObjectName("Phone")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")

        layout = QFormLayout()
        layout.addRow("Name:", self.nameField)
        layout.addRow("Last_name:", self.last_nameField)
        layout.addRow("Phone:", self.phoneField)
        layout.addRow("Email:", self.emailField)
        self.layout.addLayout(layout)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        self.data = []
        for field in (self.nameField, self.last_nameField, self.phoneField, self.emailField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()
