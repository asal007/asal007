import os
import sys
import time
import webbrowser
import socket
import urllib.request
import threading
from pathlib import Path


def base_dir() -> Path:
    # Wenn per PyInstaller gebaut, liegen Assets unter _MEIPASS
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))


def resource_path(rel: str) -> Path:
    return base_dir() / rel


def wait_for_server(port: int, timeout: float = 60.0) -> bool:
    start = time.time()
    health_urls = [
        f"http://localhost:{port}/_stcore/health",
        f"http://127.0.0.1:{port}/_stcore/health",
        f"http://localhost:{port}/",
    ]
    while time.time() - start < timeout:
        # HTTP check
        for url in health_urls:
            try:
                with urllib.request.urlopen(url, timeout=1) as _:
                    return True
            except Exception:
                pass
        # Socket check
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def _open_browser_when_ready(port: int):
    if wait_for_server(port):
        try:
            webbrowser.open(f"http://localhost:{port}/")
        except Exception:
            pass


def run_streamlit(app: Path, port: int = 8502):
    """Starte Streamlit programmgesteuert; fallback via subprocess.

    - Öffnet automatisch den Browser auf localhost:port.
    - Nutzt die gebündelten Projektdateien (app.py, pages, .streamlit usw.).
    """
    try:
        # Arbeitsverzeichnis auf das gebündelte Projekt setzen
        os.chdir(str(base_dir()))
        # Programmgesteuerter Start (robuster als reiner subprocess)
        from streamlit.web.cli import main as st_main
        sys.argv = [
            "streamlit",
            "run",
            str(app),
            f"--server.port={port}",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ]
        threading.Thread(target=_open_browser_when_ready, args=(port,), daemon=True).start()
        # Streamlit starten
        st_main()
    except Exception:
        # Fallback: subprocess mit dem eingebetteten Python
        python = sys.executable
        cmd = [
            python,
            "-m",
            "streamlit",
            "run",
            str(app),
            f"--server.port={port}",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ]
        os.chdir(str(base_dir()))
        try:
            import subprocess

            subprocess.Popen(cmd)
            # Auf Serververfügbarkeit warten
            if wait_for_server(port):
                webbrowser.open(f"http://localhost:{port}/")
        except Exception as e:
            print("Fehler beim Starten der App:", e)


def main():
    app = resource_path("app.py")
    if not app.exists():
        print("app.py nicht gefunden.")
        sys.exit(1)
    run_streamlit(app)


if __name__ == "__main__":
    main()