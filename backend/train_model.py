import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

print("Training started...")

df = pd.read_csv("processed_salary_data.csv")

le_domain = LabelEncoder()
le_exp = LabelEncoder()
le_emp = LabelEncoder()
le_size = LabelEncoder()
le_job = LabelEncoder()

df["domain"] = le_domain.fit_transform(df["domain"])
df["experience"] = le_exp.fit_transform(df["experience"])
df["employment"] = le_emp.fit_transform(df["employment"])
df["company_size"] = le_size.fit_transform(df["company_size"])
df["job_title"] = le_job.fit_transform(df["job_title"])

X = df[["domain", "experience", "employment", "company_size", "salary"]]
y = df["job_title"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump({
    "domain": le_domain,
    "experience": le_exp,
    "employment": le_emp,
    "company_size": le_size,
    "job_title": le_job
}, "encoders.pkl")

print("Model trained and saved successfully.")
