import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def healthy(port):
    try:
        with urllib.request.urlopen(f"http://localhost:{port}/health", timeout=2):
            return True
    except OSError:
        return False

class ModelServer:
    def __init__(self, model, port, timeout, log_level):
        self.model = model
        self.port = int(port)
        self.timeout = int(timeout)
        self.log_level = log_level
        self.process = None

    @property
    def v1_url(self):
        return f"http://localhost:{self.port}/v1"

    def start(self):
        if healthy(self.port):
            return self

        self.process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "transformers.cli.transformers",
                "serve",
                self.model,
                "--port",
                str(self.port),
                "--log-level",
                self.log_level,
            ],
            cwd=ROOT,
        )

        deadline = time.monotonic() + self.timeout
        while not healthy(self.port):
            if self.process.poll() is not None or time.monotonic() > deadline:
                self.stop()
                raise RuntimeError(f"Model server failed to start on port {self.port}")
            time.sleep(1)
        return self

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self.process.kill()

    def __enter__(self):
        return self.start()

    def __exit__(self, *_):
        self.stop()


if __name__ == "__main__":
    from config import LOG_LEVEL, MODEL, PORT, TIMEOUT

    with ModelServer(MODEL, PORT, TIMEOUT, LOG_LEVEL):
        input("Press Enter to stop the model server")
