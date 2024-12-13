# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides a GUI-based easy-to-use approach to perform various sophisticated chemical operations/calculations.
# This file creates a database for various operations in this application.


import pymysql
import openpyxl

class DBCompounds:
    """
    A class used to represent the database operations for chemical compounds.
    """
    def __init__(self, host, user, password, database=None):
        """
        A constructor that initializes the database class
        :param host: The hostname or IP address of the database server.
        :param user: The username used to authenticate with the database.
        :param password: The password used to authenticate with the database.
        :param database: The name of the database to connect to (default is None).
        :param connection : Connection or None - The connection object for the database.
        :param cursor : Cursor or None - The cursor object to execute database queries.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def createDatabase(self, dbName):

        """Creates a new database if it does not already exist."""

        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
        self.cursor.execute(f"USE {dbName}")
        self.database = dbName

    def createTable(self, createTableQuery):
        """Creates a new table in the database."""
        self.cursor.execute(createTableQuery)

    def connect(self, database=None):
        """Establishes a connection to the database."""
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()

    def insertTableData(self, insertQuery, excelFilePath):
        """Inserts data into the table from an Excel file."""
        loc = excelFilePath
        dataList = []
        wb = openpyxl.load_workbook(loc)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Clean and validate data
            clean_row = tuple(
                str(cell).replace('\xa0', '').replace('−', '-').replace(' ', '') if isinstance(cell, str) else cell for cell in row
            )
            # Skip rows with empty or NULL ChemicalName
            if clean_row[0] and clean_row[0].strip():
                dataList.append(clean_row)

        self.cursor.executemany(insertQuery, dataList)
        self.connection.commit()

    def read_data(self, select_query):
        """Reads data from the table using a SELECT query."""
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def readRecord(self, table_name, record_id):
        """Reads a record from the table by the chemical name."""
        query = f"SELECT * FROM {table_name} WHERE ChemicalName = %s"
        self.cursor.execute(query, (record_id,))
        return self.cursor.fetchone()

    def readRecordF(self, table_name, record_id):
        """Reads a record from the table by the chemical formula."""
        query = f"SELECT * FROM {table_name} WHERE ChemicalFormula = %s"
        self.cursor.execute(query, (record_id,))
        return self.cursor.fetchone()

    def close(self):
        """Closes the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def fetch_compound(self, query):
        """Fetches the chemical names based on the query."""
        self.cursor.execute(query)
        return [row['ChemicalName'] for row in self.cursor.fetchall()]

    def fetch_compoundF(self, query):
        """Fetches the chemical formulas based on the query."""
        self.cursor.execute(query)
        return [row['ChemicalFormula'] for row in self.cursor.fetchall()]

    def fetchChemicalNames(self, cursor):
        """Fetches all chemical names from the compounds table."""
        cursor.execute("SELECT ChemicalName FROM compounds")
        result = cursor.fetchall()
        names = [row['ChemicalName'] for row in result]
        return names

    def fetchChemicalFormulas(self, cursor, cName):
        """Fetches the chemical formula for a given chemical name."""
        cursor.execute("SELECT ChemicalFormula FROM compounds where ChemicalName = %s", (cName,))
        result = cursor.fetchone()
        if result:
            return result['ChemicalFormula']
        return ""

def main():
    """Main function to create a database, create a table, insert data, and read data."""
    db = DBCompounds(host='localhost', user='root', password='Chemistry.123')
    db.connect()

    # Create a new database
    db.createDatabase("ChemicalDatabase")

    # Close initial connection and reconnect specifying the database
    db.close()
    db.connect(database='ChemicalDatabase')

    # Create a new table
    createTableQuery = """
    CREATE TABLE IF NOT EXISTS compounds (
        ChemicalName VARCHAR(100) PRIMARY KEY,
        ChemicalFormula VARCHAR(100) NOT NULL,
        MolecularWeight DECIMAL(10, 3),
        Density DECIMAL(10, 4),
        pKa DECIMAL(10, 4)
    )
    """
    db.createTable(createTableQuery)

    # Insert data from an Excel file into the table
    queryInsert = "INSERT INTO compounds(ChemicalName, ChemicalFormula, MolecularWeight, Density, pKa) VALUES (%s, %s, %s, %s, %s)"
    db.insertTableData(queryInsert, 'ChemicalDatabase.xlsx')

    # Read data from the table
    result = db.read_data("SELECT * FROM compounds")
    for row in result:
        print(row)

    # Fetch individual record by ID
    record = db.readRecord('compounds', "Hydrochloric acid")
    print("Record:", record)

    db.close()

# Calling main function
if __name__ == "__main__":
    main()
