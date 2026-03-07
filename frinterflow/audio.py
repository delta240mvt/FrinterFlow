# frinterflow/audio.py
"""
Thread-safe audio capture using sounddevice.
Records into a numpy buffer while a threading.Event is set.
Posts wav file path to result_queue when recording stops.
"""
import threading
import queue
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os

from frinterflow.config import AUDIO_SAMPLE_RATE, AUDIO_CHANNELS


class AudioRecorder:
    def __init__(self, result_queue: queue.Queue):
        """
        result_queue: receives wav file paths (str) when recording stops.
        The caller is responsible for deleting the temp file after use.
        """
        self.result_queue = result_queue
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self):
        """Begin recording in a daemon thread. No-op if already recording."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Signal recording to stop. Result posted to result_queue."""
        self._stop_event.set()

    def _record_loop(self):
        chunks = []
        try:
            with sd.InputStream(
                samplerate=AUDIO_SAMPLE_RATE,
                channels=AUDIO_CHANNELS,
                dtype="float32",
            ) as stream:
                while not self._stop_event.is_set():
                    data, _ = stream.read(1024)
                    chunks.append(data.copy())
        except Exception:
            return

        if not chunks:
            return

        audio = np.concatenate(chunks, axis=0)
        audio_int16 = (audio * 32767).astype(np.int16)

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(tmp.name, AUDIO_SAMPLE_RATE, audio_int16)
        tmp.close()
        self.result_queue.put(tmp.name)
