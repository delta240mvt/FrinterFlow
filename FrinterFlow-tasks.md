# FrinterFlow — Agent Task Specification
**Version:** 2.0.0
**Status:** Open Source Build Brief
**Target Agents:** Cursor, Claude Code, Open Interpreter, or any autonomous coding agent
**Platform:** Windows 10/11 (primary), Linux/macOS (secondary)

---

## 0. Read This First — Agent Instructions

You are an expert Python developer. Your task is to build **FrinterFlow** in its entirety.
Read every section before writing any code. The architecture relies on careful threading — mistakes here cause silent freezes or crashes.

### CRITICAL Architecture Decision

> **Frint_bot is NOT in the terminal.**

The floating overlay (tkinter) is the **primary UI**. It appears as a frameless, semi-transparent, always-on-top widget at the **bottom of the screen**. The terminal is used only for startup messages and model loading progress — after that, the user can minimize/close the terminal entirely.

```
SCREEN (full desktop)
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│     [user's browser / other apps — full focus]                     │
│                                                                     │
│                                                                     │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  [FRINT_BOT]   [14:32:01] Dzisiaj omawiam strukturę...       │  │
│  │  pixel art     [14:32:45] Kolejny punkt to wdrożenie modelu. │  │
│  │  (animated)    [14:33:10] SLUCHAM...                         │  │
│  │  ────────────────────────────────────────────────────────────│  │
│  │  GOTOWY  |  Log: ~/frinterflow_log.txt          [X] zamknij  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                    ↑ ALWAYS ON TOP, ALWAYS VISIBLE
```

**Non-negotiable rules:**
1. `root.mainloop()` runs on the **main thread** — all tkinter calls must use `root.after(0, fn)`.
2. Never call tkinter widgets from background threads directly — always use `root.after()`.
3. Audio capture, Whisper transcription, and hotkey listener each get their own daemon threads.
4. Use `queue.Queue` for all cross-thread data. Poll via `root.after(100, poll_fn)`.
5. `os._exit(0)` for clean shutdown — kills all daemon threads immediately.
6. `os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"` must be the first line of `main.py`.
7. All configurable values live in `config.py`. No hardcoded constants elsewhere.
8. Test each module in isolation before wiring together.

---

## 1. Project Overview

FrinterFlow is a **100% local, always-on-top voice dictation overlay** for Windows/Linux/macOS.
It allows the user to dictate spoken commentary while browsing, reviewing, or working in other apps — without ever losing focus.

**Key UX flow:**
1. User runs `frinterflow` in any terminal.
2. Terminal shows: model loading progress, then "Overlay launched — you can minimize this terminal."
3. A floating overlay appears at the bottom of the screen (always on top).
4. Overlay shows: animated Frint_bot pixel art (left) + live transcription text (right).
5. User holds **Left CTRL + SHIFT** → bot animates differently, status shows "SLUCHAM...".
6. User releases keys → audio transcribed locally → text appears in overlay + logged to file.
7. Clicking `[X]` in overlay status bar exits cleanly.

---

## 2. Final Project File Structure

```
FrinterFlow/
├── frinterflow/
│   ├── __init__.py
│   ├── main.py          # Entry point: loads model, wires threads, launches overlay
│   ├── overlay.py       # Tkinter floating overlay (Frint_bot + transcript)
│   ├── sprites.py       # Pixel-art sprite matrices + tkinter Canvas renderer
│   ├── audio.py         # Sounddevice audio capture
│   ├── transcriber.py   # faster-whisper wrapper (runs in daemon thread)
│   ├── hotkeys.py       # pynput push-to-talk global listener
│   ├── logger.py        # Timestamped file logging
│   └── config.py        # All constants — colors, sizes, model settings
├── tests/
│   ├── test_audio.py
│   ├── test_transcriber.py
│   ├── test_sprites.py
│   └── test_overlay.py
├── FrinterFlow.md        # Brand/visual specification
├── FrinterFlow-tasks.md  # This file
├── README.md
├── CONTRIBUTING.md
├── LICENSE               # MIT
├── pyproject.toml        # Build + distribution config
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 3. Distribution Strategy — uvx (Recommended)

### Should we use uvx? YES — strongly recommended.

`uvx` is the modern Python equivalent of `npx`. With a single command, users can run FrinterFlow from PyPI without installing Python, creating a venv, or thinking about dependencies. It's the standard for 2024+ Python CLI tools.

**User experience comparison:**

| Method | User command | Requires Python? | Requires venv? |
|--------|-------------|-----------------|----------------|
| `uvx` | `uvx frinterflow` | No (uv installs Python) | No |
| `uv tool install` | `uv tool install frinterflow` then `frinterflow` | No | No |
| `pip install` | `pip install frinterflow` then `frinterflow` | Yes | Recommended |
| `.exe` download | Download + run | No | No |

### How to install `uv` (one-time, for the user)

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### User install commands (after publishing to PyPI)

```bash
# Run once without installing (great for trying out)
uvx frinterflow

