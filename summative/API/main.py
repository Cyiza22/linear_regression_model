from fastapi import FastAPI
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

# Load dataset and train model
data = pd.read_csv("Student_Lifestyle_Dataset.csv")  # Replace with your dataset name

# Example: Assume 'feature1', 'feature2' as predictors, and 'target' as the outcome
X = data[["feature1", "feature2"]]  # Replace with actual column names
y = data["target"]  # Replace with actual column name

# Train-test split and model fitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

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

# To run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
