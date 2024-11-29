from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pickle

# Load the trained model
try:
    with open("linear_regression_model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError("Model file 'linear_regression_model.pkl' not found.")

# Create FastAPI app
app = FastAPI(title="Student CGPA Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for input validation
class StudentInput(BaseModel):
    study_hours: float = Field(
        ..., 
        ge=0, 
        le=24, 
        description="Daily study hours (0-24)"
    )
    extracurricular_hours: float = Field(
        ..., 
        ge=0, 
        le=24, 
        description="Daily extracurricular hours (0-24)"
    )
    sleep_hours: float = Field(
        ..., 
        ge=0, 
        le=24, 
        description="Daily sleep hours (0-24)"
    )
    social_hours: float = Field(
        ..., 
        ge=0, 
        le=24, 
        description="Daily social hours (0-24)"
    )
    physical_activity_hours: float = Field(
        ..., 
        ge=0, 
        le=24, 
        description="Daily physical activity hours (0-24)"
    )
    stress_level: str = Field(
        ..., 
        description="Stress level (Low/Moderate/High)"
    )

# Helper function to convert stress level
def convert_stress_level(stress_level):
    stress_map = {"Low": 1, "Moderate": 2, "High": 3}
    return stress_map.get(stress_level.capitalize(), 2)

# Prediction endpoint
@app.post("/predict")
def predict_cgpa(input_data: StudentInput):
    # Prepare input for prediction
    input_array = np.array([
        input_data.study_hours,
        input_data.extracurricular_hours,
        input_data.sleep_hours,
        input_data.social_hours,
        input_data.physical_activity_hours,
        convert_stress_level(input_data.stress_level)
    ]).reshape(1, -1)
    
    try:
        # Make prediction
        prediction = model.predict(input_array)[0]
        return {
            "predicted_cgpa": round(prediction, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Student CGPA Prediction API"}

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)