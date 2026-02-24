from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
import json
from typing import Annotated, Literal
import os

app = FastAPI()

FILE_NAME = "patient.json"


# ------------------ MODEL ------------------

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient', example='P001')]
    name: Annotated[str, Field(..., description='Name of the patient', example='John Doe')]
    city: Annotated[str, Field(..., description='City of the patient', example='New York')]
    age: Annotated[int, Field(..., gt=0, description='Age of the patient', example=30)]
    gender: Annotated[Literal['male', 'female', 'others'],
                      Field(..., description='Gender Of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height in cm', example=170)]
    weight: Annotated[float, Field(..., gt=0, description='Weight in kg', example=70.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / ((self.height / 100) ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


# ------------------ FILE HANDLING ------------------

def load_data():
    if not os.path.exists(FILE_NAME):
        return {}

    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


# ------------------ ENDPOINTS ------------------

@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,
                            detail='Patient with this ID already exists')

    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            'message': 'Patient created successfully',
            'patient': patient.model_dump()
        }
    )


@app.get('/patient/{patient_id}')
def get_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,
                            detail='Patient not found')

    patient_data = data[patient_id]
    patient = Patient(id=patient_id, **patient_data)

    return patient


@app.get('/all')
def get_all_patients():
    data = load_data()

    patients = []
    for pid, details in data.items():
        patient = Patient(id=pid, **details)
        patients.append(patient)

    return patients