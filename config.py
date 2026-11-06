import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

#demoblaze credentials
DB_USERNAME1 = os.environ["DB_USERNAME1"]
DB_PASSWORD1 = os.environ["DB_PASSWORD1"]
DB_USERNAME2 = os.environ["DB_USERNAME2"]
DB_PASSWORD2 = os.environ["DB_PASSWORD2"]

#URLs
SAUCEDEMO_URL=os.environ["SAUCEDEMO_URL"]
DEMOBLAZE_URL=os.environ["DEMOBLAZE_URL"]
