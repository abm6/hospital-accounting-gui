import schemas
import transactions
import pprint
import cli_dashboard
from datetime import date

import temp_data

pp = pprint.PrettyPrinter()

today = date.today()

# YYYY-MM-DD
day = today.strftime("%Y-%m-%d")





user_session = {
    "username": "",
    "usertype": "",
    "id": ""
}





class User:
    def __init__(self):
        pass

    def login(self, username, password, usertype):
        # check if username and password is correct
        # returns true / false

        global user_session
        id = transactions.userLogin(cursor, username, password, usertype)
        if id is not None:
            user_session['username'] = username
            user_session['usertype'] = usertype
            user_session['id'] = id
            return True
        return False

    def logout(self):
        global user_session
        user_session = {
            "username": "",
            "usertype": "",
            "id": ""
        }
        return True

    def getUserSession(self):
        return user_session

    def setUserSession(self,username, usertype, id):
        user_session["username"] = username
        user_session["usertype"] = usertype
        user_session["id"] = id

class Admin(User):
    def __init__(self):
        pass

    def login(self, username, password):
        # check if username and password is correct
        # returns true / false
        return super().login(username, password, "admin")

    def addUser(self, user={}):
        isUserAdded = transactions.addUser(cursor, user=user)
        return True if isUserAdded is not None and isUserAdded != 0 else False

    def removeUser(self, userID=None, username=None):
        # remove user with userId reference
        # returns true / false
        if userID is not None:
            return transactions.removeUserById(cursor, userID)
        elif username is not None:
            return transactions.removeUserByUsername(cursor, username)
        return False

    def getUserInfo(self, userID=None, username=None):
        # fetch user info if exists
        if userID is not None:
            return transactions.getUserInfoById(cursor, userID)
        elif username is not None:
            return transactions.getUserInfoByUsername(cursor, username)
        return None

    def getAllUsers(self,usertype=None):
        # fetch all users
        return transactions.getAllUsers(cursor,usertype)

    def getAllPatients(self):
        # fetch all patients
        return transactions.getAllPatients(cursor)


    def updateUser(self,username=None,userid=None, user={}):
        # update user with userId reference
        # returns Updated user data if any changes else returns false

        userBeforeUpdate = self.getUserInfo(username)


        updatedUser = transactions.updateUserByUsername(cursor,username=username,userid=userid, user=user)

        return updatedUser if updatedUser != userBeforeUpdate else None


class Receptionist(User):
    def __init__(self):
        pass

    def login(self, username, password):
        return super().login(username, password, "receptionist")

    def addPatient(self, patientData={}):
        # update Database
        # returns patientData if added else returns None
        if patientData['date'] is None or patientData['date'] == '':
            patientData['date'] = day

        filter = {
            'name': patientData['name'],
            'date': patientData['date'],
            'phone': patientData['phone']
        }

        similarPatient = self.findPatient(filter)

        if similarPatient is not None and similarPatient == tuple(patientData.values()):
            return None
        else:
            patient_id = transactions.addPatient(cursor, patientData)
            return patient_id

    def getPatientInfoById(self, patientID):
        return 0

    def findPatient(self, filter={}, limit=1):
        foundPatient = transactions.findPatient(
            cursor, filter=filter, limit=limit)

        return foundPatient

    def updatePatientById(self, patientID, patientData={}):
        updatedPatient = transactions.updatePatientById(
            cursor, patientID, patientData)

        if updatedPatient is not None and updatedPatient == tuple(patientData.values()):
            return {"data": updatedPatient, "message": "Patient updated successfully"}
        else:
            return {"data": None, "message": "Patient not found"}

    def removePatientById(self, patientID):
        foundPatient = self.findPatient(filter={'patientID': patientID})
        isPatientRemoved = transactions.removePatientById(cursor, patientID)
        return {"data": foundPatient, "message": "Patient removed successfully"} if isPatientRemoved else {"data": None, "message": "Patient not found"}

    def makeAppointment(self, appointmentData={}):
        appointment = transactions.makeAppointment(appointmentData)
        return {"data": appointment, "message": "Appointment made successfully"} if appointment is not None else {"data": None, "message": "Appointment not made"}

    def getAllAppointments(self):
        return transactions.getAllAppointments(cursor)

    
    def fetchAvailableDoctors(self):
        availableDoctors = transactions.getAvailableDoctors(cursor,day)

        if availableDoctors is not None and len(availableDoctors) > 0:
            return {"data": availableDoctors, "message": "Doctors fetched successfully"}
        else:
            return {"data": None, "message": "No doctors available"}

    def updatePatientInfo(self, filter={}, patientData={}):
        updatedPatient = None

        if patientData['date'] is None or patientData['date'] == '':
            patientData['date'] = day

        if patientData['patientID'] is not None:
            updatedPatient = transactions.updatePatientById(
                cursor, patientData)
            return updatedPatient

        else:

            foundPatient = self.findPatient(filter, 1)
            if foundPatient is not None and len(foundPatient) == 1:
                # get patientID from foundPatient
                patientData['patientID'] = foundPatient[0][0]
                updatedPatient = transactions.updatePatientById(
                    cursor, patientData)
                return {"updatedData": updatedPatient, "message": "Patient updated Successfully"}

        return {"data": None, "message": "Patient not found"}

    def removePatientByName(self, patientName):
        return 0


