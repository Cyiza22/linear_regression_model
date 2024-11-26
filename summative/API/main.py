# Import required libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Initialize the FastAPI app
app = FastAPI(title="Student Lifestyle Prediction API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; replace "*" with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for input validation
class PredictionRequest(BaseModel):
    study_hours: float = Field(..., ge=0, le=24, description="Hours spent studying daily (0-24)")
    extracurricular_hours: float = Field(..., ge=0, le=12, description="Hours spent on extracurricular activities daily (0-12)")
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours spent sleeping daily (0-24)")

# Endpoint for predictions
@app.post('/predict')
def predict(request: PredictionRequest):
    """
    Predicts CGPA based on input variables.
    Args:
        request (PredictionRequest): Input variables for prediction.
    Returns:
        dict: The predicted CGPA.
    """
    # Example simple prediction logic (replace with your actual model logic)
    cgpa = (request.study_hours * 0.4) + (request.extracurricular_hours * 0.2) + (request.sleep_hours * 0.1)

    # Clip the CGPA to a maximum of 4.0
    cgpa = min(cgpa, 4.0)

    return {"predicted_cgpa": round(cgpa, 2)}

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)



