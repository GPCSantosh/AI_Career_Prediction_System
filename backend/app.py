from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import os
import pandas as pd
from schemas import CareerInput

app = FastAPI()
@app.get("/")
def health():
    return {"status": "AI Career Prediction Backend is running"}

@app.get("/")
def root():
    return {
        "status": "AI Career Prediction Backend is running",
        "docs": "/docs"
    }

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
le_exp, le_emp, le_size, le_domain, le_job = pickle.load(
    open(os.path.join(BASE_DIR, "encoders.pkl"), "rb")
)

salary_df = pd.read_csv(
    os.path.join(BASE_DIR, "processed_salary_data.csv")
)

# ---------------- Encoder safety ----------------
def encode_safe(encoder, value, field):
    if value not in encoder.classes_:
        raise ValueError(
            f"Invalid {field}. Allowed values: {list(encoder.classes_)}"
        )
    return encoder.transform([value])[0]

# ---------------- API ----------------
@app.post("/predict")
def predict(data: CareerInput):
    try:
        exp = encode_safe(le_exp, data.experience, "experience")
        emp = encode_safe(le_emp, data.employment, "employment")
        size = encode_safe(le_size, data.company_size, "company_size")

        # Handle unknown domains safely
        if data.domain not in le_domain.classes_:
            return {
                "predicted_role": "Domain not trained yet",
                "salary_range_usd": "N/A"
            }

        dom = le_domain.transform([data.domain])[0]

        job_encoded = model.predict([[exp, emp, size, dom]])[0]
        job_title = le_job.inverse_transform([job_encoded])[0]

        job_salary = salary_df[salary_df["job_title"] == job_encoded]["salary"]

        return {
            "predicted_role": job_title,
            "salary_range_usd": f"${int(job_salary.min())} - ${int(job_salary.max())}"
        }

    except ValueError as e:
        return {"error": str(e)}
