from prediction import app
import uvicorn

host = "localhost"
port = 8000

if __name__ == '__main__':
    uvicorn.run(app, host=host, port=port)
