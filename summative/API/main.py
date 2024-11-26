from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

# Load the dataset
data = pd.read_csv("Student_Lifestyle_Dataset.csv")

# Standardize column names for consistency
data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")

# Define predictors and target
X = data[['study_hours', 'physical_activity_hours']]  # Predictors
y = data['cgpa']  # Target variable

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Output results
print("Model training complete!")
print("Model Coefficients:", model.coef_)
print("Model Intercept:", model.intercept_)

# Define FastAPI app
app = FastAPI(title="Prediction API", description="A simple API to predict target values", version="1.0")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic model for input validation
class PredictionInput(BaseModel):
    feature1: float = Field(..., title="Feature 1", description="First input feature", ge=0, le=100)
    feature2: float = Field(..., title="Feature 2", description="Second input feature", ge=0, le=100)

@app.post("/predict")
def predict(input_data: PredictionInput):
    # Convert input to model-ready format
    input_array = np.array([[input_data.feature1, input_data.feature2]])
    prediction = model.predict(input_array)
    
    return {"prediction": prediction[0]}

import nest_asyncio
nest_asyncio.apply()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


