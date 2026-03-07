import os
import queue
import time

import pytest


def test_audio_recorder_imports():
    from frinterflow.audio import AudioRecorder
    assert AudioRecorder is not None


def test_audio_recorder_instantiation():
    from frinterflow.audio import AudioRecorder
    q = queue.Queue()
    rec = AudioRecorder(result_queue=q)
    assert rec is not None
    assert rec.result_queue is q


def test_audio_recorder_stop_before_start():
    """Stopping before starting should not raise."""
    from frinterflow.audio import AudioRecorder
    q = queue.Queue()
    rec = AudioRecorder(result_queue=q)
    rec.stop()  # should not raise


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="No audio device in CI environment",
)
def test_record_and_stop_produces_wav():
    from frinterflow.audio import AudioRecorder
    q = queue.Queue()
    rec = AudioRecorder(result_queue=q)
    rec.start()
    time.sleep(0.4)
    rec.stop()
    time.sleep(0.6)

    if not q.empty():
        path = q.get()
        assert os.path.exists(path)
        assert path.endswith(".wav")
        os.unlink(path)
