"""
One-Click Launcher for DeepDTA Web Platform
Automatically opens default browser and starts the Uvicorn FastAPI server.
"""

import sys
import os
import subprocess
import webbrowser
import time

PYTHON313_EXE = r"C:\Users\Rishitha\AppData\Local\Programs\Python\Python313\python.exe"


def main():
    # If currently running on Python without TensorFlow/Uvicorn, delegate to Python 3.13
    current_exe = sys.executable
    target_exe = current_exe
    try:
        import uvicorn
        import fastapi
        import tensorflow
    except ImportError:
        if os.path.exists(PYTHON313_EXE):
            target_exe = PYTHON313_EXE
        else:
            print("[!] Error: Required packages not found and Python 3.13 not at expected path.")
            sys.exit(1)

    print("=" * 70)
    print("       STARTING DEEPDTA INTERACTIVE WEB PLATFORM")
    print("=" * 70)
    print(f"[*] Python Runtime : {target_exe}")
    print("[*] Server Address : http://127.0.0.1:8000")
    print("[*] Opening web browser automatically in 2 seconds...")

    # Open web browser after a short delay
    def open_browser():
        time.sleep(1.8)
        webbrowser.open("http://127.0.0.1:8000")

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    # Launch server
    if target_exe != current_exe:
        subprocess.run([target_exe, "-m", "uvicorn", "web.app:app", "--host", "127.0.0.1", "--port", "8000"])
    else:
        import uvicorn
        uvicorn.run("web.app:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()

