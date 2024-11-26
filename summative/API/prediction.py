from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pickle

# Load the trained model
with open("linear_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
origins = ["*"]  # Adjust this to specific origins for better security
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for input validation
class InputData(BaseModel):
    study_hours: float = Field(..., ge=0, le=24, description="Study hours per day (0-24)")
    extracurricular_hours: float = Field(..., ge=0, le=24, description="Extracurricular activity hours per day (0-24)")
    sleep_hours: float = Field(..., ge=0, le=24, description="Sleep hours per day (0-24)")
    social_hours: float = Field(..., ge=0, le=24, description="Socializing hours per day (0-24)")

# Prediction endpoint
@app.post("/predict")
def predict(data: InputData):
    # Convert input data to numpy array
    input_values = np.array([
        data.study_hours,
        data.extracurricular_hours,
        data.sleep_hours,
        data.social_hours,
    ]).reshape(1, -1)

    try:
        # Predict using the model
        prediction = model.predict(input_values)[0]
        return {"predicted_gpa": round(prediction, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