# Install globally as a persistent tool
uv tool install frinterflow

# Update to latest version
uv tool upgrade frinterflow

# Traditional pip install
pip install frinterflow

# pip install specific version
pip install frinterflow==1.0.0
```

### `pyproject.toml` — full config for uvx/PyPI compatibility

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "frinterflow"
version = "1.0.0"
description = "Local voice dictation overlay with retro pixel Frint_bot — 100% offline"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.10"
keywords = ["voice", "dictation", "whisper", "local-ai", "overlay", "tui", "frinter"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Win32 (MS Windows)",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
]
dependencies = [
    "faster-whisper>=1.0.0",
    "sounddevice>=0.4.6",
    "numpy>=1.24.0",
    "scipy>=1.11.0",
    "pynput>=1.7.6",
    "rich>=13.7.0",
]

[project.scripts]
frinterflow = "frinterflow.main:run"

[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/FrinterFlow"
Repository = "https://github.com/YOUR_USERNAME/FrinterFlow"
Issues = "https://github.com/YOUR_USERNAME/FrinterFlow/issues"

[project.optional-dependencies]
dev = ["pytest>=8.0", "black>=24.0", "ruff>=0.4.0"]

[tool.hatch.build.targets.wheel]
packages = ["frinterflow"]

[tool.hatch.build.targets.sdist]
include = ["frinterflow/", "README.md", "LICENSE", "pyproject.toml"]
```

### Publishing to PyPI (agent must NOT do this — owner only)

```bash
# Install build tools
pip install hatch

# Build wheel + sdist
hatch build

# Publish to PyPI (requires PyPI account + API token)
hatch publish

# Or with uv:
uv build
uv publish
```

---

## 4. Configuration — `config.py`

```python
# frinterflow/config.py
import os

# --- Frinter Brand Colors ---
COLOR_BLOOM    = "#4a8d83"   # Turkus — body of bot, success status
COLOR_RELATION = "#8a4e64"   # Fiolet — bot eyes, social accents
COLOR_FOCUS    = "#d6b779"   # Zloto  — bot antenna, listening state
COLOR_BG       = "#1a1a2e"   # Dark navy — overlay background
COLOR_DIM      = "#0d0d1a"   # Darker — status bar background
COLOR_TEXT     = "#e0e0e0"   # Primary text

# --- Whisper Model ---
WHISPER_MODEL_SIZE   = "small"   # tiny | base | small | medium | large-v3
WHISPER_DEVICE       = "cpu"     # "cpu" or "cuda"
WHISPER_COMPUTE_TYPE = "int8"    # "int8" (CPU) or "float16" (GPU)
WHISPER_LANGUAGE     = "pl"      # "pl" | "en" | None (auto-detect)
WHISPER_BEAM_SIZE    = 1         # 1 = fastest

# --- Audio ---
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS    = 1

# --- Hotkey (pynput key names) ---
HOTKEY_TRIGGER = {"Key.ctrl_l", "Key.shift"}

# --- Overlay Window ---
OVERLAY_PIXEL_SIZE = 5       # px per sprite cell → 12 cells * 5px = 60px bot width
OVERLAY_WIDTH      = 640     # Total overlay width in px
OVERLAY_HEIGHT     = 120     # Total overlay height in px
OVERLAY_ALPHA      = 0.92    # 0.0 = invisible, 1.0 = fully opaque
OVERLAY_MARGIN_BOTTOM = 48   # Distance from bottom of screen (px, clears taskbar)
OVERLAY_FONT       = ("Consolas", 11)
OVERLAY_FONT_TS    = ("Consolas", 10)  # Timestamp font

# --- Animation ---
ANIMATION_FPS    = 8    # Overlay canvas refresh rate
BOT_BOB_SPEED    = 0.7  # Seconds per full sine cycle

# --- Logging ---
LOG_FILE   = os.path.expanduser("~/frinterflow_log.txt")
LOG_FORMAT = "[{timestamp}] {text}\n"
```

---

## 5. Pixel Sprites — `sprites.py`

