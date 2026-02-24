from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os

app = FastAPI()
FILE_NAME = "patient.json"


class Patient(BaseModel):
    id: str
    name: str
    age: int


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


def load_data():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)


@app.post("/create")
def create(patient: Patient):
    data = load_data()
    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)
    return {"message": "Created"}


@app.put("/edit/{patient_id}")
def update(patient_id: str, update_data: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Not found")

    updates = update_data.model_dump(exclude_unset=True)

    for key, value in updates.items():
        data[patient_id][key] = value

    save_data(data)

    return {"message": "Updated"}


@app.delete("/delete/{patient_id}")
def delete(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Not found")

    del data[patient_id]
    save_data(data)

    return {"message": "Deleted"}