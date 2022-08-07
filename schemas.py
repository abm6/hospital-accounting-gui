import sqlite3
import os

# create the database directory if does not exist
if not os.path.exists('db'):
    os.mkdir('db')


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(f'./db/{db_file}.db')
    except Error as e:
        print(e)

    return conn


def create_tables(cursor):
    # create table
    # the unique ROW ID gets assigned for each patient
    # When the account gets created

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient(
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT,
            address TEXT,
            gender CHAR(1) NOT NULL,
            bloodgroup CHAR(3),
            weight INTEGER,
            height INTEGER,
            date DATE
        );
    """)

    # only one admin can make add or make someone admin

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user(
            username VARCHAR(20) NOT NULL,
            fullname VARCHAR(20) NOT NULL,
            password VARCHAR(20) NOT NULL,
            usertype VARCHAR(10) NOT NULL,
            gender CHAR(1) NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT,
            CONSTRAINT usertype CHECK (usertype IN ('doctor', 'nurse', 'receptionist', 'admin')),
            UNIQUE(username)
        );
    """)

    # adding a default admin

    cursor.execute("""
        INSERT OR IGNORE INTO user VALUES(
            'admin',
            'Administrator',
            'admin123',
            'admin',
            'M',
            0,
            ''
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointment(
            receptionist_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            accept_date DATE NOT NULL,
            accept_time TEXT ,
            symptoms TEXT,
            status VARCHAR(10) NOT NULL,
            CONSTRAINT status CHECK (status IN ('pending', 'accepted', 'rejected'))
            CONSTRAINT patient_id FOREIGN KEY (patient_id) REFERENCES patient(rowid),
            CONSTRAINT doctor_id FOREIGN KEY (doctor_id) REFERENCES user(rowid),
            CONSTRAINT receptionist_id FOREIGN KEY (receptionist_id) REFERENCES user(rowid)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_record(
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            nurse_id INTEGER,
            prescription TEXT,
            operation TEXT,
            remarks TEXT,
            demographics TEXT,
            injection TEXT,
            vaccinated BOOLEAN,
            CONSTRAINT patient_id FOREIGN KEY (patient_id) REFERENCES patient(rowid), 
            CONSTRAINT doctor_id FOREIGN KEY (doctor_id) REFERENCES user(rowid)
        );
    """)

    print("Tables created")
