import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load the datasetcd ..

data = pd.read_csv("Student_Lifestyle_Dataset.csv")

# Define features (X) and target (y)
X = data[["Study_Hours", "Extracurricular_Hours", "Sleep_Hours", "Social_Hours", "Physical_Activity_Hours"]]

# Convert categorical Stress_Level to numeric
stress_level_map = {"Low": 1, "Moderate": 2, "High": 3}
X["Stress_Level"] = data["Stress_Level"].map(stress_level_map)

y = data["CGPA"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
with open("linear_regression_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as 'linear_regression_model.pkl'.")