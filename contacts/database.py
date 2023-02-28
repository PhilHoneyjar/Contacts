from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def create_contacts_table():
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            phone INTEGER(40),
            email VARCHAR(50) NOT NULL)
        """
    )


def create_connection(databaseName):
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)

    if not connection.open():
        QMessageBox.warning(
            None,
            "Contact",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    create_contacts_table()
    return True
