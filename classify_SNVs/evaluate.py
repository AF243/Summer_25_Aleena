from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import torch
from torch.utils.data import DataLoader

def evaluate_model(model, test_dataset):
    model.eval()
    loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    all_preds = []
    all_labels = []
    all_probs = []

    with torch.no_grad():
        for X_batch, y_batch in loader:
            outputs = model(X_batch)
            probs = torch.sigmoid(outputs).squeeze().numpy()
            preds = (probs >= 0.5).astype(int)

            all_probs.extend(probs)
            all_preds.extend(preds)
            all_labels.extend(y_batch.numpy())

    print("Accuracy:", accuracy_score(all_labels, all_preds))
    print("Precision:", precision_score(all_labels, all_preds, zero_division=0))
    print("Recall:", recall_score(all_labels, all_preds, zero_division=0))
    print("F1 Score:", f1_score(all_labels, all_preds, zero_division=0))

    return all_labels, all_preds, all_probs
