from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title = 'Name of the Patient',
                               description ='Give the Name of the patient',
                                examples ='Ahmed Shaikh')]
    email : EmailStr
    linkedin_url : AnyUrl
    age: int
    weight: Annotated[float, Field(gt = 0, strict =True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Optional[List[str]] = Field(max_length=5)
    contact_details: Dict[str, str]
    
    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        
        valid_domains = ['hdfc.com','icici.com']
        #abc@gmail.com
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domains:
          raise ValueError('Not a valid email')
            
        return value
    
    @field_validator('name',mode='after')
    @classmethod
    def transform_name(cld,value):
        return value.upper()
    

    @field_validator('age',mode='before')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')
        

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.linkedin_url)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted')

def update_patient_data(patient: Patient):
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
    'email' : 'ahmed@hdfc.com',
    'linkedin_url': 'https://www.linkedin.com/in/ahmed-shaikh2004/',
    'age': 21,
    'weight': 72.4,
    'married': True,
    'allergies': ['pollen', 'dust'],  # ✅ fixed here
    'contact_details': {
        'email': 'ahmed@gmail.com',
        'phone': '7977393273'
    }
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)