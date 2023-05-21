# -*- coding: utf-8 -*-
"""
Created on Sun May 21 10:10:48 2023

@author: Saagnik
"""

import json
import pandas as pd

# Read the JSON file
with open('DataEngineeringQ2.json') as file:
    data = json.load(file)

# Extract the required columns from JSON
columns = ['appointmentId', 'phoneNumber', 'patientDetails.firstName', 'patientDetails.lastName',
           'patientDetails.gender', 'patientDetails.birthDate', 'consultationData.medicines']
selected_data = []

for item in data:
    selected_item = {}
    for column in columns:
        keys = column.split('.')
        value = item
        try:
            for key in keys:
                value = value.get(key)
            selected_item[column] = value
        except (KeyError, TypeError):
            selected_item[column] = None

    # Create the derived column fullName
    selected_item['fullName'] = f"{selected_item['patientDetails.firstName']} {selected_item['patientDetails.lastName']}"

    # Count the total number of medicines
    selected_item['noOfMedicines'] = len(selected_item['consultationData.medicines'])
    
    # Count the number of active and inactive medicines
    active_medicines = 0
    inactive_medicines = 0
    active_medicine_names = []
    for medicine in selected_item['consultationData.medicines']:
        if medicine['isActive']:
            active_medicines += 1
            active_medicine_names.append(medicine['medicineName'])
        else:
            inactive_medicines += 1
    
    selected_item['noOfActiveMedicines'] = active_medicines
    selected_item['noOfInactiveMedicines'] = inactive_medicines
    
    # Join the active medicine names with a comma
    selected_item['medicineNames'] = ', '.join(active_medicine_names)
    
    selected_data.append(selected_item)

# Create a DataFrame from the selected data
df = pd.DataFrame(selected_data)

# Transform gender column values
df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

# Rename birthDate column to DOB
df = df.rename(columns={'patientDetails.birthDate': 'DOB'})

# Print the resulting DataFrame
print(df)
