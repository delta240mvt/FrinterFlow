# frinterflow/transcriber.py
"""
Wraps faster-whisper for local speech transcription.
Model is loaded ONCE at startup (expensive — ~2-10s depending on size).
Transcription runs in a daemon thread and posts results to result_queue.
"""
import os
import time
import threading
import queue

from faster_whisper import WhisperModel

from frinterflow.config import (
    WHISPER_MODEL_SIZE,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE,
    WHISPER_LANGUAGE,
    WHISPER_BEAM_SIZE,
)


class Transcriber:
    def __init__(self, result_queue: queue.Queue):
        """
        result_queue: receives transcribed text strings (str).
        Empty recordings produce no queue item.
        """
        self.result_queue = result_queue
        self.model_size = WHISPER_MODEL_SIZE
        self._model: WhisperModel | None = None
        self._lock = threading.Lock()

    def load_model(self):
        """
        Blocking. Call once during startup before launching overlay.
        Downloads model on first run (~500 MB for 'small').
        """
        self._model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE,
        )

    def transcribe_async(self, wav_path: str, on_done=None):
        """
        Launch transcription in a daemon thread.
        Posts result string to result_queue. Deletes wav_path when done.
        on_done(): optional callback called when transcription finishes (even if empty).
        """
        t = threading.Thread(target=self._run, args=(wav_path, on_done), daemon=True)
        t.start()

    def _run(self, wav_path: str, on_done=None):
        with self._lock:  # prevent concurrent transcriptions
            try:
                t0 = time.time()
                segments, _ = self._model.transcribe(
                    wav_path,
                    language=WHISPER_LANGUAGE,
                    beam_size=WHISPER_BEAM_SIZE,
                    vad_filter=True,
                )
                text = " ".join(s.text.strip() for s in segments).strip()
                elapsed = time.time() - t0
                print(f"[DEBUG] Transkrypcja ({elapsed:.1f}s): '{text}'", flush=True)
                if text:
                    self.result_queue.put(text)
                else:
                    print("[DEBUG] Pusty wynik — cicho lub brak mowy", flush=True)
            except Exception as e:
                print(f"[TRANSCRIBE ERROR] {e}", flush=True)
            finally:
                if on_done:
                    on_done()
                try:
                    os.unlink(wav_path)
                except OSError:
                    pass
