from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal
import json
import os

app = FastAPI()

FILE_NAME = "patient.json"


# ------------------ MODELS ------------------

class Patient(BaseModel):
    id: str = Field(..., example="P001")
    name: str = Field(..., example="Ahmed")
    city: str = Field(..., example="Mumbai")
    age: int = Field(..., gt=0, example=22)
    gender: Literal["male", "female", "others"]
    height: float = Field(..., gt=0, example=175)
    weight: float = Field(..., gt=0, example=72)


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal["male", "female", "others"]] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)


# ------------------ FILE FUNCTIONS ------------------

def load_data():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


# ------------------ CREATE ------------------

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)

    return {"message": "Patient created successfully"}


# ------------------ READ ------------------

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"id": patient_id, **data[patient_id]}


@app.get("/all")
def get_all_patients():
    return load_data()


# ------------------ UPDATE ------------------

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    update_data = patient_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        data[patient_id][key] = value

    save_data(data)

    return {"message": "Patient updated successfully"}


# ------------------ DELETE ------------------

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)

    return {"message": "Patient deleted successfully"}