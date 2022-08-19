import os
from tabulate import tabulate


class Dashboard:
    admin = None
    receptionist = None
    doctor = None
    nurse = None
    currentdate = None

    # function to clear the console
    def clearConsole(self): return os.system('cls'
                                             if os.name in ('nt', 'dos') else 'clear')

    usertypes = ["admin", "receptionist", "doctor", "nurse"]

    def __init__(self, admin, receptionist, doctor, nurse, currentdate=None):
        self.admin = admin
        self.receptionist = receptionist
        self.doctor = doctor
        self.nurse = nurse
        self.currentdate = currentdate

    def loginUnsuccessful(self, message=None):
        print("Login failed")
        if message is not None:
            print(message)
        print("Press any key to continue...")
        input()
        self.clearConsole()
        self.loginPrompt()

    def continuePrompt(self):
        print("Press any key to continue...")
        input()
        if self.admin.getUserSession()["usertype"] == "admin":
            self.adminDashboard()
        elif self.admin.getUserSession()["usertype"] == "receptionist":
            self.receptionistDashboard()
        elif self.admin.getUserSession()["usertype"] == "doctor":
            self.doctorDashboard()
        elif self.admin.getUserSession()["usertype"] == "nurse":
            self.nurseDashboard()
        else:
            self.loginPrompt()

    def loginPrompt(self):
        self.clearConsole()
        print("================================HMS Login================================")
        usertype = input(
            "Usertype:  [ 1=admin | 2=receptionist | 3=doctor | 4=nurse ]\n: choice: ")
      

        try:
            if int(usertype) < 1 or int(usertype) > 4:
                self.loginUnsuccessful(message="Invalid usertype")
        except ValueError:
            self.loginUnsuccessful(message="Invalid usertype")

        username = input("Username: ")
        password = input("Password: ")

        usertype = self.usertypes[int(usertype)-1]

        if usertype == "admin":
            if self.admin.login(username, password):
                print("Login successful")
                print("Press any key to go to admin dashboard")
                input()
                self.adminDashboard()
            else:
                self.loginUnsuccessful()

        elif usertype == "receptionist":
            if self.receptionist.login(username, password):
                print("Login successful")
                print("Press any key to go to receptionist dashboard")
                input()
                self.receptionistDashboard()
            else:
                self.loginUnsuccessful()

        elif usertype == "doctor":
            if self.doctor.login(username, password):
                print("Login successful")
                print("Press any key to go to doctor dashboard")
                input()
                self.doctorDashboard()
            else:
                self.loginUnsuccessful()

        elif usertype == "nurse":
            if self.nurse.login(username, password):
                print("Login successful")
                print("Press any key to go to nurse dashboard")
                input()
                self.nurseDashboard()
            else:
                self.loginUnsuccessful()

        else:
            self.loginUnsuccessful()

    def adminDashboard(self):
        self.clearConsole()

        print("Showing Admin page")
        print("1. Add new user")
        print("2. Show all users")
        print("3. Show all patients")
        print("4. Show all doctors")
        print("5. Show all nurses")
        print("6. Remove user")
        print("7. Get user information")
        print("8. Update user information")
        print("9. Logout")

        choice = input("Choice: ")

        if choice == "1":
            self.clearConsole()

            username = input("Username: ")
            firstname = input("Firstname: ")
            lastname = input("Lastname: ")

            fullname = firstname.title() + " " + lastname.title()

            password = input("Password: ")
            usertype = input(
                "Usertype \n\t1.admin \n\t2.receptionist \n\t3.doctor \n\t4.nurse\n: choice:")

            usertype = self.usertypes[int(usertype)-1]

            gender = input("Gende [M/F]: choice: ")
            age = input("Age: ")
            phone = input("Phone: ")

            newUser = {
                "username": username,
                "fullname": fullname,
                "password": password,
                "usertype": usertype,
                "gender": gender,
                "age": age,
                "phone": phone
            }

            if self.admin.addUser(newUser):
                print("User added successfully")
                self.admin.commitChanges()
                self.continuePrompt()
            else:
                print("User not added")

        elif choice == "2":
            self.clearConsole()

            foundUsers = self.admin.getAllUsers()
            headers = ["UserID", "Username", "Fullname",
                       "Password", "Usertype", "Gender", "Age", "Phone"]
            print(tabulate(foundUsers, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "3":
            self.clearConsole()

            foundPatients = self.admin.getAllPatients()
            headers = ["PatientID", "Name", "Age", "Phone", "Address",
                       "Gender", "Blood Group", "Weight", "Height", "Date"]
            print(tabulate(foundPatients, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "4":
            self.clearConsole()

            foundDoctors = self.admin.getAllUsers(usertype="doctor")
            headers = ["DoctorID", "Username", "Fullname",
                       "Password", "Usertype", "Gender", "Age", "Phone"]
            print(tabulate(foundDoctors, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "5":
            foundNurses = self.admin.getAllUsers(usertype="nurse")
            headers = ["NurseID", "Username", "Fullname",
                       "Password", "Usertype", "Gender", "Age", "Phone"]
            print(tabulate(foundNurses, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "6":
            self.clearConsole()

            print("Removing user by userId or username?")
            print("1. UserId")
            print("2. Username")

            userid = None
            username = None

            isRemoved = False

            choice = input("Choice: ")
            if choice == "1":
                userid = input("UserID: ")
                isRemoved = self.admin.removeUser(userid=userid)
            elif choice == "2":
                username = input("Username: ")
                isRemoved = self.admin.removeUser(username=username)

            if isRemoved:
                print("User removed successfully")
                self.continuePrompt()
            else:
                print("User not removed")
                self.continuePrompt()

        elif choice == "7":
            self.clearConsole()

            userid = int(input("Enter UserID to get information: "))

            

            foundUsers = self.admin.getAllUsers()

            for user in foundUsers:
                if user[0] == userid:
                    foundUsers = [user]
                    break
            headers = ["UserID", "Username", "Fullname",
                       "Password", "Usertype", "Gender", "Age", "Phone"]
            print(tabulate(foundUsers, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "8":
            self.clearConsole()

            print("listing all users")

            foundUsers = self.admin.getAllUsers()

            print("userID\tUsername")
            for i in range(len(foundUsers)):
                print(f"{foundUsers[i][0]}\t{foundUsers[i][1]}")

            userid = input("Enter UserID of the user: ")

            isUpdated = False

            newUserData = {"username": "",
                           "fullname": "", 
                           "password": "", 
                           "usertype": "",
                           "gender": "", 
                           "age": 0, 
                           "phone": ""}

            print("Enter new information")

            newUserData['username'] = input("New Username: ")
            firstname = input("New Firstname: ")
            lastname = input("New Lastname: ")
            newUserData['fullname'] = firstname.title() + " " + lastname.title()
            newUserData['password'] = input("New Password: ")

            usertype = input(
            "Usertype:  [ 1=admin | 2=receptionist | 3=doctor | 4=nurse ]\n: choice: ")
      

            try:
                if int(usertype) < 1 or int(usertype) > 4:
                    self.loginUnsuccessful(message="Invalid usertype")
            except ValueError:
                self.loginUnsuccessful(message="Invalid usertype")


            newUserData['usertype'] = self.usertypes[int(usertype)-1]

            newUserData['gender'] = input("Gender [M/F]: ")
            newUserData['age'] = int(input("Age: "))
            newUserData['phone'] = input("Phone: ")

            
            isUpdated = self.admin.updateUser(
                userid=userid, update=newUserData)

            if isUpdated:
                print("User updated successfully")
                self.continuePrompt()
            else:
                print("User not updated")
                self.continuePrompt()

        elif choice == "9":
            if self.admin.logout():
                print("Logout successful")
                print("Press any key to continue...")
                input()
                self.loginPrompt()
            else:
                print("Logout failed")
                print("Press any key to continue...")
                input()
                self.adminDashboard()

    def receptionistDashboard(self):
        self.clearConsole()
        print("Showing Receptionist page")
        print("1. Add new patient")
        print("2. Show all patients")
        print("3. Show all available doctors")
        print("4. Make appointment")
        print("5. List appointments")
        print("6. Remove patient")
        print("7. Get patient information")
        print("8. Update patient information")
        print("9. Logout")

        choice = input("Choice: ")

        if choice == "1":
            self.clearConsole()

            newPatient = {}

            try:
                newPatient['name'] = input("Name: ")
                newPatient['age'] = int(input("Age: "))
                newPatient['phone'] = input("Phone: ")
                newPatient['address'] = input("Address: ")
                newPatient['gender'] = input("Gender [M/F]: ")
                newPatient['bloodgroup'] = input("Blood Group: ")
                newPatient['weight'] = int(input("Weight: "))
                newPatient['height'] = int(input("Height: "))
                newPatient['date'] = self.currentdate
            except Exception as e:
                print(e)
                print("Patient not added")
                self.continuePrompt()

            if self.receptionist.addPatient(newPatient):
                print("Patient added successfully")
            else:
                print("Patient not added")
            self.continuePrompt()

        elif choice == "2":
            self.clearConsole()
            foundPatients = self.admin.getAllPatients()
            headers = ["PatientID", "Name", "Age", "Phone", "Address",
                       "Gender", "Blood Group", "Weight", "Height", "Date"]
            print(tabulate(foundPatients, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "3":
            self.clearConsole()
            date = input("On Which date (YYYY-MM-DD)? ")
            foundDoctors = self.receptionist.fetchAvailableDoctors(date)

            if(foundDoctors is not None):
                print("ID\tName")
                for i in range(len(foundDoctors['data'])):
                    print(f"{foundDoctors['data'][i][0]}\t{foundDoctors['data'][i][2]}")
                self.continuePrompt()
            else:
                print("No doctors available")
                self.continuePrompt()

        elif choice == "4":
            self.clearConsole()
            appointmentData = {}

            print("------------------Patients----------------- ")
            print("ID\tName")
            foundPatients = self.admin.getAllPatients()
            for patient in foundPatients:
                print(f"{patient[0]}\t{patient[1]}")

            
            print("------------------Doctors----------------- ")
            foundDoctors = self.receptionist.fetchAvailableDoctors()

            if(foundDoctors is not None):
                print("ID\tName")
                for i in range(len(foundDoctors['data'])):
                    print(f"{foundDoctors['data'][i][0]}\t{foundDoctors['data'][i][2]}")
            else:
                print("No doctors available")

            try:
                appointmentData['patientid'] = int(input("PatientID: "))
                appointmentData['doctorid'] = int(input("DoctorID: "))
                appointmentData['date'] = input("Date: [YYYY-MM-DD] ")
                appointmentData['time'] = input("Time: ")
                appointmentData['symptoms'] = input("Symptoms: ")

            except Exception as e:
                print(e)
                print("Incorrect input")
                self.continuePrompt()

            appointment = self.receptionist.makeAppointment(appointmentData=appointmentData)
            if appointment is not None:
                print("Appointment made successfully")
                print("AppointmentID: " + str(appointment['data']))

                self.receptionist.commitChanges()
            else:
                print("Appointment not made")
            self.continuePrompt()

        elif choice == "5":
            self.clearConsole()
            foundAppointments = self.receptionist.getAllAppointments()
            headers = ["Appt.ID", "Recept.ID", "Pat.ID",
                       "Doc.ID", "Date", "Time", "Symptoms","Status"]
            print(tabulate(foundAppointments, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "6":
            self.clearConsole()
            patientid = input("PatientID: ")
            if self.receptionist.removePatientById(patientid):
                print("Patient removed successfully")
                self.receptionist.commitChanges()
            else:
                print("Patient not removed")
            self.continuePrompt()

        elif choice == "7":
            self.clearConsole()
            patientid = int(input("PatientID: "))
            foundPatient = self.receptionist.getPatientInfoById(patientid)
            headers = ["PatientID", "Name", "Age", "Phone", "Address",
                       "Gender", "Bloodgroup", "Weight", "Height", "Date"]
            print(tabulate(foundPatient, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "8":
            self.clearConsole()
            print("Updating patient information")

            patientid = input("PatientID: ")
            newPatientData = {}

            newPatientData['name'] = input("Name: ")
            newPatientData['age'] = int(input("Age: "))
            newPatientData['phone'] = input("Phone: ")
            newPatientData['address'] = input("Address: ")
            newPatientData['gender'] = input("Gender [M/F]: ")
            newPatientData['bloodgroup'] = input("Blood Group: ")
            newPatientData['weight'] = int(input("Weight: "))
            newPatientData['height'] = int(input("Height: "))
            newPatientData['date'] = self.currentdate

            filter = {"patientid": patientid}
            if self.receptionist.updatePatientById(patientid,patientData=newPatientData):
                print("Patient updated successfully")
                self.receptionist.commitChanges()
            else:
                print("Patient updated successfully")
            self.continuePrompt()

        elif choice == "9":
            if self.receptionist.logout():
                print("Logout successful")
                print("Press any key to continue...")
                input()
                self.loginPrompt()
            else:
                print("Logout failed")
                print("Press any key to continue...")
                input()
                self.receptionistDashboard()

    def doctorDashboard(self):
        self.clearConsole()
        print("Showing Doctor page")
        print("1. Show all patients under me")
        print("2. Show all available nurses")
        print("3. Show patient medical history")
        print("4. Update patient medical report")
        print("5. Logout")

        choice = input("Choice: ")

        if choice == "1":
            self.clearConsole()
            foundPatients = self.doctor.getPatientsAppointed()
            print("pat.ID\tName")
            for patient in foundPatients['data']:
                print(f"{patient[0]}\t{patient[1]}")

            self.continuePrompt()

        elif choice == "2":
            self.clearConsole()
            foundNurses = self.doctor.getAvailableNurses()
            headers = ["NurseID", "Name"]

            if(foundNurses is not None):
                print(tabulate(foundNurses, headers, tablefmt="grid"))
            self.continuePrompt()

        elif choice == "3":
            self.clearConsole()

            print("patients list")
            foundPatients = self.doctor.getPatientsAppointed()
            print("pat.ID\tName")
            for patient in foundPatients['data']:
                print(f"{patient[0]}\t{patient[1]}")

            print("showing patient medical history")
            patientid = int(input("PatientID: "))

            medicalRecords = self.doctor.getMedicalRecords(patientID=patientid)

            if medicalRecords is not None and len(medicalRecords['data']) > 0:
                headers = ["PatientID", "DoctorID","NurseID","prescription", "Operation", "remarks","demographics","injection","Vaccinated"]
                print(tabulate(medicalRecords['data'], headers, tablefmt="grid"))
            else:
                print("No medical records found")
            self.continuePrompt()

        elif choice == "4":
            self.clearConsole()
            print("Updating patient medical report")
            medicalRecordData = {}

            foundPatients = self.doctor.getPatientsAppointed()
            print("------------------Patients----------------- ")
            print("pat.ID\tName")
            for patient in foundPatients['data']:
                print(f"{patient[0]}\t{patient[1]}")

            print("----------------Nurses----------------- ")
            foundNurses = self.doctor.getAvailableNurses()
            headers = ["NurseID", "Name"]

            if(foundNurses is not None):
                print(tabulate(foundNurses, headers, tablefmt="grid"))

            print("UPDATE MEDICAL RECORD:")

            try:
                medicalRecordData['patient_id'] = int(input("PatientID: "))
                medicalRecordData['doctor_id'] = self.doctor.getUserSession()[
                    'id']
                medicalRecordData['nurse_id'] = int(input("NurseID: "))
                medicalRecordData['prescription'] = input("Prescription: ")
                medicalRecordData['operation'] = input("Operation: ")
                medicalRecordData['remarks'] = input("Remarks: ")
                medicalRecordData['demographics'] = input("Demographics: ")
                medicalRecordData['injection'] = input("Injection: ")

            except Exception as e:
                print(e)
                print("Incorrect input")
                self.continuePrompt()

            updatedMedicalRecord = self.doctor.createOrUpdateMedicalRecord(
                medicalRecordData)
            if updatedMedicalRecord is not None:
                print(updatedMedicalRecord['message'])
                print(updatedMedicalRecord['data'])
                self.doctor.commitChanges()
                self.continuePrompt()

            else:
                print("Medical record not updated")
            self.continuePrompt()

        elif choice == "5":
            self.clearConsole()
            if self.doctor.logout():
                print("Logout successful")
                print("Press any key to continue...")
                input()
                self.loginPrompt()
            else:
                print("Logout failed")
                print("Press any key to continue...")
                input()
                self.doctorDashboard()

    def nurseDashboard(self):
        self.clearConsole()
        print("Showing Nurse page")
        print("1. Show all patient under me")
        print("2. Show Patient medical record")
        print("3. Set Vaccination Status")
        print("4. Logout")

        choice = input("Choice: ")

        if choice == "1":
            self.clearConsole()
            foundMedicalRecords = self.nurse.getPatientsAppointed()

            if foundMedicalRecords['data'] is not None:
                print(foundMedicalRecords['message'])

                headers = ["PatientID", "Name"]
                print(tabulate(foundMedicalRecords['data'], headers, tablefmt="grid"))
                
                self.continuePrompt()

            else:
                print(foundMedicalRecords['message'])
                self.continuePrompt()

        elif choice == "2":
            self.clearConsole()
            print("Showing patient medical record")
            patientid = int(input("PatientID: "))

            medicalRecords = self.nurse.getPatientMedicalRecords(patientID=patientid)

            if medicalRecords['data'] is not None and len(medicalRecords['data']) > 0:
                headers = ["PatientID", "DoctorID","NurseID","prescription", "Operation", "remarks","demographics","injection","Vaccinated"]
                print(tabulate(medicalRecords['data'], headers, tablefmt="grid"))
            else:
                print("No medical records found")
            self.continuePrompt()

        elif choice == "3":
            self.clearConsole()

            medicalRecords = self.nurse.getPatientMedicalRecords(patientID=None)

            if medicalRecords['data'] is not None and len(medicalRecords['data']) > 0:
                for record in medicalRecords['data']:
                    print("Prescp.ID\tPat.ID\tVaccinated")
                    print(f"{record[0]}\t\t{record[1]}\t{record[9]}")
                    


            print("Setting vaccination status")
            patientID = input("PatientID: ")
            prescriptionID = input("PrescriptionID (MedicalRecordID): ")

            vaccinationStatus = input("Vaccinated: [y/n] ")
            vaccinationStatus = 1 if vaccinationStatus == "y" or vaccinationStatus == "Y" else 0
            if self.nurse.setVaccinatedStatus(patientID, prescriptionID, vaccinationStatus)['data']:
                print("Vaccination status set")
                self.nurse.commitChanges()
            else:
                print("Vaccination status not updated")
            self.continuePrompt()

        elif choice == "4":
            self.clearConsole()
            if self.nurse.logout():
                print("Logout successful")
                print("Press any key to continue...")
                input()
                self.loginPrompt()
            else:
                print("Logout failed")
                print("Press any key to continue...")
                input()
                self.nurseDashboard()
