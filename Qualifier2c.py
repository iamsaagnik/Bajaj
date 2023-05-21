# -*- coding: utf-8 -*-
"""
Created on Sun May 21 09:57:47 2023

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

def is_valid_phone_number(phone_number):
    # Remove any non-digit characters
    phone_number = ''.join(filter(str.isdigit, phone_number))
    
    # Check the length of the phone number
    if len(phone_number) == 10:
        # Check if the phone number falls within the valid range
        if 6000000000 <= int(phone_number) <= 9999999999:
            return True
    elif len(phone_number) == 12:
        # Check if the phone number has a valid prefix
        if phone_number.startswith('91') or phone_number.startswith('+91'):
            # Check if the remaining digits fall within the valid range
            if 6000000000 <= int(phone_number[2:]) <= 9999999999:
                return True
    
    return False

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
    
    # Check if the phone number is valid
    selected_item['isValidMobile'] = is_valid_phone_number(selected_item['phoneNumber'])
    
    selected_data.append(selected_item)

# Create a DataFrame from the selected data
df = pd.DataFrame(selected_data)

# Transform gender column values
df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

# Rename birthDate column to DOB
df = df.rename(columns={'patientDetails.birthDate': 'DOB'})

# Print the resulting DataFrame
print(df)
