import os
from dotenv import load_dotenv

class EnvLoader:
    @staticmethod
    def load_api_key():
        load_dotenv()
        try:
            api_key = os.getenv("GROQ_API_KEY")
            return api_key
        except KeyError as e:
            raise RuntimeError(f"Failed to load GROQ API key: {e}")