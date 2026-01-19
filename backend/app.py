import joblib
import pandas as pd
from fastapi import FastAPI
from schemas import CareerInput
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

app = FastAPI()

# Load dataset
salary_df = pd.read_csv("processed_salary_data.csv")

# Train encoders
le_domain = LabelEncoder().fit(salary_df["domain"])
le_exp = LabelEncoder().fit(salary_df["experience"])
le_emp = LabelEncoder().fit(salary_df["employment"])
le_size = LabelEncoder().fit(salary_df["company_size"])
le_job = LabelEncoder().fit(salary_df["job_title"])

# Encode dataset
salary_df["domain"] = le_domain.transform(salary_df["domain"])
salary_df["experience"] = le_exp.transform(salary_df["experience"])
salary_df["employment"] = le_emp.transform(salary_df["employment"])
salary_df["company_size"] = le_size.transform(salary_df["company_size"])
salary_df["job_title"] = le_job.transform(salary_df["job_title"])

# Train model
X = salary_df[["domain", "experience", "employment", "company_size", "salary"]]
y = salary_df["job_title"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

print("Model trained on startup successfully.")


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

        avg_salary = salary_df[salary_df["domain"].str.lower() == data.domain.lower()]["salary"].mean()

        if pd.isna(avg_salary):
            return {
                "predicted_role": "Domain not trained yet",
                "salary_range_usd": "N/A"
            }

        job_encoded = model.predict([[dom, exp, emp, size, avg_salary]])[0]
        job_title = le_job.inverse_transform([job_encoded])[0]

        return {
            "predicted_role": job_title,
            "salary_range_usd": f"${int(avg_salary*0.6)} - ${int(avg_salary*1.4)}"
        }

    except ValueError as e:
        return {"error": str(e)}
