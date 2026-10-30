import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent

load_dotenv(ROOT / ".env")

def healthy(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, OSError):
        return False


def resolve(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(
            f"{name} not found on PATH. Run this via: uv run python main.py"
        )
    return path
def start(model: str, port: int, timeout: int, log_level: str) -> None:
    health_url = f"http://localhost:{port}/health"
    server = None

    def shutdown(*_) -> None:
        if server is None or server.poll() is not None:
            return
        print(f"Stopping model server (pid {server.pid})")
        try:
            if os.name == "posix":
                os.killpg(os.getpgid(server.pid), signal.SIGTERM)
            else:
                server.terminate()
        except (ProcessLookupError, PermissionError):
            pass
        try:
            server.wait(timeout=30)
        except subprocess.TimeoutExpired:
            if os.name == "posix":
                os.killpg(os.getpgid(server.pid), signal.SIGKILL)
            else:
                server.kill()

    try:
        print(f"Starting model server for {model} on port {port}")
        server = subprocess.Popen(
            [
                resolve("transformers"), "serve", model,
                "--port", str(port), "--log-level", log_level,
            ],
            cwd=ROOT,
            start_new_session=(os.name == "posix"),
        )
        signal.signal(signal.SIGTERM, shutdown)

        deadline = time.monotonic() + int(timeout)
        elapsed = 0
        while not healthy(health_url):
            if server.poll() is not None:
                print(
                    f"Model server exited with code {server.returncode} before becoming ready.",
                )
                sys.exit(1)
            if time.monotonic() > deadline:
                print(f"Timed out after {timeout}s waiting for {health_url}")
                sys.exit(1)
            if elapsed % 15 == 0:
                print(f"loading model... {elapsed}s")
            time.sleep(1)
            elapsed += 1
        print("Model ready.")
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    start()
