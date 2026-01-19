from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import CareerInput
import pandas as pd
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

csv_path = os.path.join(os.path.dirname(__file__), "processed_salary_data.csv")

salary_df = pd.read_csv(csv_path)

@app.get("/")
def health():
    return {"status": "Backend running successfully"}

@app.post("/predict")
def predict(data: CareerInput):

    matches = salary_df[
        (salary_df["domain"].str.lower() == data.domain.lower()) &
        (salary_df["experience"].str.lower() == data.experience.lower()) &
        (salary_df["employment"].str.lower() == data.employment.lower()) &
        (salary_df["company_size"].str.lower() == data.company_size.lower())
    ]

    if matches.empty:
        return {
            "predicted_role": "No matching role found",
            "salary_range_usd": "N/A"
        }

    role = matches.iloc[0]["job_title"]
    min_salary = int(matches["salary"].min())
    max_salary = int(matches["salary"].max())

    return {
        "predicted_role": role,
        "salary_range_usd": f"${min_salary} - ${max_salary}"
    }
