# frinterflow/hotkeys.py
"""
Toggle-to-talk listener using pynput.
First press of LCTRL+SHIFT = start recording.
Second press of LCTRL+SHIFT = stop recording.
Runs in its own daemon thread (pynput creates this automatically).
"""
from pynput import keyboard

from frinterflow.config import HOTKEY_TRIGGER


class PushToTalkListener:
    def __init__(self, on_start, on_stop):
        """
        on_start: callable() — called on first LCTRL+SHIFT press (recording starts)
        on_stop:  callable() — called on second LCTRL+SHIFT press (recording stops)
        """
        self.on_start = on_start
        self.on_stop = on_stop
        self._held: set = set()
        self._recording: bool = False
        self._combo_fired: bool = False  # prevents repeat-fire while holding
        self._listener: keyboard.Listener | None = None

    def start(self):
        """Start the background listener thread."""
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
        """Stop the listener thread."""
        if self._listener:
            self._listener.stop()

    def _on_press(self, key):
        self._held.add(self._norm(key))
        if HOTKEY_TRIGGER.issubset(self._held) and not self._combo_fired:
            self._combo_fired = True
            if not self._recording:
                self._recording = True
                self.on_start()
            else:
                self._recording = False
                self.on_stop()

    def _on_release(self, key):
        k = self._norm(key)
        self._held.discard(k)
        if k in HOTKEY_TRIGGER:
            self._combo_fired = False  # allow next press to fire again

    @staticmethod
    def _norm(key) -> str:
        try:
            return f"Key.{key.name}"
        except AttributeError:
            return str(key)
