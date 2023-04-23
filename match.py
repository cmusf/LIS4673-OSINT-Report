import csv
import json
import sys

with open(sys.argv[1], 'r') as nameFile, open(sys.argv[2]) as numbersFile, open(sys.argv[3], 'w') as outputFile:
    nameFile = csv.DictReader(nameFile, delimiter='\t')
    numbersFile = csv.DictReader(numbersFile, delimiter='\t')

    addressRecords = {}

    for record in nameFile:
        # Clean up the record a bit
        recordCopy = record.copy()
        recordClean = {k : v for k, v in recordCopy.items() if v != '' and v != ' ' and v != '\\N' and v != None}

        addressRecords[record['id']] = recordClean

    # Matches IDs from CDEK leak and adds phone numbers to the address records if they exist
    for record in numbersFile:
        if record['id'] in addressRecords:
            addressRecords[record['id']]['phone'] = record['number']
    
    # Write output file as csv
    fieldNames = []


    for record in addressRecords:
        for field in addressRecords[record]:
            if field not in fieldNames:
                fieldNames.append(field)

    writer = csv.DictWriter(outputFile, fieldnames=fieldNames, delimiter='\t')
    writer.writeheader()

    for record in addressRecords:
        writer.writerow(addressRecords[record])
