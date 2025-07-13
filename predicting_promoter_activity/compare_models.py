import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from mord import LogisticAT
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

def compare_models(feature_file):
    print("Loading data...")
    df = pd.read_csv(feature_file)

    X = df.drop(columns=["label"])
    y = df["label"]

    print(" Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Model 1: Ordinal Logistic Regression
    print("\nTraining Ordinal Logistic Regression...")
    ord_model = LogisticAT()
    ord_model.fit(X_train, y_train)
    y_pred_ord = ord_model.predict(X_test)

    acc_ord = accuracy_score(y_test, y_pred_ord)
    print(f"Ordinal Accuracy: {acc_ord:.4f}")
    print("Classification Report (Ordinal):\n", classification_report(y_test, y_pred_ord))

    cm_ord = confusion_matrix(y_test, y_pred_ord)
    print("Confusion Matrix (Ordinal):\n", cm_ord)

    # Model 2: Random Forest Classifier
    print("\nTraining Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)

    acc_rf = accuracy_score(y_test, y_pred_rf)
    print(f"Random Forest Accuracy: {acc_rf:.4f}")
    print("Classification Report (Random Forest):\n", classification_report(y_test, y_pred_rf))

    cm_rf = confusion_matrix(y_test, y_pred_rf)
    print("Confusion Matrix (Random Forest):\n", cm_rf)
