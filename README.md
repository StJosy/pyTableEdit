# PyQt6 MySQL Table Editor

**PyQt6 MySQL Table Editor** is a Python script that utilizes the PyQt6 library to create a graphical user interface for editing records in a MySQL database table. This tool provides a convenient way to interact with your MySQL database and make updates to specific records.

## Features

- **User-Friendly Interface**: The graphical user interface (GUI) is designed using the PyQt6 library, offering an intuitive and visually appealing experience for users.

- **Search by ID**: Easily search for records in the MySQL database table by providing the record's ID.

- **Edit and Save**: Modify the data in the selected record's fields and save your changes back to the database.

- **Automatic Logging**: The application automatically logs important events and errors to a log file (`application.log`), making troubleshooting and error tracking easier.

## Usage

1. Install the required packages by running `pip install PyQt6 mysql-connector-python`.

2. Configure the config.json file with your MySQL database connection details including the desired table name. The config.json file should have the following structure:
   ```json
   {
       "host": "your_database_host",
       "user": "your_database_user",
       "password": "your_database_password",
       "database": "your_database_name",
       "table": "your_table_name"
   }
   ```


4. Run the script and open the PyQt6 MySQL Table Editor interface.

5. Enter the ID of the record you want to edit, make the necessary changes, and click the "Save" button to update the record in the database.

## Prerequisites

- Python 3.x
- PyQt6 library
- MySQL database
- `config.json` file with database connection details

## Installation

1. Clone this repository using `git clone https://github.com/your-username/pyqt6-mysql-table-editor.git`.

2. Navigate to the project directory: `cd pyqt6-mysql-table-editor`.

3. Install the required packages: `pip install PyQt6 mysql-connector-python`.

4. Configure the `config.json` file with your MySQL database connection details.

5. Run the script: `python pyTableEdit.py`.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
