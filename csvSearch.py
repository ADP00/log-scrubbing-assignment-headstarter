import csv
import os
from loguru import logger
from emailAlert import emailAlert

path = os.getcwd()
csvDir = path+"/CSV"

def csvSearch():
    custInfoFiles = os.listdir(csvDir)
    for filename in custInfoFiles:
        if filename.endswith(".csv"):
            file = open(os.path.join(csvDir, filename),"r")
            reader = csv.reader(file, delimiter="\t")

            for row in reader:
                if reader.line_num == 1:
                    continue #skips the headers at the start

                #Check for potential phone numbers and ssn in the area code and zip code columns of the premade csv files.
                if len(row[0]) == 10 or len(row[0]) == 9:
                    logger.critical(f"Data found in {filename} in row {reader.line_num} contains personal identifiable information in column 1.")
                    
                    #Send email
                    emailAlert("Sensitive information found in logs", f"Data found in {filename} in row {reader.line_num} contains personal identifiable information in column 1.")
                if len(row[2]) == 10 or len(row[2]) == 9:
                    logger.critical(f"Data found in {filename} in row {reader.line_num} contains personal identifiable information in column 3.")

                    #send email
                    emailAlert("Sensitive information found in logs", f"Data found in {filename} in row {reader.line_num} contains personal identifiable information in column 3.")

csvSearch()