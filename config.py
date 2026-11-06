import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Global configuration variables
STANDARD_USERNAME = os.environ["STANDARD_USERNAME"]
VALID_PASSWORD = os.environ["VALID_PASSWORD"]

LOCKED_OUT_USERNAME = os.environ["LOCKED_OUT_USERNAME"]
PROBLEM_USERNAME = os.environ["PROBLEM_USERNAME"]

INVALID_USERNAME = os.environ["INVALID_USERNAME"]
INVALID_PASSWORD = os.environ["INVALID_PASSWORD"]
PERFORMANCE_GLITCH_USERNAME = os.environ["PERFORMANCE_GLITCH_USERNAME"]
ERROR_USER = os.environ["ERROR_USER"]
VISUAL_USER = os.environ["VISUAL_USER"]

#demoblaze credentials
DB_USERNAME1 = os.environ["DB_USERNAME1"]
DB_PASSWORD1 = os.environ["DB_PASSWORD1"]
DB_USERNAME2 = os.environ["DB_USERNAME2"]
DB_PASSWORD2 = os.environ["DB_PASSWORD2"]

#URLs
SAUCEDEMO_URL=os.environ["SAUCEDEMO_URL"]
DEMOBLAZE_URL=os.environ["DEMOBLAZE_URL"]
