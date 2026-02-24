from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)

    @classmethod
    def insert_patient_data(cls, patient: 'Patient'):
        print("Name:", patient.name)
        print("Email:", patient.email)
        print("Age:", patient.age)
        print("Weight:", patient.weight)
        print("Height:", patient.height)
        print("Married:", patient.married)
        print("Allergies:", patient.allergies)
        print("Contact:", patient.contact_details)
        print("BMI:", patient.calculate_bmi)   # ✅ BMI PRINTED
        print("Inserted")

    @classmethod
    def update_patient_data(cls, patient: 'Patient'):
        print("BMI:", patient.calculate_bmi)   # ✅ Also here
        print("Updated")


patient_info = {
    'name': 'Ahmed',
    'email': 'ahmed@hdfc.com',
    'age': 61,
    'weight': 72.4,
    'height': 1.75,
    'married': True,
    'allergies': ['pollen', 'dust'],
    'contact_details': {
        'phone': '7977393273',
        'emergency': '9876543210'
    }
}

patient1 = Patient(**patient_info)

Patient.insert_patient_data(patient1)