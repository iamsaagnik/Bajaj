import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


with open('DataEngineeringQ2.json') as file:
    data = json.load(file)

columns = ['appointmentId', 'phoneNumber', 'patientDetails.firstName', 'patientDetails.lastName',
           'patientDetails.gender', 'patientDetails.birthDate', 'consultationData.medicines']
selected_data = []

def is_valid_phone_number(phone_number):
    
    phone_number = ''.join(filter(str.isdigit, phone_number))
    
    if len(phone_number) == 10:
        if 6000000000 <= int(phone_number) <= 9999999999:
            return True
    elif len(phone_number) == 12:
        if phone_number.startswith('91') or phone_number.startswith('+91'):
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

    selected_item['fullName'] = f"{selected_item['patientDetails.firstName']} {selected_item['patientDetails.lastName']}"
    
    selected_item['isValidMobile'] = is_valid_phone_number(selected_item['phoneNumber'])
    
    selected_data.append(selected_item)

df = pd.DataFrame(selected_data)

df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

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

    selected_item['fullName'] = f"{selected_item['patientDetails.firstName']} {selected_item['patientDetails.lastName']}"

    selected_item['noOfMedicines'] = len(selected_item['consultationData.medicines'])
    
    active_medicines = 0
    inactive_medicines = 0
    for medicine in selected_item['consultationData.medicines']:
        if medicine['isActive']:
            active_medicines += 1
        else:
            inactive_medicines += 1
    
    selected_item['noOfActiveMedicines'] = active_medicines
    selected_item['noOfInactiveMedicines'] = inactive_medicines
    
    selected_data.append(selected_item)

df = pd.DataFrame(selected_data)

df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

df = df.rename(columns={'patientDetails.birthDate': 'DOB'})


def calculate_age(birth_date):
    if birth_date is None:
        return None

    birth_date = datetime.strptime(birth_date, '%Y-%m-%dT%H:%M:%S.%fZ')

    age = datetime.now().year - birth_date.year

    if birth_date.month > datetime.now().month:
        age -= 1
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

    selected_item['fullName'] = f"{selected_item['patientDetails.firstName']} {selected_item['patientDetails.lastName']}"
    
    selected_item['Age'] = calculate_age(selected_item['patientDetails.birthDate'])
    
    selected_data.append(selected_item)

df = pd.DataFrame(selected_data)

df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

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

    selected_data.append(selected_item)

df = pd.DataFrame(selected_data)

df['patientDetails.gender'] = df['patientDetails.gender'].map({'M': 'male', 'F': 'female'}).fillna('others')

df = df.rename(columns={'patientDetails.birthDate': 'DOB'})

aggregated_data = {
    'Age': df['Age'].mean(),
    'gender': df['patientDetails.gender'].value_counts().to_dict(),
    'validPhoneNumbers': df['isValidMobile'].sum(),
    'appointments': len(df),
    'medicines': df['noOfMedicines'].sum(),
    'activeMedicines': df['noOfActiveMedicines'].sum()
}


with open('agrData.json', 'w') as file:
    json.dump(aggregated_data, file, indent=4)

gender_counts = df['patientDetails.gender'].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%')
plt.title('Number of Appointments by Gender')
plt.axis('equal')
plt.show()
