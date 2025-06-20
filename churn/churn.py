import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("./data/customers_clean.csv")


churn_map = {"Aktif": 0, "Cuti": 0, "Blokir": 1, "Putus": 1}
df["Churn"] = df["Status"].map(churn_map)
df.drop(
    ["Name", "Address"],
    axis=1,
    inplace=True,
)

# Cek hasil
# print("Kolom yang digunakan:", df.columns)
# print(df.head(10))

# ==== 3 Pisahkan fitur dan target ====
x = df.drop(columns=["Churn"])
y = df["Churn"]

# ==== 4 Pipeline Preprocessing dan Model ====
# Karena paket dan fiber optik adalah kategorikal
categorical_features = ["Paket", "Fiber Optic"]
preprocessor = ColumnTransformer(
    transformers=[("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42)),
    ]
)

# ==== 5 Split Data ====
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# ==== 6 Training ====
model.fit(X_train, y_train)

# ==== 7 Evaluasi ====
y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClasification Report:")
print(classification_report(y_test, y_pred))

print("\n===================================================")

print("Total awal:", len(pd.read_csv("./data/customers_clean.csv")))
print("Setelah mapping churn:", df.shape[0])
print("Jumlah data test:", len(X_test))
print("Jumlah data train:", len(X_train))

print("\n===================================================")
print("Cek Hasil")
print("Kolom yang digunakan:", df.columns)
print(df.head(10))

print("\n===================================================")
# Hitung Jumlah nilai unik pada kolom "status"
status_counts = df["Status"].value_counts()
print("\nJumlah Status:")
print(status_counts)

print("\n===================================================")
# Hitung Jumlah nilai unik pada kolom "Churn"
churn_counts = df["Churn"].value_counts()
print("\nJumlah Churn:")
print(churn_counts)

print("\n===================================================")
# HItung jumlah nilai unik pada kolom "Status" setelah pemetaan (Mapping.)
status_counts = df["Status"].map(churn_map).value_counts()
print("\nJumlah status setelah pemetaan (Mapping)")
print(status_counts)
