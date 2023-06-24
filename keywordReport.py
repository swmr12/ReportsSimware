# from dataclasses import fields

import pyodbc
import sqlSettings
from datetime import date
import csv


def getEncounters(Date, years, cursor):
    year = Date.year
    year = int(year) - int(years)
    oldest_encounter_date = [str(year) + "-" + str(Date.month) + "-" + str(Date.day)]
    cursor.execute('SELECT * FROM dbo.Encounters WHERE visit_date >= CONVERT(datetime, ?) ORDER BY visit_date desc',
                   oldest_encounter_date)
    list_encounters = cursor.fetchall()
    return list_encounters


def getEncounterData(Encounter_ID, cursor):
    search_list = [Encounter_ID, str(102)]
    cursor.execute('SELECT * FROM dbo.Encounter_Data WHERE EncountID=? AND  Object_Type=?', search_list)
    Encounter_DataList = cursor.fetchone()
    return Encounter_DataList


def getPtInfo(ptId, cursor):
    search_list = [str(ptId)]
    cursor.execute('SELECT * FROM dbo.Gen_Demo WHERE Patient_ID=?', search_list)
    return cursor.fetchone()


def toCsv(dictDiag, header, cursor):
    dataToWrite = []
    # ['Last', 'First', 'Sex', 'Dob', 'Last Encounter', 'diabetes', 'hypertension', 'Date of report', '2023-06-04']
    for key in dictDiag:
        ptInfo = getPtInfo(key, cursor)
        print(key)
        print(ptInfo)
        try:
            listOfDiag = dictDiag[key]
            length = len(listOfDiag)
            dob = str(ptInfo[7])
            dobFormatted = dob[:4] + "-" + dob[4:6] + "-" + dob[6:8]
            dosFormatted = str(listOfDiag[(int(length) - 1)])[0:10]
            rowList = [str(ptInfo[1]), str(ptInfo[2]), str(ptInfo[6]), str(dobFormatted), str(dosFormatted)]
            isPositive = 0
            for x in range((len(listOfDiag) - 1)):
                rowList.append(listOfDiag[x])
                if listOfDiag[x] == 1:
                    isPositive = 1
            if isPositive == 1:
                dataToWrite.append(rowList)
            else:
                print("No Diagnosis")

        except:
            print(Exception)

    fileName = r'C:\reports\KeywordReport.csv'
    with open(fileName, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(dataToWrite)


def runReport():
    conn = pyodbc.connect(sqlSettings.get_settings())
    cursor = conn.cursor()

    diag_list = ['ANEMIA', 'VITAMIN B12 DEFICIENCY', 'SMOKING', 'DYSLIPIDEMIA', 'HYPERLIPIDEMIA', 'ANXIETY', 'COLITIS',
                 'HTN', 'HEART MURMUR', 'CAROTID STENOSIS',
                 'VITAMIN D DEFICIENCY', 'OBESITY', 'DIVERTICULOSIS', 'AAA', 'ABNORMAL EKG', 'OSTEOPENIA',
                 'DEPRESSION', 'GERD', 'ASHD', 'HEART DISEASE', 'HYPOTHYROIDISM', 'ASTHMA', 'ANEURYSM', 'FIBROMYALGIA',
                 'PULMONARY FIBROSIS', 'OSTEOPOROSIS',
                 'Obstructive Sleep Apnea', 'OSA', 'PMR', 'POLYMYALGIA RHEUMATICA', 'DERMATOMYOSITIS',
                 'ATRIAL FIBRILLATION', 'BACK PAIN', 'CHRONIC PAIN', 'HYPERGLYCEMIA',
                 'BPH', 'NOCYURIA', 'MIGRAINE', 'DIABETES', 'HYPERTENSION']

    # key for dictionary is PT id
    dictionary = {}

    fields = ['Last', 'First', 'Sex', 'Dob', 'Last Encounter']
    for i in diag_list:
        fields.append(i)
    fields.append('Date of report')
    fields.append(str(date.today()))

    ptList = []
    dateOfReport = date.today()
    EncountersInDateRange = getEncounters(dateOfReport, 2, cursor)

    count = 0
    count2 = 0
    for i in EncountersInDateRange:
        Encounter_data = getEncounterData(i[0], cursor)
        index = 0
        NoneType = type(None)
        if not isinstance(Encounter_data, NoneType):
            listOfDiags = []
            for diag_listIT in diag_list:
                listOfDiags.append(0)
            listOfDiags.append(str(i[6]))

            if str(i[1]) in dictionary:
                # print("DICT key exists")
                listOfDiags = dictionary[str(i[1])]

            print(Encounter_data[0])
            for j in diag_list:
                if str(j) in str(Encounter_data[3]).upper():
                    print("YES : " + str(j))
                    listOfDiags[index] = 1
                    count2 = count2 + 1
                # else:
                #     print("NO " + str(Encounter_data[0]))
                index = index + 1
            count = count + 1

            dictionary[str(i[1])] = listOfDiags

            print(str(listOfDiags))
        else:
            print("NONE")
        print(str(count) + " : " + str(count2))

    toCsv(dictionary, fields, cursor)

    cursor.close()


if __name__ == '__main__':
    runReport()
