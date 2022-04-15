import csv
import os
import re
from loguru import logger
from emailAlert import emailAlert

path = os.getcwd()
csvDir = path+"/CSV"

def csvSearch():
    custInfoFiles = os.listdir(csvDir)
    for filename in custInfoFiles:
        if filename.endswith(".csv"):
            file = open(os.path.join(csvDir, filename),"r")
            reader = csv.reader(file, delimiter=",")

            coords = dict()

            for row in reader:
                if reader.line_num == 1:
                    continue #skips the headers at the start

                
                r = reader.line_num
                msg = f"Data found in {filename} in row {r} contains personal identifiable information in column "

                #Checks for potential pii in the columns of the row
                #Checks for 9 digit SSNs, 10 digit phone numbers, and letters in the area code column
                if (row[0].isnumeric() and (len(row[0]) == 10 or len(row[0]) == 9)) or re.search('[a-zA-Z]', row[0]):
                    logger.critical(msg+"1.")
                    emailAlert("Sensitive information found in logs", msg+"1.")
                    addCoord(coords, r-1, 0)

                #Checks for the same things in the zip code column
                if (row[0].isnumeric() and (len(row[2]) == 10 or len(row[2]) == 9)) or re.search('[a-zA-Z]', row[2]):
                    logger.critical(msg+"3.")
                    emailAlert("Sensitive information found in logs", msg+"3.")
                    addCoord(coords, r-1, 2)

                #Checks for any numbers in the town name column
                if re.search('[0-9]', row[1]):
                    logger.critical(msg+"2.")
                    emailAlert("Sensitive information found in logs", msg+"2.")
                    addCoord(coords, r-1, 1)
            
            file.close()
            if len(coords) > 0:
                csvWrite(filename, coords)


def csvWrite(filename, coords):
    zipContent = "00000"
    areaCodeContent = "000"
    townContent = "Sensitive Data removed"

    #file must be reopened since reader already iterated and cannot write while iterating
    file = open(os.path.join(csvDir, filename), "r")
    reader = csv.reader(file, delimiter=",")

    currentContent = list(reader)
    file.close()
    #logger.debug(currentContent)

    for row,columns in coords.items():
        for column in columns:
            #Replaces pii with content that will not cause an alert
            if column == 0:
                currentContent[row][column] = areaCodeContent
            elif column == 1:
                currentContent[row][column] = townContent
            elif column == 2:
                currentContent[row][column] = zipContent

    file = open(os.path.join(csvDir, filename), "w", newline="")
    writer = csv.writer(file)
    writer.writerows(currentContent)
    file.close()

#Since pii can be in more than one column in a row, the dict needs to store a list of values for a key
def addCoord(coords, row, col):
    if row not in coords:
        coords[row] = [col]
    else:
        coords[row].append(col)


csvSearch()