### 5.1 Color Legend
- `0` — transparent (skip drawing)
- `1` — primary color (bot body = `COLOR_BLOOM`)
- `2` — highlight / eyes (bot = `COLOR_RELATION`, others = soft white)
- `3` — accent / gold (bot antenna, glow = `COLOR_FOCUS`)

### 5.2 Sprite Matrices

```python
# frinterflow/sprites.py

SPRITES = {
    "tree": [
        [0,0,0,0,1,1,1,1,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,2,2,1,1,1,1,1,0],
        [1,1,1,1,2,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,2,2,1,1,1],
        [0,1,1,1,1,1,1,2,2,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,0,0,0,0],
    ],
    "heart": [
        [0,0,1,1,1,0,0,0,1,1,1,0,0],
        [0,1,1,1,1,1,0,1,1,1,1,1,0],
        [1,1,1,2,2,1,1,1,1,1,1,1,1],
        [1,1,1,2,2,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,1,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0],
    ],
    "brain": [
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,2,2,1,1,1,2,2,1,0],
        [1,1,1,2,2,1,1,1,2,2,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,2,2,2,2,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,0,0,1,1,1,0,0],
        [0,0,0,1,1,0,0,1,1,0,0,0],
    ],
    # bot: 1=COLOR_BLOOM (body), 2=COLOR_RELATION (eyes), 3=COLOR_FOCUS (antenna/glow)
    "bot": [
        [0,0,0,3,3,3,3,3,3,0,0,0],
        [0,0,0,0,0,3,3,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,2,2,1,1,2,2,1,1,0],
        [0,1,1,2,2,1,1,2,2,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,3,3,3,3,3,3,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,1,1,0,0,0,0,1,1,0,0],
    ],
    # wave: 1=COLOR_BLOOM (ocean), 2=soft white "#e8f8f5" (foam/crest)
    "wave": [
        [0,0,1,1,0,0,0,0,0,1,1,0],
        [0,1,1,1,1,0,0,0,1,1,1,1],
        [1,1,2,2,1,1,0,1,1,2,2,1],
        [1,2,2,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0],
    ],
}

# Color maps for Canvas rendering (tkinter hex strings)
SPRITE_COLOR_MAP = {
    "bot":   {1: "#4a8d83", 2: "#8a4e64", 3: "#d6b779"},
    "tree":  {1: "#4a8d83", 2: "#aaffee"},
    "heart": {1: "#8a4e64", 2: "#ffaad4"},
    "brain": {1: "#d6b779", 2: "#fff3c0"},
    "wave":  {1: "#4a8d83", 2: "#e8f8f5"},
}
```

### 5.3 Canvas Renderer (used in overlay.py)

```python
def draw_sprite_on_canvas(canvas, sprite_name: str, pixel_size: int, bob_offset: int = 0):
    """
    Draw a sprite onto a tkinter Canvas using filled rectangles.
    bob_offset: vertical pixel shift for animation (0, 1, or 2).
    Call canvas.delete("all") before calling this to redraw.
    """
    matrix = SPRITES[sprite_name]
    color_map = SPRITE_COLOR_MAP[sprite_name]
    bg = "#1a1a2e"

    for r_idx, row in enumerate(matrix):
        y0 = r_idx * pixel_size + bob_offset
        y1 = y0 + pixel_size
        for c_idx, cell in enumerate(row):
            x0 = c_idx * pixel_size
            x1 = x0 + pixel_size
            if cell == 0:
                continue
            color = color_map.get(cell, "#4a8d83")
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
```

---

## 6. Floating Overlay — `overlay.py`

This is the **core UI module**. All rendering happens here on the main thread via `root.after()`.

