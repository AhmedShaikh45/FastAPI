from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 should have emergency contact number')
        return model

    @classmethod
    def insert_patient_data(cls, patient: 'Patient'):
        print(patient.name)
        print(patient.email)
        print(patient.age)
        print(patient.weight)
        print(patient.married)
        print(patient.allergies)
        print(patient.contact_details)
        print('inserted')

    @classmethod
    def update_patient_data(cls, patient: 'Patient'):
        print(patient.name)
        print(patient.email)
        print(patient.age)
        print(patient.weight)
        print(patient.married)
        print(patient.allergies)
        print(patient.contact_details)
        print('updated')


patient_info = {
    'name': 'Ahmed',
    'email': 'ahmed@hdfc.com',
    'age': 61,
    'weight': 72.4,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'phone': '7977393273','emergency': '9876543210'
    }
}

patient1 = Patient(**patient_info)

Patient.insert_patient_data(patient1)