import os


# Base directory of the project.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Asset Configuration.
ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")
LOGO_PATH = os.path.join(ASSETS_FOLDER, "icon.png")

# Chat History Configuration.
HISTORY_DIR = os.path.join(BASE_DIR, "sessions")

# Database Configuration.
DATA_FOLDER = os.path.join(BASE_DIR, "data")
DB_NAME = "agent.db"
DB_PATH = os.path.join(DATA_FOLDER, DB_NAME)
DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# App Settings.
APP_TITLE = "KaggleN"
APP_ICON = LOGO_PATH
MODEL_NAME = "gemini-2.5-flash-lite"