```python
# frinterflow/overlay.py
"""
Always-on-top floating tkinter overlay.
- Frameless (overrideredirect)
- Semi-transparent
- Positioned at bottom-center of screen
- Left panel: Frint_bot pixel art (animated)
- Right panel: live transcript text
- Bottom bar: status + [X] close button
- Draggable by clicking anywhere on the overlay
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
        self._setup_bot_canvas()
        self._setup_transcript()
        self._setup_statusbar()
        self._show_welcome()

    # ------------------------------------------------------------------
    # Window setup
    # ------------------------------------------------------------------

    def _setup_window(self):
        r = self.root
        r.title("FrinterFlow")
        r.overrideredirect(True)           # No title bar / frame
        r.attributes("-topmost", True)     # Always on top
        r.attributes("-alpha", OVERLAY_ALPHA)
        r.configure(bg=COLOR_BG)

        # Compute bottom-center position
        sw = r.winfo_screenwidth()
        sh = r.winfo_screenheight()
        x = (sw - OVERLAY_WIDTH) // 2
        y = sh - OVERLAY_HEIGHT - OVERLAY_MARGIN_BOTTOM
        r.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{x}+{y}")
        r.resizable(False, False)

        # Dragging
        r.bind("<ButtonPress-1>", self._on_drag_start)
        r.bind("<B1-Motion>", self._on_drag_motion)

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
        # Add 2px padding for bob animation headroom
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
        self._append("Trzymaj LEWY CTRL + SHIFT, by mowic.\n", tag="dim")

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
        self.status_var = tk.StringVar(value=self._idle_status_text())
        bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=COLOR_DIM,
            fg=COLOR_BLOOM,
            font=("Consolas", 9),
            anchor="w",
            padx=8,
            pady=2,
        )
        bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Close button — right side
        close_btn = tk.Label(
            bar,
            text="  [X]  ",
            bg=COLOR_DIM,
            fg="#8a4e64",
            font=("Consolas", 9, "bold"),
            cursor="hand2",
        )
        close_btn.pack(side=tk.RIGHT)
        close_btn.bind("<Button-1>", lambda _: os._exit(0))

    def _idle_status_text(self) -> str:
        return f"  GOTOWY  |  Log: ~/frinterflow_log.txt"

    # ------------------------------------------------------------------
    # Thread-safe public API (call from ANY thread)
    # ------------------------------------------------------------------

    def set_status(self, status: str):
        self.root.after(0, self._set_status_main, status)

    def add_transcript(self, text: str):
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
            self.status_var.set(self._idle_status_text())

    def _add_transcript_main(self, text: str):
        ts = datetime.now().strftime("%H:%M:%S")
        self._append(f"\n[{ts}] ", "ts")
        self._append(text, "text")
        self._set_status_main("IDLE")

    # ------------------------------------------------------------------
    # Animation loop (runs on main thread via root.after)
    # ------------------------------------------------------------------

    def _animate(self):
        t = time.time()
        bob = int((math.sin(t * (2 * math.pi / BOT_BOB_SPEED)) + 1))
        self.bot_canvas.delete("all")
        draw_sprite_on_canvas(self.bot_canvas, "bot", OVERLAY_PIXEL_SIZE, bob_offset=bob)
        interval_ms = int(1000 / ANIMATION_FPS)
        self.root.after(interval_ms, self._animate)

    # ------------------------------------------------------------------
    # Queue poller (runs on main thread via root.after)
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
    # Run (blocking — call from main thread)
    # ------------------------------------------------------------------

    def run(self):
        self._animate()
        self._poll_queue()
        self.root.mainloop()
```

---

## 7. Audio Capture — `audio.py`

```python
# frinterflow/audio.py
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
        self.result_queue = result_queue  # receives wav file paths
        self._stop_event = threading.Event()
        self._thread = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()

    def _record_loop(self):
        chunks = []
        with sd.InputStream(
            samplerate=AUDIO_SAMPLE_RATE,
            channels=AUDIO_CHANNELS,
            dtype="float32",
        ) as stream:
            while not self._stop_event.is_set():
                data, _ = stream.read(1024)
                chunks.append(data.copy())

        if not chunks:
            return

        audio = np.concatenate(chunks, axis=0)
        audio_int16 = (audio * 32767).astype(np.int16)
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        wav.write(tmp.name, AUDIO_SAMPLE_RATE, audio_int16)
        tmp.close()
        self.result_queue.put(tmp.name)
```

---

## 8. Transcription Engine — `transcriber.py`

```python
# frinterflow/transcriber.py
import os
import threading
import queue
from faster_whisper import WhisperModel
from frinterflow.config import (
    WHISPER_MODEL_SIZE, WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE, WHISPER_LANGUAGE, WHISPER_BEAM_SIZE,
)


class Transcriber:
    def __init__(self, result_queue: queue.Queue):
        self.result_queue = result_queue
        self._model = None
        self._lock = threading.Lock()

    def load_model(self):
        """Blocking. Call once during startup before launching overlay."""
        self._model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE,
        )

    def transcribe_async(self, wav_path: str):
        t = threading.Thread(target=self._run, args=(wav_path,), daemon=True)
        t.start()

    def _run(self, wav_path: str):
        with self._lock:
            try:
                segments, _ = self._model.transcribe(
                    wav_path,
                    language=WHISPER_LANGUAGE,
                    beam_size=WHISPER_BEAM_SIZE,
                )
                text = " ".join(s.text.strip() for s in segments).strip()
                if text:
                    self.result_queue.put(text)
            finally:
                try:
                    os.unlink(wav_path)
                except OSError:
                    pass
```

