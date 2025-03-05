 
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from app.database import collection
from app.followup_questions import generate_follow_up_questions

# Load datasets
df_symptoms = pd.read_csv("data/cleaned_disease_symptoms_latest.csv").set_index("Disease")
df_first_aid = pd.read_csv("data/cleaned_first_aid_recommendations_latest.csv").set_index("Disease")

# Convert symptoms into binary features
df_symptoms = df_symptoms.notna().astype(int)  # Convert symptoms into 1 (present) and 0 (absent)

# Train model
disease_names = df_symptoms.index.tolist()
X = df_symptoms.values
model = MultinomialNB()
model.fit(X, np.arange(len(disease_names)))  # Train on binary data

def diagnose(input_data):
    symptoms = input_data.symptoms
    
    # Create binary input vector for symptoms
    input_vector = np.array([1 if s in symptoms else 0 for s in df_symptoms.columns]).reshape(1, -1)
    
    # Predict diseases
    disease_probs = model.predict_proba(input_vector)[0]
    top_indices = disease_probs.argsort()[-3:][::-1]  # Get top 3 predictions
    top_diseases = [(disease_names[i], disease_probs[i]) for i in top_indices]

    # Low confidence handling
    if top_diseases[0][1] < 0.6:
        return {
            "follow_up": "Confidence is low. Answer these additional questions:",
            "questions": generate_follow_up_questions(symptoms)
        }

    # Retrieve AstraDB medical context
    doc_context = ""
    try:
        embedding = [float(x) for x in symptoms]  # Ensure embedding format
        cursor = collection.find({}, {"sort": {"$vector": embedding}, "limit": 5})
        documents = cursor.toArray()
        doc_context = "\n".join([doc["text"] for doc in documents])
    except Exception:
        doc_context = "No additional context available."

    # Generate response
    response = {"input_symptoms": symptoms, "predictions": []}
    for disease, confidence in top_diseases:
        first_aid_steps = df_first_aid.loc[disease].dropna().tolist() if disease in df_first_aid.index else ["No first-aid info."]
        response["predictions"].append({
            "disease": disease,
            "confidence_score": f"{round(confidence * 100, 2)}%",
            "first_aid_recommendations": first_aid_steps,
            "medical_context": doc_context
        })
    
    return response

def refine_diagnosis(input_data):
    symptoms = input_data.symptoms
    follow_up_responses = input_data.follow_up_responses  # Get follow-up answers

    # Add follow-up answers as additional symptoms
    if follow_up_responses:
        for key, value in follow_up_responses.items():
            if isinstance(value, list):  # If it's a list, extend symptoms
                symptoms.extend(value)
            else:
                symptoms.append(value)  # If it's a string, just append

    # Run the updated symptom list through the model again
    input_vector = np.array([1 if s in symptoms else 0 for s in df_symptoms.columns]).reshape(1, -1)
    disease_probs = model.predict_proba(input_vector)[0]
    top_indices = disease_probs.argsort()[-3:][::-1]  # Get top 3 predictions
    top_diseases = [(disease_names[i], disease_probs[i]) for i in top_indices]

    # Retrieve first aid steps and AstraDB medical context
    response = {"input_symptoms": symptoms, "predictions": []}
    for disease, confidence in top_diseases:
        first_aid_steps = df_first_aid.loc[disease].dropna().tolist() if disease in df_first_aid.index else ["No first-aid info."]
        response["predictions"].append({
            "disease": disease,
            "confidence_score": f"{round(confidence * 100, 2)}%",
            "first_aid_recommendations": first_aid_steps
        })

    return response
