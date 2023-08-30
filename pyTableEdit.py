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
import mysql.connector
import json
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("application.log"),
        logging.StreamHandler(sys.stdout),
    ],
    encoding="utf-8",
)


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
        except FileNotFoundError:
            self.logger.error(f"Error opening file: {config_file}")
            raise FileNotFoundError
            # sys.exit()

        # Connect do database
        try:
            self.db_connection = mysql.connector.connect(**connection_details)
        except Exception as e:
            self.logger.error(f"Error connecting to database. {e}")
            # sys.exit()

        self.db_cursor = self.db_connection.cursor(dictionary=True)

        # Obtain column names
        query = """
            SELECT COLUMN_NAME \
            FROM INFORMATION_SCHEMA.COLUMNS \
            WHERE TABLE_NAME = %s;
        """
        self.db_cursor.execute(query, (self.table_name,))
        self.field_names = [
            dict_item["COLUMN_NAME"] for dict_item in self.db_cursor.fetchall()
        ]
        self.init_ui()
        self.populate_empty_form()

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
            self.form_layout.addRow(label, self.edits[col_name])

        self.form_layout.addItem(QSpacerItem(10, 10))
        save_button = QPushButton("Save")
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.clicked.connect(self.save_changes)
        self.form_layout.addRow(save_button)
        self.form_layout.addItem(QSpacerItem(10, 10))

    def clear_form(self) -> None:
        for col_name in self.field_names:
            self.edits[col_name].clear()

        self.current_result = None  # Reset current result

    def search_by_id(self) -> bool:
        try:
            search_id = int(self.search_input.text().strip())
        except Exception:
            print("You have to type ineger")
            return False
        self.clear_form()

        try:
            query = f"SELECT * FROM {self.table_name}  WHERE id = %(id)s"
            self.db_cursor.execute(query, {"status": 1, "id": search_id})
            result = self.db_cursor.fetchone()
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
        if hasattr(self, "current_result"):
            update_data = {}

            for field_name in self.field_names:
                current_field_value = self.edits[field_name].text().strip()
                stored_value = self.current_result[field_name]

                if str(current_field_value) != str(stored_value):
                    update_data[field_name] = current_field_value

            if update_data:
                update_field_list = [f"{e} = %({e})s" for e in update_data]
                update_stmt = f"UPDATE {self.table_name} set {', '.join(update_field_list)} WHERE id = %(id)s"
                update_data["id"] = int(self.search_input.text())

                try:
                    self.db_cursor.execute(update_stmt, update_data)
                    self.db_connection.commit()
                    self.logger.info(f"Query DONE: {self.db_cursor.statement}")
                except mysql.connector.Error as err:
                    self.logger.error(f"Query Error: {err}")

            else:
                print("No changes to save.")
        else:
            print("Record not found.")
        self.search_input.setText("")
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