---

## 9. Hotkey Listener — `hotkeys.py`

```python
# frinterflow/hotkeys.py
from pynput import keyboard
from frinterflow.config import HOTKEY_TRIGGER


class PushToTalkListener:
    def __init__(self, on_start, on_stop):
        self.on_start = on_start
        self.on_stop = on_stop
        self._held = set()
        self._active = False
        self._listener = None

    def start(self):
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
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
```

---

## 10. Logger — `logger.py`

```python
# frinterflow/logger.py
from datetime import datetime
from frinterflow.config import LOG_FILE, LOG_FORMAT


def append_entry(text: str):
    ts = datetime.now().strftime("%H:%M:%S")
    entry = LOG_FORMAT.format(timestamp=ts, text=text)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
```

---

## 11. Entry Point — `main.py`

```python
# frinterflow/main.py
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # MUST be first — PyInstaller fix

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
    def beep(): winsound.Beep(1000, 150)
except ImportError:
    def beep(): print("\a", end="", flush=True)


def run():
    """
    Threading model:
      main thread      → tkinter overlay mainloop (FrinterOverlay.run())
      audio thread     → sounddevice capture (daemon)
      transcribe thread→ faster-whisper inference (daemon)
      pynput thread    → keyboard listener (daemon, auto-created)
      fanout thread    → routes raw transcription to tui_queue + log_queue
      log thread       → writes to file + beeps

    Queues:
      audio_q   : AudioRecorder  → audio_watcher (wav paths)
      raw_q     : Transcriber    → fanout_dispatcher (transcribed text)
      tui_q     : fanout         → FrinterOverlay._poll_queue
      log_q     : fanout         → log_worker
    """
    audio_q = queue.Queue()
    raw_q   = queue.Queue()
    tui_q   = queue.Queue()
    log_q   = queue.Queue()

    transcriber = Transcriber(result_queue=raw_q)
    recorder    = AudioRecorder(result_queue=audio_q)
    overlay     = FrinterOverlay(transcript_queue=tui_q)

    # Load Whisper model (blocking — show terminal progress)
    console.print("\n[bold #4a8d83]FrinterFlow[/] — loading Whisper model...", end=" ")
    with Progress(SpinnerColumn(), TextColumn("[#d6b779]{task.description}"),
                  console=console, transient=True) as p:
        task = p.add_task("Loading...", total=None)
        transcriber.load_model()
        p.update(task, description="Done!")
    console.print("[bold #4a8d83]Model ready.[/]")
    console.print("[dim]Overlay launched — you can minimize this terminal.[/]\n")

    # Fanout dispatcher: raw_q → tui_q + log_q
    def fanout():
        while True:
            text = raw_q.get()
            tui_q.put(text)
            log_q.put(text)

    # Log worker: log_q → file + beep
    def log_worker():
        while True:
            text = log_q.get()
            append_entry(text)
            beep()

    # Audio watcher: audio_q → transcriber (signals overlay PROCESSING)
    def audio_watcher():
        while True:
            wav_path = audio_q.get()
            overlay.set_status("PROCESSING")
            transcriber.transcribe_async(wav_path)

    for fn in (fanout, log_worker, audio_watcher):
        threading.Thread(target=fn, daemon=True).start()

    # Hotkeys
    def on_start():
        overlay.set_status("LISTENING")
        recorder.start()

    def on_stop():
        recorder.stop()
        overlay.set_status("PROCESSING")

    hotkeys = PushToTalkListener(on_start=on_start, on_stop=on_stop)
    hotkeys.start()

    # Block on tkinter mainloop
    overlay.run()
    os._exit(0)


if __name__ == "__main__":
    run()
```

---

## 12. Whisper Model Sizes Reference

| Model | Size on disk | RAM needed | CPU speed | Use when |
|-------|-------------|-----------|-----------|----------|
| `tiny` | ~150 MB | ~300 MB | Fastest | Quick tests, demos |
| `base` | ~290 MB | ~450 MB | Fast | Casual use |
| `small` | ~490 MB | ~700 MB | Medium | **Default — best balance** |
| `medium` | ~1.5 GB | ~2 GB | Slow | High accuracy needed |
| `large-v3` | ~3 GB | ~5 GB | Very slow | Studio accuracy |

Pre-download the model before first run:
```bash
python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8')"
```

---

## 13. Build Instructions

### Development install

```bash
git clone https://github.com/YOUR_USERNAME/FrinterFlow.git
cd FrinterFlow
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/macOS
pip install -e ".[dev]"
frinterflow
```

