import sqlite3


def addUser(cursor, user={}):
    # user adding logic
    # get reference of user ID

    print(user)

    try:
        cursor.execute(f"""
            INSERT INTO user VALUES(
                '{user['username']}',
                '{user['fullname']}',
                '{user['password']}',
                '{user['usertype']}',
                '{user['gender']}',
                {user['age']},
                '{user['phone']}'
                );
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.lastrowid


def removeUserById(cursor, userID):
    # remove user with userId reference
    # returns true / false
    try:
        cursor.execute(f"""
        DELETE FROM user WHERE rowid = {userID};
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return True


def removeUserByUsername(cursor, username):
    # remove user with userId reference
    # returns true / false
    try:
        cursor.execute(f"""
        DELETE FROM user WHERE username = '{username}';
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return False if cursor.rowcount == 0 else True


def getAllUsers(cursor):
    # fetch all users
    try:
        cursor.execute(f"""
        SELECT * FROM user;
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()


def getUserInfoById(cursor, userID):
    # fetch user info if exists
    try:
        cursor.execute(f"""
        SELECT * FROM user WHERE rowid = {userID};
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchone()


def getUserInfoByUsername(cursor, username):
    # fetch user info if exists
    try:
        cursor.execute(f"""
        SELECT * FROM user WHERE username = '{username}';
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchone()


def updateUserByUsername(cursor, user={}):
    # update user with userId reference
    # returns true / false
    try:
        cursor.execute(f"""
            UPDATE user SET
                fullname = '{user['fullname']}',
                password = '{user['password']}',
                usertype = '{user['usertype']}',
                gender = '{user['gender']}',
                age = {user['age']},
                phone = '{user['phone']}'
            WHERE username = '{user['username']}'
            RETURNING *;
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.fetchone()


def addPatient(cursor, patientData={}):
    # update Database
    # returns patientID
    try:
        cursor.execute(f"""
            INSERT INTO patient VALUES(
                '{patientData['name']}',
                {patientData['age']},
                '{patientData['phone']}',
                '{patientData['address']}',
                '{patientData['gender']}',
                '{patientData['bloodgroup']}',
                {patientData['weight']},
                {patientData['height']},
                '{patientData['date']}'
                );
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.lastrowid


def findPatient(cursor, filter={}, limit=1):
    # find patient with filter
    # by default, it will return all patients with matching conditions
    # if options['limit'] is set, it will return only that many patients
    # Returns list of tuples containing patient data

    fields = filter.keys()

    query = "select rowid,* from patient where "

    for index, field in enumerate(fields):
        if index == 0:
            query += f"{field} = '{filter[field]}'"
        else:
            query += f" AND {field} = '{filter[field]}'"
        if index == len(fields)-1:
            query += ";"

    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchmany(limit)


def updatePatientById(cursor, patientID, patientData={}):
    # update patient with patientId reference
    # returns true / false

    query = "update patient set "

    updatedFields = patientData.keys()

    for index, field in enumerate(updatedFields):
        if index == 0:
            query += f"{field} = '{patientData[field]}'"
        else:
            query += f", {field} = '{patientData[field]}'"
        if index == len(updatedFields)-1:
            query += f" where rowid = {patientID} RETURNING *;"

    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchone()


def removePatientById(cursor, patientID):
    # remove patient with patientId reference
    # returns true / false
    try:
        cursor.execute(f"""
        DELETE FROM patient WHERE rowid = {patientID};
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.rowcount == 1

# ================EXPERIMENTAL BEGIN=====================================

def findOnePatientAndUpdate(cursor, filter={}, patientData={}):
    # find patient with filter

    fields = filter.keys()

    query = "update patient set "

    for index, field in enumerate(fields):
        if index == 0:
            query += f"{field} = '{patientData[field]}'"
        else:
            query += f", {field} = '{patientData[field]}'"
        if index == len(fields)-1:
            query += " where "
            for index, field in enumerate(fields):
                if index == 0:
                    query += f"{field} = '{filter[field]}'"
                else:
                    query += f" AND {field} = '{filter[field]}'"
                if index == len(fields)-1:
                    query += ";"

    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchone()


# ================EXPERIMENTAL END=====================================



def getAllDoctors(cursor):
    # fetch all doctors
    try:
        cursor.execute(f"""
        SELECT * FROM user WHERE usertype = 'doctor';
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()

def getAvailableDoctors(cursor, date):
    # fetch all doctors
    try:
        cursor.execute(f"""
        SELECT * FROM user WHERE usertype = 'doctor' AND rowid NOT IN (
            SELECT doctorID FROM appointment WHERE date = '{date}'
        );
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()


def userLogin(cursor,username,password, usertype):
    try:
        cursor.execute(f"""
            SELECT rowid from user
            WHERE username = '{username}' AND password = '{password}'
            AND usertype = '{usertype}'
            ;
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    rowid = cursor.fetchone()
    return rowid[0] if rowid is not None else None

def makeAppointment(cursor, appointmentData={}):
    # update Database
    # returns appointmentID
    try:
        cursor.execute(f"""
            INSERT INTO appointment VALUES(
                {appointmentData['patientID']},
                {appointmentData['doctorID']},
                '{appointmentData['date']}',
                '{appointmentData['time']}',
                '{appointmentData['status']}'
                );
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.lastrowid


def getPatientsAppointedToDoctor(cursor, doctorID, patientID=None):
    # fetch all patients appointed to doctor


    query = f"""
        SELECT * FROM patient WHERE rowid IN (
            SELECT patientID FROM appointment WHERE doctorID = {doctorID} 
    """

    if patientID is not None:
        query += f" AND patientID = {patientID}"

    query += ");"

    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()

def getPatientMedicalRecords(cursor, patientID, doctorID, nurseID):
    # fetch all medical records of patient
    
    query = f"SELECT rowid,* FROM medical_record WHERE patientID = {patientID}"

    if doctorID is not None:
        query += f" AND doctorID = {doctorID}"
    if nurseID is not None:
        query += f" AND nurseID = {nurseID}"
    
    query += ";"

    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()


def updatePrescription(cursor,patientID,doctorID,prescription):
    # update prescription of patient
    # returns true / false
    try:
        cursor.execute(f"""
            UPDATE medical_record SET prescription = '{prescription}'
            WHERE patientID = {patientID} AND doctorID = {doctorID};
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.rowcount == 1


def updateMedicalRecord(cursor,medicalRecordData={}):
    # update medical record of patient
    # returns upadted medical record
    try:
        cursor.execute(f"""
            UPDATE medical_record SET
                nurseID = {medicalRecordData['nurseID']},
                prescription = '{medicalRecordData['prescription']}',
                operation = '{medicalRecordData['operation']}',
                remarks = '{medicalRecordData['remarks']}',
                demographics = '{medicalRecordData['demographics']}',
                injection = '{medicalRecordData['injection']}',
            WHERE rowid = {medicalRecordData['rowid']} 
            AND doctor_id = {medicalRecordData['doctorID']};
            ;
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.rowcount == 1

def getAvailableNurses(cursor, date):
    # fetch all nurses
    try:
        cursor.execute(f"""
        SELECT * FROM user WHERE usertype = 'nurse' AND rowid NOT IN (
            SELECT nurseID FROM appointment WHERE date = '{date}'
        );
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()


def setVaccinatedStatus(cursor, patientID, vaccinatedStatus):
    # update vaccinated status of patient
    # returns true / false

    vaccinatedStatus = 1 if vaccinatedStatus else 0

    try:
        cursor.execute(f"""
            UPDATE medical_record SET vaccinated = '{vaccinatedStatus}'
            WHERE rowid = {patientID};
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.rowcount == 1