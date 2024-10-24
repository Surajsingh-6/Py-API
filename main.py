from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import shutil,os
from models import pred
app = FastAPI()

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
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
    if os.path.exists('data/data.csv'):
        os.remove('data/data.csv')

    with open('data/data.csv', 'wb') as f:
        shutil.copyfileobj(file.file, f)
    
    pred_val, accuracy = pred(date, ltp)
    return {'prediction': pred_val, 'accuracy': accuracy}