### End-user install (via PyPI after publishing)

```bash
# Option 1: uvx — zero install, runs directly from PyPI
uvx frinterflow

# Option 2: uv tool — persistent global install
uv tool install frinterflow

# Option 3: pip
pip install frinterflow
```

### Windows Standalone Executable

```bash
pip install pyinstaller

pyinstaller \
  --onefile \
  --windowed \
  --name frinter-flow \
  --hidden-import=faster_whisper \
  --hidden-import=sounddevice \
  --hidden-import=pynput.keyboard._win32 \
  --hidden-import=pynput.mouse._win32 \
  frinterflow/main.py
```

Output: `dist/frinter-flow.exe`

> Note: `--windowed` hides the console window. If overlay does not appear, test with `--console` first to see startup errors.

### Known Build Issues

| Problem | Fix |
|---------|-----|
| `OMP: Error #15` | `KMP_DUPLICATE_LIB_OK=TRUE` already set in `main.py` |
| pynput not firing in `.exe` | `--hidden-import=pynput.keyboard._win32` |
| `sounddevice` no device | Add PortAudio DLL via `--add-binary` |
| Overlay not on top of UAC/admin apps | Run `frinter-flow.exe` as Administrator |
| `tkinter` not found on Linux | `sudo apt install python3-tk` |

---

## 14. Tests

### `tests/test_sprites.py`
```python
from frinterflow.sprites import SPRITES, draw_sprite_on_canvas

def test_all_sprites_defined():
    for name in ("tree", "heart", "brain", "bot", "wave"):
        assert name in SPRITES

def test_wave_dimensions():
    assert len(SPRITES["wave"]) == 8
    assert all(len(row) == 12 for row in SPRITES["wave"])

def test_bot_has_all_cell_types():
    flat = [c for row in SPRITES["bot"] for c in row]
    assert 1 in flat  # body
    assert 2 in flat  # eyes
    assert 3 in flat  # antenna

def test_bot_dimensions():
    assert len(SPRITES["bot"]) == 12
    assert all(len(row) == 12 for row in SPRITES["bot"])
```

### `tests/test_audio.py`
```python
import queue, time
from frinterflow.audio import AudioRecorder

def test_record_and_stop_produces_wav():
    q = queue.Queue()
    rec = AudioRecorder(result_queue=q)
    rec.start()
    time.sleep(0.4)
    rec.stop()
    time.sleep(0.6)
    if not q.empty():
        import os
        path = q.get()
        assert os.path.exists(path)
        assert path.endswith(".wav")
        os.unlink(path)
```

### `tests/test_transcriber.py`
```python
import queue
from frinterflow.transcriber import Transcriber

def test_model_loads_without_error():
    q = queue.Queue()
    t = Transcriber(result_queue=q)
    t.load_model()
    assert t._model is not None
```

### `tests/test_overlay.py`
```python
# Smoke test — just verifies imports and object creation don't crash
import queue
def test_overlay_imports():
    from frinterflow.overlay import FrinterOverlay
    assert FrinterOverlay is not None

def test_config_overlay_values():
    from frinterflow.config import OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_PIXEL_SIZE
    assert OVERLAY_WIDTH > 0
    assert OVERLAY_HEIGHT > 0
    assert OVERLAY_PIXEL_SIZE >= 4
```

Run all:
```bash
pytest tests/ -v
```

---

## 15. Agent Task Checklist

This is the **authoritative task list** for autonomous agents. Execute in order. Do not skip steps.
Mark each `[ ]` as `[x]` when complete. Do not proceed to the next task if the current one fails.

### PHASE 0 — Project Scaffolding

```
[ ] TASK-001  Create directory structure as specified in Section 2
[ ] TASK-002  Create frinterflow/__init__.py (empty or version string)
[ ] TASK-003  Write pyproject.toml (Section 3) — include all classifiers and urls
[ ] TASK-004  Create requirements.txt from Section 3 dependencies
[ ] TASK-005  Write LICENSE file (MIT, year 2025, author = FrinterFlow Contributors)
[ ] TASK-006  Verify: pip install -e ".[dev]" runs without errors
[ ] TASK-007  Verify: frinterflow --help or frinterflow raises ImportError (not yet implemented, that's OK)
```

### PHASE 1 — Configuration

```
[ ] TASK-010  Write frinterflow/config.py (Section 4) — all constants, no hardcodes elsewhere
[ ] TASK-011  Verify: python -c "from frinterflow.config import COLOR_BLOOM; print(COLOR_BLOOM)" prints #4a8d83
```

