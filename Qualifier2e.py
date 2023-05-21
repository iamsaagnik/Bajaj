# -*- coding: utf-8 -*-
"""
Created on Sun May 21 10:04:12 2023

@author: Saagnik
"""

import json
import pandas as pd
from datetime import datetime

# Read the JSON file
with open('DataEngineeringQ2.json') as file:
    data = json.load(file)

# Extract the required columns from JSON
columns = ['appointmentId', 'phoneNumber', 'patientDetails.firstName', 'patientDetails.lastName',
           'patientDetails.gender', 'patientDetails.birthDate', 'consultationData.medicines']
selected_data = []

def calculate_age(birth_date):
    if birth_date is None:
        return None

    # Convert the birth date string to datetime object
    birth_date = datetime.strptime(birth_date, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Calculate the age based on the current date
    age = datetime.now().year - birth_date.year

    # Adjust the age if the birth month is greater than the current month
    if birth_date.month > datetime.now().month:
        age -= 1
    # Adjust the age if the birth month is equal to the current month
    elif birth_date.month == datetime.now().month:
        if birth_date.day > datetime.now().day:
            age -= 1

    return age

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
    
    # Calculate the age based on the birth date
    selected_item['Age'] = calculate_age(selected_item['patientDetails.birthDate'])
    
    selected_data.append(selected_item)

# Create a DataFrame from the selected data
df = pd.DataFrame(selected_data)

# Transform gender column values
df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

# Rename birthDate column to DOB
df = df.rename(columns={'patientDetails.birthDate': 'DOB'})

# Print the resulting DataFrame
print(df)
