import joblib
import pandas as pd
from fastapi import FastAPI
from schemas import CareerInput

app = FastAPI()

model = joblib.load("model.pkl")

le_domain = joblib.load("domain_encoder.pkl")
le_exp = joblib.load("experience_encoder.pkl")
le_emp = joblib.load("employment_encoder.pkl")
le_size = joblib.load("size_encoder.pkl")
le_job = joblib.load("job_encoder.pkl")


salary_df = pd.read_csv("processed_salary_data.csv")

def encode_safe(encoder, value, field):
    if value not in encoder.classes_:
        raise ValueError(f"Invalid {field}. Allowed values: {list(encoder.classes_)}")
    return encoder.transform([value])[0]

@app.post("/predict")
def predict(data: CareerInput):

    try:
        dom = encode_safe(le_domain, data.domain, "domain")
        exp = encode_safe(le_exp, data.experience, "experience")
        emp = encode_safe(le_emp, data.employment, "employment")
        size = encode_safe(le_size, data.company_size, "company_size")

        avg_salary = salary_df[salary_df["domain"] == data.domain]["salary"].mean()

        job_encoded = model.predict([[dom, exp, emp, size, avg_salary]])[0]
        job_title = le_job.inverse_transform([job_encoded])[0]

        return {
            "predicted_role": job_title,
            "salary_range_usd": f"${int(avg_salary*0.6)} - ${int(avg_salary*1.4)}"
        }

    except ValueError as e:
        return {"error": str(e)}
