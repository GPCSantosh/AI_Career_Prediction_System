import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

print("Training started...")

cyber = pd.read_csv("../data/salaries_cyber.csv")
ds = pd.read_csv("../data/Latest_Data_Science_Salaries.csv")

ds.columns = [c.lower().replace(" ", "_") for c in ds.columns]
cyber.columns = [c.lower().replace(" ", "_") for c in cyber.columns]

cyber = cyber.rename(columns={
    "job_title":"job_title",
    "experience_level":"experience",
    "employment_type":"employment",
    "company_size":"company_size",
    "salary_in_usd":"salary"
})

ds = ds.rename(columns={
    "job_title":"job_title",
    "experience_level":"experience",
    "employment_type":"employment",
    "company_size":"company_size",
    "salary_in_usd":"salary"
})

df = pd.concat([
    cyber[["job_title","experience","employment","company_size","salary"]],
    ds[["job_title","experience","employment","company_size","salary"]]
])

df = df.dropna()

encoders = {}
for col in ["experience","employment","company_size","job_title"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df[["experience","employment","company_size"]]
y = df["job_title"]

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X,y)

pickle.dump(model, open("model.pkl","wb"))
pickle.dump(encoders, open("encoders.pkl","wb"))

df.to_csv("processed_salary_data.csv", index=False)

print("MODEL TRAINED SUCCESSFULLY")
