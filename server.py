import sys
import os
import time
import io
import threading
import logging
import contextlib
from xmlrpc.server import SimpleXMLRPCServer

g_globals = {}
g_globals_lock = threading.RLock()


def eval_code(py_code: str) -> str:
    g_globals_lock.acquire()
    global g_globals
    try:
        logging.info("client request, eval code")
        lines = py_code.split("\n")
        for i, line in enumerate(lines):
            logging.info("%2d %s", i, line)
        with contextlib.redirect_stdout(io.StringIO()) as f:  # TODO: redirect_stderr
            exec(py_code, g_globals, g_globals)
        output = f.getvalue()
        logging.info(output)
        return output
    finally:
        g_globals_lock.release()


def eval_file(py_file: str) -> str:
    with open(py_file) as f:
        return eval_code(f.read())


def run_server(init_script_file):
    if init_script_file is not None and os.path.exists(init_script_file):
        eval_file(init_script_file)
    server = SimpleXMLRPCServer(("0.0.0.0", 50052))
    print('SEIDA_SERVER_ADDR = "http://%s:%d"' % (server.server_address[0], server.server_address[1]))
    server.register_function(eval_code, "eval")
    server.serve_forever()


def loop():
    line = input("> ")
    while True:
        if line == "exit()":
            break
        if line.startswith("load "):
            filename = line[4:]
            if os.path.exists(filename):
                print(eval_file(filename))
        else:
            print(eval_code(str(line)))
        line = input()


def main():
    init_script_file = sys.argv[1] if len(sys.argv) > 1 else None
    server = threading.Thread(target=run_server, args=(init_script_file,))
    server.start()
    time.sleep(1)
    loop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
