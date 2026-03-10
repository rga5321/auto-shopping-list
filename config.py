import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

class AppConfig:
    def __init__(self):
        """Initializes configuration by loading environment variables and validating them."""
        # Execution mode
        self.mode = os.getenv("EXECUTION_MODE", "simulation").lower()
        if self.mode not in ["simulation", "real"]:
            raise ValueError("EXECUTION_MODE must be either 'simulation' or 'real'")

        # Keep Configuration
        self.keep_email = self._get_required_env("KEEP_EMAIL")
        self.keep_token = self._get_required_env("KEEP_TOKEN")
        self.keep_note_id = self._get_required_env("KEEP_NOTE_ID")

        # Todoist Configuration
        self.todoist_api_key = self._get_required_env("TODOIST_API_KEY")
        self.todoist_project_id = self._get_required_env("TODOIST_PROJECT_ID")

        # Gemini Configuration
        self.gemini_api_key = self._get_required_env("GEMINI_API_KEY")

    @staticmethod
    def _get_required_env(key: str) -> str:
        """Helper to get required environment variables."""
        value = os.getenv(key)
        if value is None or value.strip() == "":
            raise ValueError(f"Missing required environment variable: {key}")
        return value

# Instead of instantiating directly, we can define a singleton getter config
# if desired, or let the main entry point initialize this class.
