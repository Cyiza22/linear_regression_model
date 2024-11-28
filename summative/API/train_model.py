import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load the dataset
data = pd.read_csv("./Student_Lifestyle_Dataset.csv")

# Define features (X) and target (y)
# Replace these columns with the relevant ones from your dataset
X = data[[
    "StudyHours",
    "ExtracurricularHours",
    "SleepHours",
    "SocialHours",
    "PhysicalActivityHours",
    "StressLevel"
]]
y = data["GPA"]  # Replace "GPA" with the actual target column in your dataset

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
with open("linear_regression_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as 'linear_regression_model.pkl'.")

