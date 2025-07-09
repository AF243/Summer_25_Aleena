import os
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc

def extract_features_from_mol(mol):
    try:
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        tpsa = Descriptors.TPSA(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        rot_bonds = Descriptors.NumRotatableBonds(mol)
        ring_count = Descriptors.RingCount(mol)

        return pd.Series({
            'molecular_weight': mw,
            'logP': logp,
            'TPSA': tpsa,
            'H_bond_donors': hbd,
            'H_bond_acceptors': hba,
            'rotatable_bonds': rot_bonds,
            'ring_count': ring_count
        })
    except:
        return pd.Series({
            'molecular_weight': None,
            'logP': None,
            'TPSA': None,
            'H_bond_donors': None,
            'H_bond_acceptors': None,
            'rotatable_bonds': None,
            'ring_count': None
        })

# Function to load molecules from an SDF file and extract features
def process_sdf(filepath, label):
    print(f" Processing: {filepath}")
    suppl = Chem.SDMolSupplier(filepath)
    data = []

    for mol in suppl: 
        if mol is not None:
            features = extract_features_from_mol(mol)
            features['label'] = label
            data.append(features)

    return pd.DataFrame(data)

# Main function to run the pipeline
def main():
    # Step 1: Load drug-like and non-drug-like ligands
    drug_file = "drug_like.sdf"
    non_drug_file = "non_drug_like.sdf"

    drug_df = process_sdf(drug_file, label=1)       # 1 = Drug-like
    non_drug_df = process_sdf(non_drug_file, label=0)  # 0 = Non-drug-like

    # Step 2: Combine datasets
    full_data = pd.concat([drug_df, non_drug_df], ignore_index=True)
    print("\n Dataset preview:")
    print(full_data.head())

    # Drop rows with any missing values (optional)
    full_data.dropna(inplace=True)

    # Step 3: Prepare X and y
    x = full_data.drop('label', axis=1)
    y = full_data['label']

    # Step 4: Train/test split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Step 5: Load and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    # Step 6: Predict and evaluate
    y_pred = model.predict(x_test)

    print("\n Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\n Classification Report:")
    print(classification_report(y_test, y_pred))

    print(f" Accuracy Score: {accuracy_score(y_test, y_pred):.4f}")
    print(f" Sample Predictions: {y_pred[:10]}")

    # Step 7: Save dataset (optional)
    full_data.to_csv("ligand_dataset.csv", index=False)
    print("\nFeatures saved to: ligand_dataset.csv")

    # Confusion Matrix
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.savefig('Confusion_matrix.png', dpi=300)
    print("image saved as Confusion_matrix.png")
    plt.close()

    # Feature Importances 
    importances = model.feature_importances_
    indices = importances.argsort()[::-1][:10]
    top_n = len(indices)  
    plt.bar(range(top_n), importances[indices])
    plt.xticks(range(top_n), [x.columns[i] for i in indices], rotation=45)
    plt.title("Top Feature Importances")
    plt.savefig('top_features.png', dpi=300)
    print("image saved as top_features.png ")
    plt.close()

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_pred)
    plt.plot(fpr, tpr, label=f"AUC = {auc(fpr, tpr):.2f}")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.title("ROC Curve")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.legend()
    plt.savefig('ROC_Curve.png', dpi=300)
    print("image saved as ROC_Curve.png")
    plt.close()

if __name__ == "__main__":
    main()
