import os
import shutil
import subprocess
import threading


def narrate_async(text):
    if not text:
        return

    thread = threading.Thread(target=_narrate, args=(text,), daemon=True)
    thread.start()


def _narrate(text):
    try:
        if os.name == "nt":
            _speak_windows(text)
        elif shutil.which("say"):
            subprocess.run(["say", text], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Narration should never crash the UI flow.
        return


def _speak_windows(text):
    escaped = text.replace("'", "''")
    script = (
        "$voice = New-Object -ComObject SAPI.SpVoice;"
        "$voice.Rate = -1;"
        f"$voice.Speak('{escaped}') | Out-Null"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
