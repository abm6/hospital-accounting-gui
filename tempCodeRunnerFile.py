int(admin.login("admin", "admin123"))
    print(admin.getUserSession())

    print(user_session)

    for user in temp_data.temporaryUsers:
        addedStatus = admin.addUser(user)
        print(addedStatus)

    loginStatus = receptionist.login("receptinist01", "password")
    print("receptionist login status: ", loginStatus)

    for patient in temp_data.temporaryPatients:
        addedStatus = receptionist.addPatient(patientData=patient)
       