import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # MUST be first — PyInstaller/OpenMP fix

import sys
import queue
import threading

from frinterflow.audio import AudioRecorder
from frinterflow.transcriber import Transcriber
from frinterflow.hotkeys import PushToTalkListener
from frinterflow.logger import append_entry
from frinterflow.overlay import FrinterOverlay


def _print(text=""):
    """Print to terminal, safely ignoring unencodable characters."""
    print(text, flush=True)

try:
    import winsound
    def beep():
        winsound.Beep(1000, 150)
except ImportError:
    def beep():
        print("\a", end="", flush=True)


def run():
    """
    FrinterFlow entry point.

    Threading model:
      main thread      → tkinter overlay mainloop (FrinterOverlay.run())
      audio thread     → sounddevice capture (daemon)
      transcribe thread→ faster-whisper inference (daemon)
      pynput thread    → keyboard listener (daemon, auto-created by pynput)
      fanout thread    → routes raw_q → tui_q + log_q
      log thread       → writes to file + plays beep

    Queues:
      audio_q  : AudioRecorder  → audio_watcher (wav paths)
      raw_q    : Transcriber    → fanout_dispatcher (transcribed text)
      tui_q    : fanout         → FrinterOverlay._poll_queue
      log_q    : fanout         → log_worker
    """
    audio_q = queue.Queue()
    raw_q   = queue.Queue()
    tui_q   = queue.Queue()
    log_q   = queue.Queue()

    transcriber = Transcriber(result_queue=raw_q)
    recorder    = AudioRecorder(result_queue=audio_q)
    overlay     = FrinterOverlay(transcript_queue=tui_q)

    # --- Load Whisper model (blocking, show terminal progress) ---
    _print()
    _print("-" * 50)
    _print("  FRINTER FLOW v1.0")
    _print("-" * 50)
    _print(f"  Model:      {transcriber.model_size} (faster-whisper)")
    _print("  Jezyk:      polski")
    _print("  Urzadzenie: CPU / int8")
    _print("-" * 50)
    _print("  Ladowanie modelu Whisper...")
    _print("  (pierwsze uruchomienie: pobieranie ~500 MB, 30-60 sek)")
    _print()

    transcriber.load_model()

    _print("  [OK] Model zaladowany.")
    _print("  Overlay uruchomiony - mozesz zminimalizowac terminal.")
    _print("  Trzymaj LEWY CTRL + SHIFT zeby mowic.")
    _print()

    # --- Fanout dispatcher: raw_q → tui_q + log_q ---
    def fanout():
        while True:
            text = raw_q.get()
            tui_q.put(text)
            log_q.put(text)

    # --- Log worker: log_q → file + beep ---
    def log_worker():
        while True:
            text = log_q.get()
            append_entry(text)
            beep()

    # --- Audio watcher: audio_q → transcriber ---
    def audio_watcher():
        while True:
            wav_path = audio_q.get()
            _print(f"[DEBUG] WAV gotowy: {wav_path}")
            overlay.set_status("PROCESSING")
            transcriber.transcribe_async(wav_path, on_done=lambda: overlay.set_status("IDLE"))

    for fn in (fanout, log_worker, audio_watcher):
        threading.Thread(target=fn, daemon=True).start()

    # --- Hotkey callbacks ---
    def on_start():
        overlay.set_status("LISTENING")
        recorder.start()

    def on_stop():
        recorder.stop()
        overlay.set_status("PROCESSING")

    hotkeys = PushToTalkListener(on_start=on_start, on_stop=on_stop)
    hotkeys.start()

    # --- Block on tkinter mainloop ---
    overlay.run()
    os._exit(0)


if __name__ == "__main__":
    run()
