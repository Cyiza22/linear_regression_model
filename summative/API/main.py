from prediction import app
import uvicorn

host = "0.0.0.0"  
port = 8000       

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)