### PHASE 2 — Sprites

```
[ ] TASK-020  Write frinterflow/sprites.py — all 5 sprite matrices + SPRITE_COLOR_MAP + draw_sprite_on_canvas()
[ ] TASK-021  Verify all sprite names: tree, heart, brain, bot, wave
[ ] TASK-022  Verify bot sprite: 12 rows × 12 cols, cells 1/2/3 all present
[ ] TASK-023  Verify wave sprite: 8 rows × 12 cols
[ ] TASK-024  Run tests/test_sprites.py — all must pass
```

### PHASE 3 — Audio

```
[ ] TASK-030  Write frinterflow/audio.py (Section 7)
[ ] TASK-031  Manual test: record 1 second, verify .wav file created in temp dir
[ ] TASK-032  Manual test: start + stop + start again — verify no thread leak
[ ] TASK-033  Run tests/test_audio.py
```

### PHASE 4 — Transcription

```
[ ] TASK-040  Write frinterflow/transcriber.py (Section 8)
[ ] TASK-041  Run pre-download command to cache Whisper model locally (Section 12)
[ ] TASK-042  Manual test: transcribe a real .wav file, verify non-empty string returned in queue
[ ] TASK-043  Manual test: call transcribe_async twice in parallel — verify _lock prevents crash
[ ] TASK-044  Run tests/test_transcriber.py
```

### PHASE 5 — Hotkeys

```
[ ] TASK-050  Write frinterflow/hotkeys.py (Section 9)
[ ] TASK-051  Manual test: run PushToTalkListener standalone, print on_start/on_stop to terminal
[ ] TASK-052  Verify both Left CTRL and SHIFT must be held — single key must not trigger
[ ] TASK-053  Verify releasing either key triggers on_stop
```

### PHASE 6 — Logger

```
[ ] TASK-060  Write frinterflow/logger.py (Section 10)
[ ] TASK-061  Verify: append_entry("test") creates ~/frinterflow_log.txt with [HH:MM:SS] test
[ ] TASK-062  Verify: calling twice appends (does not overwrite)
```

### PHASE 7 — Overlay (Core UI)

```
[ ] TASK-070  Write frinterflow/overlay.py (Section 6) — full FrinterOverlay class
[ ] TASK-071  Smoke test: python -c "import queue; from frinterflow.overlay import FrinterOverlay; FrinterOverlay(queue.Queue()).run()"
              — overlay must appear at bottom of screen, bot must animate, window must be always-on-top
[ ] TASK-072  Verify: window is frameless (no title bar)
[ ] TASK-073  Verify: window is semi-transparent (OVERLAY_ALPHA applied)
[ ] TASK-074  Verify: clicking [X] label closes the app (os._exit)
[ ] TASK-075  Verify: window is draggable by clicking anywhere on it
[ ] TASK-076  Verify: bot pixel art uses correct colors (teal body, violet eyes, gold antenna)
[ ] TASK-077  Verify: bot bobs up and down (sine animation, 8fps)
[ ] TASK-078  Manual test: call overlay.set_status("LISTENING") from a thread — status bar must update
[ ] TASK-079  Manual test: put text in transcript_queue — text must appear in overlay
[ ] TASK-080  Run tests/test_overlay.py
```

### PHASE 8 — Main Entry Point

```
[ ] TASK-090  Write frinterflow/main.py (Section 11) — KMP fix as FIRST LINE
[ ] TASK-091  Verify: frinterflow command launches, shows model loading in terminal, then overlay appears
[ ] TASK-092  Verify: terminal shows "Overlay launched — you can minimize this terminal"
[ ] TASK-093  Verify: holding LCTRL+SHIFT shows SLUCHAM status in overlay
[ ] TASK-094  Verify: releasing keys shows TRANSKRYBUJE status, then transcript appears
[ ] TASK-095  Verify: transcript is appended to ~/frinterflow_log.txt with correct timestamp
[ ] TASK-096  Verify: audio beep plays after transcript appears
[ ] TASK-097  Verify: multiple sequential dictations work without restart
[ ] TASK-098  Verify: simultaneous transcriptions don't crash (Transcriber._lock)
```

### PHASE 9 — Packaging & Distribution

```
[ ] TASK-100  Verify: pip install -e . (editable) works cleanly
[ ] TASK-101  Verify: uvx frinterflow (after PyPI publish — skip if pre-publish)
[ ] TASK-102  Build wheel: hatch build → verify dist/ contains .whl and .tar.gz
[ ] TASK-103  Build .exe: pyinstaller command from Section 13
[ ] TASK-104  Test .exe on a machine without Python installed
[ ] TASK-105  Verify .exe: overlay appears, transcription works, log file created
```

