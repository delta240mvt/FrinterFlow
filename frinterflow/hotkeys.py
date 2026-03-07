# frinterflow/hotkeys.py
"""
Global push-to-talk listener using pynput.
Triggers callbacks when BOTH Left CTRL and SHIFT are held simultaneously.
Runs in its own daemon thread (pynput creates this automatically).
"""
from pynput import keyboard

from frinterflow.config import HOTKEY_TRIGGER


class PushToTalkListener:
    def __init__(self, on_start, on_stop):
        """
        on_start: callable() — called when trigger combo is first pressed
        on_stop:  callable() — called when either trigger key is released
        """
        self.on_start = on_start
        self.on_stop = on_stop
        self._held: set = set()
        self._active: bool = False
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
        if HOTKEY_TRIGGER.issubset(self._held) and not self._active:
            self._active = True
            self.on_start()

    def _on_release(self, key):
        k = self._norm(key)
        self._held.discard(k)
        if k in HOTKEY_TRIGGER and self._active:
            self._active = False
            self.on_stop()

    @staticmethod
    def _norm(key) -> str:
        try:
            return f"Key.{key.name}"
        except AttributeError:
            return str(key)
