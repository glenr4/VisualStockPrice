import torch
import torch.nn as nn

class StockClassifier(nn.Module):
    def __init__(self):
        super(StockClassifier, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Dynamically calculate the size of the flattened output
        dummy_input = torch.randn(1, 3, 64, 64)  # Adjust 64x64 if your image size is different
        output_size = self._get_conv_output(dummy_input)

        self.fc1 = nn.Linear(output_size, 128)  # Use the calculated size
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(128, 3)  # 3 output classes (up, down, neutral)

    def _get_conv_output(self, shape):
        """Calculates the output size of the convolutional layers."""
        with torch.no_grad():
            x = self.pool1(self.relu1(self.conv1(shape)))
            x = self.pool2(self.relu2(self.conv2(x)))
            return int(torch.prod(torch.tensor(x.size())))

    def forward(self, x):
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        x = x.view(x.size(0), -1)  # Flatten
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)
        return x