import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle


heart_path = "heart.csv"
df = pd.read_csv(heart_path)


if "HeartDisease" not in df.columns:
    raise KeyError("Coloana 'HeartDisease' nu există în heart.csv")


features = ["Age", "Sex", "ChestPainType", "ExerciseAngina", "FastingBS", "RestingBP", "MaxHR"]
X = df[features]
y = df["HeartDisease"]


X = pd.get_dummies(X, drop_first=True)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


model.feature_names_in_ = X.columns.to_numpy()

y_pred = model.predict(X_test)
print(f"Acuratețe pe test: {accuracy_score(y_test, y_pred):.4f}")
print("Raport clasificare:\n", classification_report(y_test, y_pred))


os.makedirs("model", exist_ok=True)
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model salvat în 'model/model.pkl'")
