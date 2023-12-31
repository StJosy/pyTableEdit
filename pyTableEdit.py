import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QSpacerItem,
)
from PyQt6.QtCore import Qt
#import mysql.connector
import mysql.connector.pooling
import json
import logging
from dataclasses import dataclass


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("application.log"),
        logging.StreamHandler(sys.stdout),
    ],
    encoding="utf-8",
)

@dataclass
class conn:
    db_connection:None
    db_cursor:None
    
class EditFormWidget(QWidget):
    def __init__(self, config_file: str):
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self.edits = {}

        # Open File
        try:
            with open(config_file, "r") as json_file:
                connection_details = json.load(json_file)
                self.table_name = connection_details.pop("table")
                self.connection_details = connection_details
        except FileNotFoundError:
            self.logger.error(f"Error opening file: {config_file}")
            raise FileNotFoundError
            # sys.exit()
      
        self.db_cursor = None
        self.db_connection = None
        
        dbhandler = self.connection
        
        # Obtain column names
        query = """
            SELECT COLUMN_NAME \
            FROM INFORMATION_SCHEMA.COLUMNS \
            WHERE TABLE_NAME = %s;
        """
        dbhandler.db_cursor.execute(query, (self.table_name,))
        self.field_names = [
            dict_item["COLUMN_NAME"] for dict_item in dbhandler.db_cursor.fetchall()
        ]
        self.init_ui()
        self.populate_empty_form()
        
    @property
    def connection(self):
        try:
            if not self.db_connection or not self.db_connection.is_connected():
                if self.db_cursor:
                    self.db_cursor.close()
                if self.db_connection:
                    self.db_connection.close()
                self.db_connection = mysql.connector.connect(**self.connection_details)
                self.db_cursor = self.db_connection.cursor(dictionary=True)
                print("Reconnected successfully.")
        except Exception as e:
            print(f'Error: {str(e)}')
        return conn(db_connection=self.db_connection, db_cursor=self.db_cursor)

 

    def init_ui(self) -> None:
        self.layout = QVBoxLayout()

        # Create search layout
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Search by ID:")
        self.search_input = QLineEdit()

        # sometimes we needs import mask
        # self.search_input.setInputMask("999999")

        self.search_button = QPushButton("Search")
        # self.search_button.setStyleSheet(u"  color:LightSeaGreen;")
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_input.returnPressed.connect(self.search_by_id)
        self.search_button.clicked.connect(self.search_by_id)
        
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)

        # Create form layout
        self.form_layout = QFormLayout()

        self.layout.addLayout(self.search_layout)
        self.layout.addLayout(self.form_layout)
        self.setLayout(self.layout)

    def populate_empty_form(self) -> None:
        for col_name in self.field_names:
            label = QLabel(col_name)
            self.edits[col_name] = QLineEdit(objectName=col_name)
            self.edits[col_name].returnPressed.connect(self.save_changes)
           
            self.form_layout.addRow(label, self.edits[col_name])

        self.form_layout.addItem(QSpacerItem(10, 10))
        self.save_button = QPushButton("Save")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setEnabled(False)
        self.form_layout.addRow(self.save_button)
        self.form_layout.addItem(QSpacerItem(10, 10))

    def clear_form(self) -> None:
        for col_name in self.field_names:
            self.edits[col_name].clear()

        self.current_result = None  # Reset current result

    def search_by_id(self) -> bool:
        dbhandler = self.connection
        try:
            field = self.search_input.text().strip()
            if len(field) > 0:
                search_id = int(self.search_input.text().strip())
            else:
                print("You have to type row_id")
                return False
        except Exception:
            print("You have to type integer")
            return False
        self.clear_form()

        try:
            self.save_button.setEnabled(True)
            query = f"SELECT * FROM {self.table_name}  WHERE id = %(id)s"
            dbhandler.db_cursor.execute(query, {"status": 1, "id": search_id})
            result = dbhandler.db_cursor.fetchone()
            if result:
                self.current_result = result
                self.fill_form_with_data(result)
            else:
                self.current_result = None
        except mysql.connector.Error as e:
            self.logger.error(f"Error executing query. {e}")
        return True

    def fill_form_with_data(self, data) -> None:
        for row_key in data:
            self.edits[row_key].setText(str(data[row_key]))

    def save_changes(self) -> None:
        dbhandler = self.connection
        if hasattr(self, "current_result"):
            update_data = {}

            for field_name in self.field_names:
                current_field_value = self.edits[field_name].text().strip()
                stored_value = self.current_result[field_name]

                if str(current_field_value) != str(stored_value):
                    update_data[field_name] = current_field_value

            if update_data:
                update_field_list = [f"`{e}` = %({e})s" for e in update_data]
                update_stmt = f"UPDATE {self.table_name} set {', '.join(update_field_list)} WHERE id = %(id)s"
                update_data["id"] = int(self.search_input.text())

                try:
                    dbhandler.db_cursor.execute(update_stmt, update_data)
                    dbhandler.db_connection.commit()
                    self.logger.info(f"Query DONE: {dbhandler.db_cursor.statement}")
                except mysql.connector.Error as err:
                    self.logger.error(f"Query Error: {err}")

            else:
                print("No changes to save.")
        else:
            print("Record not found.")
        self.search_input.setText("")
        self.save_button.setEnabled(False)
        self.clear_form()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = QMainWindow()
    try:
        edit_form_widget = EditFormWidget("config.json")
    except Exception:
        sys.exit()

    window.setCentralWidget(edit_form_widget)
    window.setWindowTitle("Python Table Editor")
    window.setGeometry(100, 100, 400, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

    """ ------------------------------------------------------
    qt6-tools designer


"""
