import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

print("Training started...")

cyber = pd.read_csv("../data/salaries_cyber.csv")
ds = pd.read_csv("../data/Latest_Data_Science_Salaries.csv")

# Normalize columns
cyber = cyber.rename(columns={"job_title": "job_title", "salary_in_usd": "salary"})
ds = ds.rename(columns={"Job Title": "job_title", "Salary in USD": "salary"})

cyber = cyber[["job_title", "salary"]]
ds = ds[["job_title", "salary"]]

# Assign domains
def assign_domain(title):
    title = title.lower()
    if "data" in title or "ml" in title or "scientist" in title:
        return "Data Science"
    elif "devops" in title or "cloud" in title:
        return "DevOps"
    elif "tester" in title or "qa" in title:
        return "Software Testing"
    elif "security" in title or "cyber" in title:
        return "Cyber Security"
    else:
        return "Software Development"

cyber["domain"] = cyber["job_title"].apply(assign_domain)
ds["domain"] = ds["job_title"].apply(assign_domain)

df = pd.concat([cyber, ds], ignore_index=True)

# Encode features
domain_enc = LabelEncoder()
title_enc = LabelEncoder()

df["domain"] = domain_enc.fit_transform(df["domain"])
df["job_title"] = title_enc.fit_transform(df["job_title"])

X = df[["domain", "salary"]]
y = df["job_title"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(domain_enc, "domain_encoder.pkl")
joblib.dump(title_enc, "title_encoder.pkl")

print("Model trained and saved successfully.")
