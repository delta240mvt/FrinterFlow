import os
import queue

import pytest


def test_transcriber_imports():
    from frinterflow.transcriber import Transcriber
    assert Transcriber is not None


def test_transcriber_instantiation():
    from frinterflow.transcriber import Transcriber
    q = queue.Queue()
    t = Transcriber(result_queue=q)
    assert t._model is None  # not loaded yet


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="Model download too large for CI",
)
def test_model_loads_without_error():
    from frinterflow.transcriber import Transcriber
    q = queue.Queue()
    t = Transcriber(result_queue=q)
    t.load_model()
    assert t._model is not None
