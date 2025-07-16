from parse_and_label import parse_and_label_vcf
from feature_extraction import extract_features
from sklearn.model_selection import train_test_split
from visualization import plot_training_loss, plot_confusion_matrix, plot_roc_curve
from evaluate import evaluate_model
from torch.utils.data import TensorDataset
import torch
from model import ANN
from train import train_model
import numpy as np

def main():
    # Step 1: Parse and label the VCF
    # cleaned_csv = parse_and_label_vcf("clinvar.vcf")

    # Step 2: Extract features
    X, y = extract_features("cleaned_variants.csv")
    X = X[:50000]
    y = y[:50000]

    mask = ~np.isnan(X).any(axis=1)
    X = X[mask]
    y = y[mask]

    # Step 3: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Step 4: Convert to tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    # Step 5: Create TensorDatasets
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

    # Step 6: Initialize model
    input_dim = X_train.shape[1]
    model = ANN(input_dim)

    # Step 7: Train the model
    losses = train_model(model, train_dataset, epochs=10)
    plot_training_loss(losses)

    # Step 8: Evaluate the model
    all_labels, all_preds, all_probs = evaluate_model(model, test_dataset)
    plot_confusion_matrix(all_labels, all_preds)
    plot_roc_curve(all_labels, all_probs)

if __name__ == "__main__":
    main()
