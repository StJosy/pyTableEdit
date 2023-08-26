# PyQt6 MySQL Table Editor

![PyQt6 Logo](https://www.riverbankcomputing.com/static/Docs/PyQt6/pyqt6_small.png)

**PyQt6 MySQL Table Editor** is a Python script that utilizes the PyQt6 library to create a graphical user interface for editing records in a MySQL database table. This tool provides a convenient way to interact with your MySQL database and make updates to specific records.

## Features

- **User-Friendly Interface**: The graphical user interface (GUI) is designed using the PyQt6 library, offering an intuitive and visually appealing experience for users.

- **Search by ID**: Easily search for records in the MySQL database table by providing the record's ID.

- **Edit and Save**: Modify the data in the selected record's fields and save your changes back to the database.

- **Automatic Logging**: The application automatically logs important events and errors to a log file (`application.log`), making troubleshooting and error tracking easier.

## Usage

1. Install the required packages by running `pip install PyQt6 mysql-connector-python`.

2. Configure the `config.json` file with your MySQL database connection details.

3. Run the script and open the PyQt6 MySQL Table Editor interface.

4. Enter the ID of the record you want to edit, make the necessary changes, and click the "Save" button to update the record in the database.

## Screenshots

![Application Screenshot](screenshots/application_screenshot.png)

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

5. Run the script: `python main.py`.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

You can copy and paste this Markdown text into your README.md file on GitHub. Don't forget to replace placeholders like `your-username` and include any relevant screenshots or adjustments to match your actual project.
