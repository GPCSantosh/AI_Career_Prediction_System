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
model = joblib.load("model.pkl")
domain_encoder = joblib.load("domain_encoder.pkl")
job_encoder = joblib.load("job_encoder.pkl")


# ---------------- API ----------------
@app.post("/predict")
def predict(data: CareerInput):

    if data.domain not in domain_encoder.classes_:
        return {
            "predicted_role": "Domain not trained yet",
            "salary_range_usd": "N/A"
        }

    domain_code = domain_encoder.transform([data.domain])[0]

    avg_salary = salary_df[salary_df["domain"] == data.domain]["salary"].mean()

    job_code = model.predict([[domain_code, avg_salary]])[0]

    job_title = job_encoder.inverse_transform([job_code])[0]

    min_salary = int(avg_salary * 0.6)
    max_salary = int(avg_salary * 1.4)

    return {
        "predicted_role": job_title,
        "salary_range_usd": f"${min_salary} - ${max_salary}"
    }
