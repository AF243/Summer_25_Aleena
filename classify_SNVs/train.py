import torch
from torch import nn
from torch.utils.data import DataLoader

def train_model(model, train_dataset, epochs=10, batch_size=32, lr=0.001):
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Calculate class weights
    labels = torch.tensor([label for _, label in train_dataset])
    pos_weight = torch.tensor([(labels == 0).sum() / (labels == 1).sum()], dtype=torch.float32)

    # Use weighted loss
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    model.train()
    losses = []
    for epoch in range(epochs):
        total_loss = 0
        for X_batch, y_batch in train_loader:
            y_batch = y_batch.unsqueeze(1)
            outputs = model(X_batch) 
            loss = criterion(outputs, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_loss = total_loss / len(train_loader)
        losses.append(avg_loss)
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
    return losses
