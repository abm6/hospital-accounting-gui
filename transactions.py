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


def getAllUsers(cursor, usertype=None):
    # fetch all users

    query = "select rowid,* from user"

    if usertype is not None:
        query += f" where usertype = '{usertype}'"
    
    query += ";"


    try:
        cursor.execute(query)
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


def updateUserByUsername(cursor,username=None,userid=None, update={}):
    # update user with userId reference
    # returns true / false


    try:
        cursor.execute(f"""
            UPDATE user SET
                username = '{update['username']}',
                fullname = '{update['fullname']}',
                password = '{update['password']}',
                usertype = '{update['usertype']}',
                gender = '{update['gender']}',
                age = {update['age']},
                phone = '{update['phone']}'
                WHERE rowid = {userid}
                ;
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return True


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


def getAllPatients(cursor):
    # fetch all patients
    try:
        cursor.execute(f"""
        SELECT rowid, * FROM patient;
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()

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
        SELECT rowid,* FROM user WHERE usertype = 'doctor' AND rowid NOT IN (
            SELECT doctor_id FROM appointment WHERE accept_date = '{date}'
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
                {appointmentData['receptionistid']},
                {appointmentData['patientid']},
                {appointmentData['doctorid']},
                '{appointmentData['date']}',
                '{appointmentData['time']}',
                '{appointmentData['symptoms']}',
                '{appointmentData['status']}'
                );
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.lastrowid

def getAllAppointments(cursor):
    # fetch all appointments
    try:
        cursor.execute(f"""
        SELECT rowid, * FROM appointment;
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()


def getPatientsAppointedToDoctor(cursor, doctorID, patientID=None):
    # fetch all patients appointed to doctor


    query = f"""
        SELECT rowid,* FROM patient WHERE rowid IN (
            SELECT patient_id FROM appointment WHERE doctor_id = {doctorID} 
    """

    if patientID is not None and patientID != "":
        query += f" AND rowid = {patientID}"

    query += ");"

    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()

def getPatientsAppointedToNurse(cursor, nurseID, patientID=None):
    # fetch all patients appointed to doctor


    query = f"""
        SELECT rowid,name FROM patient WHERE rowid IN (
            SELECT patient_id FROM medical_record WHERE nurse_id = {nurseID} 
    """

    if patientID is not None and patientID != "":
        query += f" AND rowid = {patientID}"

    query += ");"

    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()

def getPatientMedicalRecords(cursor, patientID=None, doctorID=None, nurseID=None):
    # fetch all medical records of patient
    
    if patientID is not None and patientID != "":
        query = f"""
            SELECT rowid,* FROM medical_record WHERE patient_id = {patientID} AND
        """
    else:
        query = f"""
            SELECT rowid,* FROM medical_record WHERE
        """

    if doctorID is not None and nurseID is not None:
        query += f" doctor_id = {doctorID} AND nurse_id = {nurseID}"
    elif doctorID is not None:
        query += f" doctor_id = {doctorID}"
    elif nurseID is not None:
        query += f" nurse_id = {nurseID}"

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
            WHERE patient_id = {patientID} AND doctor_id = {doctorID};
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.rowcount == 1


def updateMedicalRecord(cursor,medicalRecordData={}):
    # update medical record of patient
    # returns upadted medical record


    print("medicalrecorddata",medicalRecordData)

    try:
        cursor.execute(f"""
            INSERT OR IGNORE INTO medical_record (patient_id,doctor_id,vaccinated) 
            VALUES ({medicalRecordData['patient_id']},{medicalRecordData['doctor_id']},0);
        """)

        cursor.execute(f"""
            UPDATE medical_record SET
                nurse_id = {medicalRecordData['nurse_id']},
                prescription = '{medicalRecordData['prescription']}',
                operation = '{medicalRecordData['operation']}',
                remarks = '{medicalRecordData['remarks']}',
                demographics = '{medicalRecordData['demographics']}',
                injection = '{medicalRecordData['injection']}'
            WHERE doctor_id = {medicalRecordData['doctor_id']};
            
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.rowcount == 1

def getAvailableNurses(cursor, date):
    # fetch all nurses
    try:
        cursor.execute(f"""
        SELECT rowid,fullname FROM user WHERE usertype = 'nurse' AND rowid NOT IN (
            SELECT nurse_id FROM medical_record
        );
        """)
    except sqlite3.Error as e:
        print(e)
        return None

    return cursor.fetchall()


def setVaccinatedStatus(cursor, patientID, prescriptionID, vaccinatedStatus):
    # update vaccinated status of patient
    # returns true / false

    vaccinatedStatus = 1 if vaccinatedStatus else 0

    try:
        cursor.execute(f"""
            UPDATE medical_record SET vaccinated = '{vaccinatedStatus}'
            WHERE rowid = {prescriptionID} AND patient_id = {patientID};
        """)
    except sqlite3.Error as e:
        print(e)
        return False

    return cursor.rowcount == 1