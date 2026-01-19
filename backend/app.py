from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import CareerInput
import pandas as pd
import joblib
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

base = os.path.dirname(__file__)

model = joblib.load(os.path.join(base, "model.pkl"))
encoders = joblib.load(os.path.join(base, "encoders.pkl"))

salary_df = pd.read_csv(os.path.join(base, "processed_salary_data.csv"))

le_domain = encoders["domain"]
le_exp = encoders["experience"]
le_emp = encoders["employment"]
le_size = encoders["company_size"]
le_job = encoders["job_title"]

def encode_safe(encoder, value):
    return encoder.transform([value])[0]

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.post("/predict")
def predict(data: CareerInput):

    try:
        dom = encode_safe(le_domain, data.domain)
        exp = encode_safe(le_exp, data.experience)
        emp = encode_safe(le_emp, data.employment)
        size = encode_safe(le_size, data.company_size)

        avg_salary = salary_df[salary_df["domain"] == data.domain]["salary"].mean()

        pred = model.predict([[dom, exp, emp, size, avg_salary]])[0]
        job_title = le_job.inverse_transform([pred])[0]

        readiness_score = round((avg_salary / 150000) * 100, 2)

        return {
            "predicted_role": job_title,
            "salary_range_usd": f"${int(avg_salary*0.6)} - ${int(avg_salary*1.4)}",
            "readiness_score": readiness_score
        }

    except Exception:
        return {"predicted_role": "No matching role found", "salary_range_usd": "N/A", "readiness_score": 0}
