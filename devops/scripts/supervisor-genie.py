import os
import socket
import sys
from threading import Thread

HOSTNAME = socket.gethostname()
ENVIRON = os.environ["ENVIRONMENT"]
APP_NAME = os.environ["SERVICE"]


def write_stdout(s):
    # only eventlistener protocol messages may be sent to stdout
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def alarming_mode(headers):
    pass


def main():
    while 1:
        # transition from ACKNOWLEDGED to READY
        write_stdout('READY\n')

        # read header line and print it to stderr
        line = sys.stdin.readline()
        write_stderr(line)

        # read event payload and print it to stderr
        headers = dict([x.split(':') for x in line.split()])
        data = sys.stdin.read(int(headers['len']))
        write_stderr(data)

        data_dict = dict([x.split(':') for x in data.split()])
        headers.update(data_dict)
        headers["hostname"] = HOSTNAME
        headers["environment"] = ENVIRON

        process_state_handlers = {
            "PROCESS_STATE_FATAL": alarming_mode,
            "PROCESS_STATE_BACKOFF": None,
            "PROCESS_STATE_EXITED": None,
            "PROCESS_STATE_RUNNING": None

        }

        if ENVIRON == "production":
            handler = process_state_handlers.get(headers["eventname"])
            if handler:
                thread = Thread(target=alarming_mode, args=[headers])
                thread.name = "supervisor-genie"
                thread.start()

            else:
                pass
        # transition from READY to ACKNOWLEDGED
        write_stdout('RESULT 2\nOK')


if __name__ == '__main__':
    main()
