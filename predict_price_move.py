from StockClassifier import StockClassifier
import torch
from torchvision import transforms
from PIL import Image
import torch.nn.functional as F

# Image to categorise
image_path='images/test/up/^AORD_2022-09-30_2022-10-06__pre50_post5_pct4_up.png'

###########################
# Load the saved model
model = StockClassifier()  # Make sure this is the same architecture you used for training
model.load_state_dict(torch.load('model/stock_classifier.pth'))
model.eval()  # Set the model to evaluation mode

# Define the device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load and preprocess the image
image = Image.open(image_path).convert('RGB')   # Limit to 3 channels to match model

transform = transforms.Compose([
    transforms.Resize((64, 64)),  # Match the size used during training
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

image = transform(image)
image = image.unsqueeze(0)  # Add a batch dimension
image = image.to(device)  # Move the image to the device

# Get the prediction
with torch.no_grad():
    output = model(image)
    probabilities = F.softmax(output.data, dim=1)  # Apply softmax
    _, predicted = torch.max(output.data, 1)
    confidence = torch.max(probabilities).item()  # Get the confidence

# Map the prediction to a category
categories = {0: 'up', 1: 'down', 2: 'neutral'}  # Adjust if your category indices are different
predicted_category = categories[predicted.item()]

print(f"Predicted category: {predicted_category}")
print(f"Confidence: {confidence * 100:.2f}%")