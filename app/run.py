import sys
import uvicorn

from terminal_command.create_super_user import create_admin_with_terminal


if __name__ == "__main__":
    argv = sys.argv[1:]

    if len(argv) == 0:
        uvicorn.run("main:app", reload=True, log_level="debug", port=8080)
    else:
        if "createsuperuser" in argv:
            create_admin_with_terminal(data_base=None)
