 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import SymptomInput
from app.inference import diagnose, refine_diagnosis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/diagnose/")
def diagnose_api(input_data: SymptomInput):
    return diagnose(input_data)

@app.post("/diagnose/follow-up/")
def follow_up_diagnose(input_data: SymptomInput):
    return refine_diagnosis(input_data)
