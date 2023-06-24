import pyodbc
import sqlSettings
from datetime import date
import csv

conn = pyodbc.connect(sqlSettings.get_settings())
cursor = conn.cursor()


def runReport():
    fields = ['Last', 'First', 'Sex', 'Dob', 'Last Encounter', 'Date of report', str(date.today())]
    ptList = []
    dateOfReport = date.today()
    dateOfReport = int(str(dateOfReport).replace('-', ''))
    listOfPts = getPtsByAge(dateOfReport)
    count = 0
    count2 = 0
    for i in listOfPts:
        count2 = count2 + 1
        dob = i[7]
        if dob != '':
            dob_int = int(dob)
            age = int((dateOfReport - dob_int)/10000)
            encounterDate = getLastEncounterDate(str(i[0]))
            NoneType = type(None)

            if not isinstance(encounterDate, NoneType):
                dos = str(encounterDate[6])[:10]
                dos = int(dos[:4] + dos[5:7] + dos[8:10])
                if dos >= (dateOfReport - 30000):
                    count = count + 1
                    Val = encounterDate[6]
                    dobFormatted = dob[:4] + "-" + dob[4:6] + "-" + dob[6:8]
                    ptData = [str(i[2]), str(i[1]), str(i[6]), str(dobFormatted), str(encounterDate[6])[:10]]
                    ptList.append(ptData)
        print(str(count) + " : " + str(count2))

    fileName = "over64report.csv"
    with open(fileName, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(ptList)


def getLastEncounterDate(PtId):
    data = [PtId]
    cursor.execute('SELECT * FROM Encounters WHERE Patient_ID=? ORDER BY visit_date DESC ', data)
    encounter_list = cursor.fetchone()
    return encounter_list


def getPtsByAge(Date):
    olderThenDate = Date-640000
    data = [olderThenDate]
    cursor.execute("SELECT * FROM Gen_Demo WHERE CAST(birthdate as int) <= ? AND deceased = 0 ORDER BY birthdate DESC", data)
    patient_list = cursor.fetchall()
    return patient_list

