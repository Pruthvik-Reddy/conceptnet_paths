import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
import wandb
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

column_df=pd.read_excel("all_unique_paths.xlsx")
column_list = column_df[0].tolist()

data=pd.read_excel("Relation_Features.xlsx")

X = data[column_list].values
y = data['metaphor'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert data to PyTorch tensors and move to the device
X_train = torch.tensor(X_train, dtype=torch.float32).to(device)
y_train = torch.tensor(y_train, dtype=torch.float32).to(device)
X_test = torch.tensor(X_test, dtype=torch.float32).to(device)
y_test = torch.tensor(y_test, dtype=torch.float32).to(device)

# Define the neural network model
class NeuralNetwork(nn.Module):
    def __init__(self,input_dim):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

# Create an instance of the neural network model and move it to the device
model = NeuralNetwork(X_train.shape[1]).to(device)

# Define the loss function and optimizer
criterion = nn.BCELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)
wandb.init(project='your_project_name', entity='your_entity_name')
wandb.watch(model)
# Train the neural network
epochs = 100
for epoch in range(epochs):
    optimizer.zero_grad()

    # Forward pass
    outputs = model(X_train)
    loss = criterion(outputs, y_train.unsqueeze(1))

    # Backward pass and optimization
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f"Epoch: {epoch+1}, Loss: {loss.item()}")
    wandb.log({'epoch': epoch+1, 'loss': loss.item()})

# Evaluate the model on the testing data
with torch.no_grad():
    model.eval()
    outputs = model(X_test)
    predicted = torch.round(outputs).squeeze().cpu().numpy()
    y_test_cpu = y_test.cpu().numpy()
    accuracy = accuracy_score(y_test_cpu, predicted)
    report = classification_report(y_test, predicted)


print('Accuracy:', accuracy)
print("Report : ",report)
wandb.finish()
