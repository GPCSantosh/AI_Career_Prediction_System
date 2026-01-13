import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

print("STEP 1: Script started")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

cyber_path = os.path.join(DATA_DIR, "salaries_cyber.csv")
data_path = os.path.join(DATA_DIR, "Latest_Data_Science_Salaries.csv")

print("STEP 2: Paths")
print("Cyber path:", cyber_path)
print("DataScience path:", data_path)

# -----------------------------
# Load datasets
# -----------------------------
cyber = pd.read_csv(cyber_path)
data = pd.read_csv(data_path)

print("STEP 3: Files loaded")
print("Cyber columns:", list(cyber.columns))
print("DataScience columns:", list(data.columns))

# -----------------------------
# Select required columns
# -----------------------------
cyber = cyber[
    ["job_title", "experience_level", "employment_type", "company_size", "salary_in_usd"]
].copy()

cyber.columns = ["job_title", "experience", "employment", "company_size", "salary"]
cyber["domain"] = "Cyber"

data = data[
    ["Job Title", "Experience Level", "Employment Type", "Company Size", "Salary in USD"]
].copy()

data.columns = ["job_title", "experience", "employment", "company_size", "salary"]
data["domain"] = "DataScience"

print("STEP 4: Columns normalized")

# -----------------------------
# Combine datasets
# -----------------------------
df = pd.concat([cyber, data], ignore_index=True)
print("STEP 5: Datasets combined, shape:", df.shape)

# -----------------------------
# Clean data
# -----------------------------
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
print("STEP 6: Data cleaned, shape:", df.shape)

# -----------------------------
# Encode features
# -----------------------------
le_exp = LabelEncoder()
le_emp = LabelEncoder()
le_size = LabelEncoder()
le_domain = LabelEncoder()
le_job = LabelEncoder()

df["experience"] = le_exp.fit_transform(df["experience"])
df["employment"] = le_emp.fit_transform(df["employment"])
df["company_size"] = le_size.fit_transform(df["company_size"])
df["domain"] = le_domain.fit_transform(df["domain"])
df["job_title"] = le_job.fit_transform(df["job_title"])

print("STEP 7: Encoding completed")

# -----------------------------
# Train model
# -----------------------------
X = df[["experience", "employment", "company_size", "domain"]]
y = df["job_title"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print("STEP 8: Model trained")

# -----------------------------
# Save model
# -----------------------------
model_path = os.path.join(BASE_DIR, "model.pkl")
encoders_path = os.path.join(BASE_DIR, "encoders.pkl")

pickle.dump(model, open(model_path, "wb"))
pickle.dump(
    (le_exp, le_emp, le_size, le_domain, le_job),
    open(encoders_path, "wb")
)
df.to_csv("processed_salary_data.csv", index=False)

print("STEP 9: Files saved")
print("Model path:", model_path)
print("Encoders path:", encoders_path)
print("MODEL TRAINED SUCCESSFULLY")