class Doctor(User):
    def __init__(self):
        pass

    def login(self, username, password):
        return super().login(username, password, "doctor")

    def getAvailableNurses(self):
        return transactions.getAvailableNurses(cursor, day)

    def getPatientsAppointed(self, patientID=None):
        # returns list of all the patients with their patient ID
        patients = transactions.getPatientsAppointedToDoctor(
            cursor, doctorID=user_session['id'], patientID=patientID)
        return {"data": patients, "message": "These are the patients appointed"} if patients is not None else {"data": None, "message": "No patients appointed"}

    def getMedicalRecords(self, patientID):
        # returns list of prescriptions, prescriptionID along with their details
        medicalRecords = transactions.getPatientMedicalRecords(
            cursor, patientID=patientID, doctorID=user_session['id'], nurseID=None)
        return {"data": medicalRecords, "message": "These are the medical records"} if medicalRecords is not None else {"data": None, "message": "No medical records"}

    def createOrUpdateMedicalRecord(self, medicalRecordData={}):
        # can contain schedules of patients for nurses
        # returns boolean

        medicalRecordData['doctorID'] = user_session['id']

        isUpdated = transactions.updateMedicalRecord(cursor, medicalRecordData)
        return {"data": isUpdated, "message": "Prescription updated successfully"} if isUpdated else {"data": None, "message": "Prescription not updated"}


class Nurse(User):
    def __init__(self):
        pass

    def login(self, username, password):
        return super().login(username, password, "nurse")

    def getPatientMedicalRecords(self):
        # return list

        return transactions.getPatientMedicalRecords(cursor, nurseID=user_session['id'])

    def getDrugPrescriptions(self, patientID):
        # return list

        prescriptions = transactions.getPatientMedicalRecords(
            cursor, patientID=patientID, doctorID=None, nurseID=user_session['id'])

        return {"data": prescriptions, "message": "These are the prescriptions"} if prescriptions is not None else {"data": None, "message": "No prescriptions"}

    def setVaccinatedStatus(self, patientID, prescriptionID, isVaccinated):
        vaccinatedStatus = transactions.setVaccinatedStatus(
            cursor, patientID, prescriptionID, isVaccinated)
        return {"data": vaccinatedStatus, "message": "Vaccinated status updated successfully"} if vaccinatedStatus is not None else {"data": None, "message": "Vaccinated status not updated"}





def main():
    # create connection
    conn = schemas.create_connection('hospital')
    # Create a cursor
    global cursor

    cursor = conn.cursor()
    # create tables
    schemas.create_tables(cursor)

    # instances
    admin = Admin()
    receptionist = Receptionist()
    doctor = Doctor()
    nurse = Nurse()

    dashboard = cli_dashboard.Dashboard(admin,receptionist,doctor,nurse,currentdate=day)

    dashboard.loginPrompt()


    # ====================UNCOMMENT THIS PART TO AUTOMATICALLY ADD SOME SAMPLE DATA========================
    # print(admin.login("admin", "admin123"))
    # print(admin.getUserSession())

    # print(user_session)

    # for user in temp_data.temporaryUsers:
    #     addedStatus = admin.addUser(user)
    #     print(addedStatus)

    # loginStatus = receptionist.login("receptinist01", "password")
    # print("receptionist login status: ", loginStatus)

    # for patient in temp_data.temporaryPatients:
    #     addedStatus = receptionist.addPatient(patientData=patient)
    #     print(addedStatus)
    #=====================================================================================================


    # commit the changes
    conn.commit()

    # close connection
    conn.close()


if __name__ == "__main__":
    main()
