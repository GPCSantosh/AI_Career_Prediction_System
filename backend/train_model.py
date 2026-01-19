import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

print("Training started...")

cyber = pd.read_csv("../data/salaries_cyber.csv")
ds = pd.read_csv("../data/Latest_Data_Science_Salaries.csv")

# Select only relevant columns
cyber = cyber[["job_title", "salary_in_usd"]].copy()
ds = ds[["Job Title", "Salary in USD"]].copy()

# Rename columns to match
cyber.columns = ["job_title", "salary"]
ds.columns = ["job_title", "salary"]

# Assign domain
def assign_domain(title):
    title = title.lower()
    if "data" in title or "ml" in title or "scientist" in title:
        return "DataScience"
    elif "devops" in title:
        return "DevOps"
    elif "tester" in title or "qa" in title:
        return "Testing"
    elif "security" in title or "cyber" in title:
        return "Cyber"
    elif "cloud" in title:
        return "Cloud"
    else:
        return "SoftwareDev"

cyber["domain"] = cyber["job_title"].apply(assign_domain)
ds["domain"] = ds["job_title"].apply(assign_domain)

# Combine safely
df = pd.concat([cyber, ds], ignore_index=True)

print("Combined dataset shape:", df.shape)

# Encode categorical columns
domain_encoder = LabelEncoder()
job_encoder = LabelEncoder()

df["domain"] = domain_encoder.fit_transform(df["domain"])
df["job_title"] = job_encoder.fit_transform(df["job_title"])

X = df[["domain", "salary"]]
y = df["job_title"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "model.pkl")
joblib.dump(domain_encoder, "domain_encoder.pkl")
joblib.dump(job_encoder, "job_encoder.pkl")

print("Model trained and saved successfully.")
