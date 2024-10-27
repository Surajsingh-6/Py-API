from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import shutil,os
from models import pred
app = FastAPI()

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5174","http://localhost:5173"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def root():
    return {'hello': 'Suraj!'}


@app.post('/getdata')
async def upload_file(
    file: UploadFile = File(...),
    date: str = Form(...),
    ltp: str = Form(...)
):
    try:
        print(f"Received date: {date}, ltp: {ltp}")

        if os.path.exists('data/data.csv'):
            os.remove('data/data.csv')
        if file.content_type not in ['application/csv', 'text/csv']:
            return {"error": "Invalid file type. Please upload a CSV file."}, 400


        with open('data/data.csv', 'wb') as f:
            shutil.copyfileobj(file.file, f)

        pred_val, accuracy = pred(date, ltp)

        print(f"Prediction: {pred_val}, Accuracy: {accuracy}")
        return {'prediction': pred_val, 'accuracy': accuracy}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}, 500
