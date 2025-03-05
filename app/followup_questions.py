from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Fetch OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

# Log the API key status
if not api_key:
    logging.error("Missing OpenAI API Key. Set it in a .env file.")
    raise RuntimeError("Missing OpenAI API Key. Set it in a .env file.")
else:
    logging.info("OpenAI API Key successfully loaded.")

client = OpenAI(
  api_key=api_key,
)

def generate_follow_up_questions(symptoms):
    prompt = f"Given the symptoms {', '.join(symptoms)}, suggest 3 medical follow-up questions."
    logging.debug(f"Generated prompt: {prompt}")  # Log the generated prompt

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use ChatCompletion instead of Completion
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": "Given the symptoms fever, cough, suggest 3 medical follow-up questions."}
            ],
            max_tokens=50
        )

        logging.debug(f"OpenAI Response: {completion}")  # Log the raw response
        
        questions = completion.choices[0].message.content.strip().split("\n")
        logging.info(f"Generated follow-up questions: {questions}")  # Log extracted questions
        return questions

    except Exception as e:
        logging.error(f"Error occurred while generating follow-up questions: {e}")
        return ["Do you have a fever?", "Are you experiencing fatigue?", "Is there any swelling?"]
