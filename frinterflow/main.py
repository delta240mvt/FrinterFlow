import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # MUST be first — PyInstaller/OpenMP fix

import queue
import threading

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from frinterflow.audio import AudioRecorder
from frinterflow.transcriber import Transcriber
from frinterflow.hotkeys import PushToTalkListener
from frinterflow.logger import append_entry
from frinterflow.overlay import FrinterOverlay

console = Console()

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
    console.print(
        "\n[bold #4a8d83]FrinterFlow v1.0[/] — [dim]loading Whisper model...[/]"
    )
    with Progress(
        SpinnerColumn(),
        TextColumn("[#d6b779]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Loading model...", total=None)
        transcriber.load_model()
        progress.update(task, description="Model ready!")

    console.print("[bold #4a8d83]Model loaded.[/] Overlay launched.")
    console.print("[dim]You can minimize this terminal.[/]\n")

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
            overlay.set_status("PROCESSING")
            transcriber.transcribe_async(wav_path)

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
