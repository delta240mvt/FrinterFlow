# frinterflow/overlay.py
"""
Always-on-top floating tkinter overlay.

Layout:
  - Frameless (overrideredirect)
  - Semi-transparent (-alpha)
  - Bottom-center of screen (-topmost)
  - Left panel:  Frint_bot pixel art on Canvas (animated sine bobbing)
  - Right panel: tk.Text with timestamped transcript entries
  - Bottom bar:  status label + [X] close button

Thread safety:
  ALL tkinter calls from background threads MUST go through root.after(0, fn).
  Never call widget methods directly from non-main threads.
"""
import os
import math
import time
import queue
import tkinter as tk
from datetime import datetime

from frinterflow.sprites import SPRITES, draw_sprite_on_canvas
from frinterflow.config import (
    COLOR_BLOOM, COLOR_RELATION, COLOR_FOCUS,
    COLOR_BG, COLOR_DIM, COLOR_TEXT,
    OVERLAY_PIXEL_SIZE, OVERLAY_WIDTH, OVERLAY_HEIGHT,
    OVERLAY_ALPHA, OVERLAY_MARGIN_BOTTOM,
    OVERLAY_FONT, OVERLAY_FONT_TS,
    ANIMATION_FPS, BOT_BOB_SPEED,
)


class FrinterOverlay:

    def __init__(self, transcript_queue: queue.Queue):
        self.transcript_queue = transcript_queue
        self.root = tk.Tk()
        self._drag_x = 0
        self._drag_y = 0
        self._status = "IDLE"
        self._setup_window()
        self._setup_statusbar()   # BOTTOM must be packed first
        self._setup_bot_canvas()
        self._setup_transcript()
        self._show_welcome()

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _setup_window(self):
        r = self.root
        r.title("FrinterFlow")
        r.overrideredirect(True)        # No title bar / frame
        r.attributes("-topmost", True)  # Always on top
        r.attributes("-alpha", OVERLAY_ALPHA)
        r.configure(bg=COLOR_BG)

        # Position: bottom-center of screen
        sw = r.winfo_screenwidth()
        sh = r.winfo_screenheight()
        x = (sw - OVERLAY_WIDTH) // 2
        y = sh - OVERLAY_HEIGHT - OVERLAY_MARGIN_BOTTOM
        r.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{x}+{y}")
        r.resizable(False, False)

        # Dragging
        r.bind("<ButtonPress-1>", self._on_drag_start)
        r.bind("<B1-Motion>", self._on_drag_motion)

        # Escape to close
        r.bind("<Escape>", lambda _: os._exit(0))

    def _on_drag_start(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag_motion(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    # ------------------------------------------------------------------
    # Bot canvas (left panel)
    # ------------------------------------------------------------------

    def _setup_bot_canvas(self):
        ps = OVERLAY_PIXEL_SIZE
        sprite = SPRITES["bot"]
        cols = len(sprite[0])
        rows = len(sprite)
        # Extra height for bob animation headroom
        canvas_w = cols * ps
        canvas_h = rows * ps + 4

        self.bot_canvas = tk.Canvas(
            self.root,
            width=canvas_w,
            height=canvas_h,
            bg=COLOR_BG,
            highlightthickness=0,
        )
        self.bot_canvas.pack(side=tk.LEFT, padx=(10, 4), pady=6)

    # ------------------------------------------------------------------
    # Transcript text (right panel)
    # ------------------------------------------------------------------

    def _setup_transcript(self):
        right = tk.Frame(self.root, bg=COLOR_BG)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8), pady=(6, 0))

        self.text_widget = tk.Text(
            right,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=OVERLAY_FONT,
            wrap=tk.WORD,
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0,
            cursor="arrow",
        )
        self.text_widget.tag_configure("ts",        foreground=COLOR_BLOOM)
        self.text_widget.tag_configure("listening", foreground=COLOR_FOCUS)
        self.text_widget.tag_configure("text",      foreground=COLOR_TEXT)
        self.text_widget.tag_configure("dim",       foreground="#5a5a7c")
        self.text_widget.pack(fill=tk.BOTH, expand=True)

    def _show_welcome(self):
        self._append("Frinter Flow v1.0 — ", tag="ts")
        self._append("LCTRL+SHIFT = start/stop nagrywania.\n", tag="dim")

    def _append(self, text: str, tag: str = "text"):
        """Must be called from main thread only."""
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, text, tag)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Status bar (bottom strip)
    # ------------------------------------------------------------------

    def _setup_statusbar(self):
        self.status_var = tk.StringVar(value=self._idle_text())
        bar = tk.Frame(self.root, bg=COLOR_DIM)
        bar.pack(side=tk.BOTTOM, fill=tk.X)

        status_lbl = tk.Label(
            bar,
            textvariable=self.status_var,
            bg=COLOR_DIM,
            fg=COLOR_BLOOM,
            font=("Consolas", 9),
            anchor="w",
            padx=8,
            pady=2,
        )
        status_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        close_btn = tk.Label(
            bar,
            text=" X ZAMKNIJ ",
            bg=COLOR_RELATION,
            fg="#ffffff",
            font=("Consolas", 9, "bold"),
            cursor="hand2",
            padx=6,
            pady=3,
        )
        close_btn.pack(side=tk.RIGHT, padx=4, pady=2)
        close_btn.bind("<Button-1>", lambda _: os._exit(0))

        mic_btn = tk.Label(
            bar,
            text=" MIC TEST ",
            bg=COLOR_BLOOM,
            fg="#ffffff",
            font=("Consolas", 9, "bold"),
            cursor="hand2",
            padx=6,
            pady=3,
        )
        mic_btn.pack(side=tk.RIGHT, padx=(0, 2), pady=2)
        mic_btn.bind("<Button-1>", lambda _: self._test_mic())

    def _idle_text(self) -> str:
        return "  GOTOWY  |  LCTRL+SHIFT = start/stop"

    def _test_mic(self):
        """Record 2 seconds and show RMS volume level in transcript."""
        import threading
        import numpy as np
        try:
            import sounddevice as sd
        except ImportError:
            self.root.after(0, self._append, "[MIC TEST] sounddevice nie zainstalowany\n", "dim")
            return

        def _run():
            try:
                self.root.after(0, self.status_var.set, "  Nagrywam 2 sek testu...")
                data = sd.rec(int(2 * 44100), samplerate=44100, channels=1,
                              dtype="float32", blocking=True)
                rms = float(np.sqrt(np.mean(data ** 2)))
                bars = int(rms * 500)
                bar_str = "#" * min(bars, 20)
                level = "CICHO" if rms < 0.01 else ("OK" if rms < 0.1 else "GLOSNO")
                msg = f"[MIC TEST] RMS={rms:.4f} [{bar_str:<20}] {level}\n"
                self.root.after(0, self._append, msg, "ts" if level == "OK" else "dim")
                self.root.after(0, self.status_var.set, self._idle_text())
            except Exception as e:
                self.root.after(0, self._append, f"[MIC ERROR] {e}\n", "dim")
                self.root.after(0, self.status_var.set, self._idle_text())

        threading.Thread(target=_run, daemon=True).start()

    # ------------------------------------------------------------------
    # Thread-safe public API (safe to call from ANY thread)
    # ------------------------------------------------------------------

    def set_status(self, status: str):
        """Thread-safe status update."""
        self.root.after(0, self._set_status_main, status)

    def add_transcript(self, text: str):
        """Thread-safe transcript insertion."""
        self.root.after(0, self._add_transcript_main, text)

    # ------------------------------------------------------------------
    # Main-thread state handlers
    # ------------------------------------------------------------------

    def _set_status_main(self, status: str):
        self._status = status
        if status == "LISTENING":
            self.status_var.set("  SLUCHAM...  |  Hold CTRL+SHIFT")
            self._append("\n", "text")
            self._append("[SLUCHAM] ", "listening")
        elif status == "PROCESSING":
            self.status_var.set("  TRANSKRYBUJE...  ")
        else:
            self.status_var.set(self._idle_text())

    def _add_transcript_main(self, text: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self._append(f"\n[{ts}] ", "ts")
        self._append(text, "text")
        self._set_status_main("IDLE")

    # ------------------------------------------------------------------
    # Animation loop (main thread via root.after)
    # ------------------------------------------------------------------

    def _animate(self):
        t = time.time()
        bob = int((math.sin(t * (2 * math.pi / BOT_BOB_SPEED)) + 1))
        self.bot_canvas.delete("all")
        draw_sprite_on_canvas(self.bot_canvas, "bot", OVERLAY_PIXEL_SIZE, bob_offset=bob)
        self.root.after(int(1000 / ANIMATION_FPS), self._animate)

    # ------------------------------------------------------------------
    # Queue poller (main thread via root.after)
    # ------------------------------------------------------------------

    def _poll_queue(self):
        try:
            while True:
                text = self.transcript_queue.get_nowait()
                self._add_transcript_main(text)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    # ------------------------------------------------------------------
    # Run (blocking — call from main thread only)
    # ------------------------------------------------------------------

    def run(self):
        """Start animation, queue polling, and tkinter mainloop."""
        self._animate()
        self._poll_queue()
        self.root.mainloop()
