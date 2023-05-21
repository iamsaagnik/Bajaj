# -*- coding: utf-8 -*-
"""
Created on Sun May 21 10:15:26 2023

@author: Saagnik
"""

import json
import hashlib
from datetime import datetime
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

def get_phone_number_hash(phone_number):
    # Remove any non-digit characters
    phone_number = ''.join(filter(str.isdigit, phone_number))

    # Normalize the phone number by removing the prefix if present
    if len(phone_number) == 12 and (phone_number.startswith('91') or phone_number.startswith('+91')):
        phone_number = phone_number[2:]
        
    # Hash the normalized phone number using SHA256
    hash_object = hashlib.sha256(phone_number.encode())
    return hash_object.hexdigest()

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
    if is_valid_phone_number(selected_item['phoneNumber']):
        # Hash the valid phone number using SHA256
        selected_item['phoneNumberHash'] = get_phone_number_hash(selected_item['phoneNumber'])
    else:
        selected_item['phoneNumberHash'] = None
    
    selected_data.append(selected_item)

# Create a DataFrame from the selected data
df = pd.DataFrame(selected_data)

# Transform gender column values
df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

# Rename birthDate column to DOB
df = df.rename(columns={'patientDetails.birthDate': 'DOB'})

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

# Export DataFrame to CSV with specified columns and separator
df.to_csv('Final.csv', columns=['appointmentId', 'fullName', 'phoneNumber', 'isValidMobile', 'phoneNumberHash',
                                'patientDetails.gender', 'DOB', 'Age', 'noOfMedicines', 'noOfActiveMedicines',
                                'noOfInactiveMedicines', 'medicineNames'], sep='~', index=False)
