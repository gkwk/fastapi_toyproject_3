import sys
from pathlib import Path

from dotenv import load_dotenv
import uvicorn
import redis
from redis.exceptions import ConnectionError

from terminal_command.create_super_user import create_admin_with_terminal


def initialize_redis():
    try:
        redis_client = redis.Redis(
            host="localhost", port=6379, db=0, socket_connect_timeout=5
        )
        redis_client.ping()
        print("Initializing Redis...")
        redis_client.flushall()
        print("Redis initialized successfully.")
    except ConnectionError:
        print("Redis is not running.")
    except Exception as e:
        print(e)
    finally:
        redis_client.close()


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) == 0:
        initialize_redis()
        load_dotenv(Path(__file__).resolve().parent.parent / ".env")

        uvicorn.run("main:app", reload=True, log_level="debug", port=8080)
    else:
        if "createsuperuser" in argv:
            create_admin_with_terminal(data_base=None)
