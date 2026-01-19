from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

model = pickle.load(open("model.pkl","rb"))
encoders = pickle.load(open("encoders.pkl","rb"))
salary_data = pd.read_csv("processed_salary_data.csv")

class CareerInput(BaseModel):
    domain: str
    experience: str
    employment: str
    company_size: str

@app.get("/")
def home():
    return {"status":"AI Career Backend running"}

@app.post("/predict")
def predict(data: CareerInput):
    try:
        exp = encoders["experience"].transform([data.experience])[0]
        emp = encoders["employment"].transform([data.employment])[0]
        size = encoders["company_size"].transform([data.company_size])[0]

        pred = model.predict([[exp,emp,size]])[0]
        role = encoders["job_title"].inverse_transform([pred])[0]

        match = salary_data[salary_data["job_title"]==pred]["salary"]
        min_salary = int(match.min())
        max_salary = int(match.max())

        readiness = round(len(match)/len(salary_data)*100,2)

        return {
            "predicted_role": role,
            "salary_range_usd": f"${min_salary} - ${max_salary}",
            "readiness_score": f"{readiness}%"
        }
    except:
        return {"predicted_role":"No matching role found","salary_range_usd":"N/A","readiness_score":"0%"}
