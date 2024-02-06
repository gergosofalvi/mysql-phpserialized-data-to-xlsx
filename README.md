MySQL to XLSX and XLSX to MySQL Converter
=========================================

Overview
--------

This repository contains Python scripts for converting data between MySQL databases and Excel (XLSX) files. It is specifically designed to handle PHP serialized data within MySQL, providing functionality to export these data to XLSX format and import back from XLSX to MySQL, with proper serialization and deserialization.

Features
--------

*   **Export from MySQL to XLSX:** Converts data from a specified MySQL database and table into an XLSX file. It automatically handles PHP serialized data in specified columns.
*   **Import from XLSX to MySQL:** Takes data from an XLSX file and imports it into a specified MySQL database and table, including conversion of PHP serialized data.

Prerequisites
-------------

Python 3  
Required Python libraries: pandas, sqlalchemy, phpserialize, etc. (See `requirements.txt` for a full list)

Usage
-----

### Configuration

Edit the following variables in both scripts to match your database configuration:  
host, port, user, password, database, table\_name, serialized\_columns: List of columns containing PHP serialized data

### Running the Scripts

*   **Export to XLSX:** Run `sql-to-xlsx.py` to export data from MySQL to an XLSX file.
*   **Import to MySQL:** Run `xlsx-to-sql.py` to import data from an XLSX file to MySQL.

License
-------

This project is open-source and available under the [MIT License](LICENSE).