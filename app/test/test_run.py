from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

from test.main_test.scripts import TestMain
from test.user_test.scripts import TestUser