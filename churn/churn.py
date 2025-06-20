import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("./data/customers_clean.csv")

def preprocessing_data(df):
    # Buat churn Map
    churn_map = {"Aktif": 0, "Cuti": 0, "Blokir": 1, "Putus": 1}
    df["Churn"] = df["Status"].map(churn_map)
    df.drop(
        ["Name", "Address"],
        axis=1,
        inplace=True,
    )
    return df


def split_data(df):
    # Pisahkan Fitur dan Target.
    x = df.drop(columns=["Churn"])
    y = df["Churn"]
    # Split data.
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


def training_model(X_train, y_train):
    # Buat Model dan Pipeline
    categorical_features = ["Paket", "Fiber Optic"]
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
        ]
    )
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(random_state=42)),
        ]
    )
    model.fit(X_train, y_train)
    return model


def evaluasi_model(model, X_test, y_test):
    # Lakukan prediksi
    y_pred = model.predict(X_test)
    print("Confusion Matrix:")
    print("                    Prediksi Churn     Prediksi Tidak Churn")
    print(
        "Actual Churn:       ",
        confusion_matrix(y_test, y_pred)[0, 0],
        "            ",
        confusion_matrix(y_test, y_pred)[0, 1],
    )
    print(
        "Actual Non-Churn:   ",
        confusion_matrix(y_test, y_pred)[1, 0],
        "            ",
        confusion_matrix(y_test, y_pred)[1, 1],
    )
    print("\n")
    print("Evaluasi Model:")
    print(classification_report(y_test, y_pred))


def print_data_info(df, X_train, X_test):
    print("Total awal:", len(pd.read_csv("./data/customers_clean.csv")))
    print("Setelah mapping churn:", df.shape[0])
    print("Jumlah data test:", len(X_test))
    print("Jumlah data train:", len(X_train))

# Hitung Jumlah nilai unik pada kolom "Churn"
def print_total_churn(df):
    churn_counts = df["Churn"].value_counts()
    print("\nJumlah Churn:")
    print(churn_counts)

# Total masing masing status. (Aktif, Cuti, Blokir, Putus)
def print_total_status(df):
    status_counts = df["Status"].value_counts()
    print("\nJumlah Status:")
    print(status_counts)

# Cari jumlah pelanggan yang berlangganan fiber optik
def cari_fiber_optik(df):
    fiber_optik_counts = df["Fiber Optic"].value_counts()
    print("\nJumlah Fiber Optik:")
    print(fiber_optik_counts)

# Cari jumlah pelanggan yang berlangganan fiber optik berpootensi churn
def cari_fiber_optik_churn(df):
    fiber_optik_churn = df[df["Churn"] == 1]["Fiber Optic"].value_counts()
    print("\nJumlah Fiber Optik Churn:")
    print(fiber_optik_churn)

# Panggil Fungsi
print("\n===================================================")
df = preprocessing_data(df)
X_train, X_test, y_train, y_test = split_data(df)
model = training_model(X_train, y_train)
evaluasi_model(model, X_test, y_test)
print("\n===================================================")
print_data_info(df, X_train, X_test)
print("\n===================================================")
print_total_churn(df)
print("\n===================================================")
print_total_status(df)
print("\n===================================================")

# Panggil Fungsi untuk hitung Fiber optik
cari_fiber_optik(df)
cari_fiber_optik_churn(df)
print("\n===================================================")




# # print("\n===================================================")
# # # HItung jumlah nilai unik pada kolom "Status" setelah pemetaan (Mapping.)
# status_counts = df["Status"].map(churn_map).value_counts()
# print("\nJumlah status setelah pemetaan (Mapping)")
# print(status_counts)