### PHASE 10 — Tests & CI

```
[ ] TASK-110  Write all 4 test files (tests/test_*.py)
[ ] TASK-111  Run pytest tests/ -v — all tests pass
[ ] TASK-112  Write .github/workflows/ci.yml (Section 17)
[ ] TASK-113  Push to GitHub — CI must pass (green check)
```

### PHASE 11 — Documentation

```
[ ] TASK-120  Verify README.md is complete and accurate (Installation, Usage, Config, FAQ sections)
[ ] TASK-121  Write CONTRIBUTING.md (code style, sprite addition guide, PR checklist)
[ ] TASK-122  Verify pyproject.toml URLs point to correct GitHub repo
[ ] TASK-123  Update version in pyproject.toml to match git tag
```

---

## 16. Frinter Visual Identity Checklist

Before any UI review, verify ALL of these:

- [ ] Background color is `#1a1a2e` (dark navy) — no pure black `#000000`
- [ ] Status/success uses Bloom Turkus `#4a8d83`
- [ ] Listening/focus uses Focus Gold `#d6b779`
- [ ] Bot eyes use Relation Violet `#8a4e64`
- [ ] Bot antenna/glow uses Focus Gold `#d6b779`
- [ ] Overlay is semi-transparent (`OVERLAY_ALPHA = 0.92`)
- [ ] Overlay is frameless (`overrideredirect=True`)
- [ ] Overlay is always on top (`-topmost True`)
- [ ] Overlay starts at bottom-center of screen
- [ ] Overlay is draggable
- [ ] Bot pixel art is 12×12 cells at `OVERLAY_PIXEL_SIZE` px per cell
- [ ] Bot bobs smoothly (sine wave, 8 FPS, no jitter)
- [ ] Text font is monospace (Consolas or Courier)
- [ ] Close button is visible and functional
- [ ] Status bar shows current state (GOTOWY / SLUCHAM / TRANSKRYBUJE)

---

## 17. CI — `.github/workflows/ci.yml`

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Run tests
        run: pytest tests/ -v
      - name: Lint
        run: |
          ruff check frinterflow/
          black --check frinterflow/
```

---

## 18. FAQ for Contributors

**Q: Why tkinter instead of a web overlay or Electron?**
A: Zero additional dependencies. tkinter is bundled with every Python installation and supports `overrideredirect` + `-topmost` natively on all platforms. Electron would add ~150 MB to the binary.

**Q: Why not use Textual/Rich for the overlay?**
A: Textual/Rich render into the terminal. The requirement is a floating window that stays on top of other applications (browser, video player, etc.) — that requires a native windowing system. tkinter Canvas gives pixel-perfect control for the sprite art.

**Q: Why `os._exit(0)` instead of `sys.exit()`?**
A: `sys.exit()` raises `SystemExit` which can be caught by threads. `os._exit()` immediately terminates all threads — essential because pynput and sounddevice threads don't respond to `SystemExit`.

**Q: Can I use GPU for faster transcription?**
A: Yes. Set `WHISPER_DEVICE = "cuda"` and `WHISPER_COMPUTE_TYPE = "float16"` in `config.py`, then install `nvidia-cublas-cu12` and `nvidia-cudnn-cu12`.

**Q: How do I add a new sprite?**
1. Add the matrix to `SPRITES` dict in `sprites.py`
2. Add color mapping to `SPRITE_COLOR_MAP`
3. The sprite is then available to `draw_sprite_on_canvas()`

**Q: Why uvx and not just pip?**
A: `uvx` lets users run `uvx frinterflow` with no prior setup — no Python install, no venv, no PATH issues. `uv` handles everything. This is the gold standard for CLI tool distribution in 2024+.

**Q: The overlay appears but I can't see the bot colors.**
A: tkinter on some Linux distros doesn't support `#rrggbb` hex colors directly in `Canvas.create_rectangle`. Test with the `colorchooser` module. If needed, convert colors to nearest X11 color names as a fallback.

**Q: Overlay flickers during animation.**
A: The `canvas.delete("all")` + full redraw approach can cause flicker on some systems. Alternative: pre-create all rectangle items and update their `fill` color using `canvas.itemconfig(item_id, fill=color)` instead of deleting and recreating.

---

*FrinterFlow-tasks.md v2.0.0 — Agent Build Specification*
*Architecture: tkinter floating overlay + faster-whisper + pynput + uvx distribution*
*Frinter Brand | Open Source | MIT License*
