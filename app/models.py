from pydantic import BaseModel
from typing import List, Dict, Union, Optional

class SymptomInput(BaseModel):
    symptoms: List[str]
    follow_up_responses: Optional[Dict[str, Union[str, List[str]]]] = None

class DiagnosisResponse(BaseModel):
    input_symptoms: List[str]
    predictions: List[Dict[str, str]]
