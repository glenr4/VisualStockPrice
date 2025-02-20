import StockClassifier
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

train_images_dir = "images/train"
test_images_dir = "images/test"

# 1. Define the Model (CNN) with dynamic flattening
# Moved to StockClassifier.py

# 2. Load and Preprocess Data
transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Resize images (adjust if needed)
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))  # Use tuples instead of lists
])

train_dataset = datasets.ImageFolder(root=train_images_dir, transform=transform)  # Replace with your actual path
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

test_dataset = datasets.ImageFolder(root=test_images_dir, transform=transform)  # Replace with your actual path
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# 3. Initialize Model, Loss Function, and Optimizer
model = StockClassifier()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. Training Loop
num_epochs = 10  # Adjust as needed
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(num_epochs):
    for images, labels in train_loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

    # 5. Evaluation (on the test set)
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.2f}%')

# 6. Save the Model
torch.save(model.state_dict(), 'model/stock_classifier.pth')