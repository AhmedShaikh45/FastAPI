from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address


patient_dict = {
    'name': 'ahmed',
    'gender': 'male',
    'age': 21,
    'address': {
        'city': 'mumbai',
        'state': 'maharashtra',
        'pin': '400054'
    }
}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(include=['name','age'])
temp1 = patient1.model_dump(exclude=['name','age'])

print(temp)
print('------------------')
print(temp1)

