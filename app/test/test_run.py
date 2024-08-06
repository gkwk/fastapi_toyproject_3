from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

from test.main_test.scripts import TestMain
from test.user_test.scripts import TestUser
from test.auth_test.scripts import TestAuth
from test.board_test.scripts import TestBoard
from test.post_test.scripts import TestPost
from test.comment_test.scripts import TestComment
# from test.ai_test.scripts import TestAI
