import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
file_path = "Student_Lifestyle_Dataset.csv"
data = pd.read_csv(file_path)

# Inspect the first few rows to ensure proper loading
print(data.head())

# Define features (X) and target (y)
X = data[["Study_Hours", "Extracurricular_Hours", "Sleep_Hours", "Social_Hours", "Physical_Activity_Hours", "Stress_Level"]]
y = data["CGPA"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model to a .pkl file
with open("linear_regression_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as 'linear_regression_model.pkl'.")
