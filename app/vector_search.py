from app.database import collection

def search_medical_context(symptom_embedding):
    try:
        cursor = collection.find({}, {"sort": {"$vector": symptom_embedding}, "limit": 5})
        return [doc["text"] for doc in cursor.toArray()]
    except Exception:
        return ["No relevant medical insights found."]