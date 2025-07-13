import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def train_model(feature_file):
    # Step 1: Load features
    print("Loading feature data...")
    df = pd.read_csv(feature_file)

    X = df.drop(columns=["label"])
    y = df["label"]

    # Step 2: Train/test split
    print("Splitting train/test data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Step 3: Train model
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 4: Evaluate model
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}\n")

    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Step 5: Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Weak (0)", "Strong (1)", "Confirmed (2)"],
                yticklabels=["Weak (0)", "Strong (1)", "Confirmed (2)"])
    
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Random Forest Confusion Matrix")
    plt.savefig("confusion_matrix.png", dpi=300)
    plt.close()

