<div align="center">

<pre>
  ██████╗ ██████╗ ██╗███╗   ██╗████████╗███████╗██████╗
  ██╔════╝██╔══██╗██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
  █████╗  ██████╔╝██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
  ██╔══╝  ██╔══██╗██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
  ██║     ██║  ██║██║██║ ╚████║   ██║   ███████╗██║  ██║
  ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
              F  L  O  W
</pre>

**Local voice dictation. Floating pixel overlay. Zero cloud.**

[![License: MIT](https://img.shields.io/badge/License-MIT-4a8d83.svg?style=flat-square)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-d6b779.svg?style=flat-square)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-8a4e64.svg?style=flat-square)](#installation)
[![AI: 100% Local](https://img.shields.io/badge/AI-100%25%20Local-4a8d83.svg?style=flat-square)](#how-it-works)
[![No Cloud Ever](https://img.shields.io/badge/Cloud-Never-d6b779.svg?style=flat-square)](#privacy)

</div>

---

Cloud dictation tools send your voice to a server. They charge subscriptions. They go offline. They transcribe the wrong language. And they run in apps that steal your focus.

**FrinterFlow fixes this.** Hold `Left CTRL + SHIFT`, speak, release — your words appear instantly in a floating pixel-art overlay that sits above every other window. Logged locally with timestamps. Powered entirely by `faster-whisper` on your CPU. Your audio never leaves your machine.

```
 YOUR SCREEN
 ┌─────────────────────────────────────────────────────────────────┐
 │                                                                 │
 │   Chrome / VS Code / any app — full focus, uninterrupted       │
 │                                                                 │
 │                                                                 │
 │                                                                 │
 │  ┌─────────────────────────────────────────────────────────┐   │
 │  │  ░░░░░░░░░░  [14:32:01] Dzisiaj omawiam strukturę...    │   │
 │  │  ░ ░░░░ ░░  [14:32:45] Kolejny punkt — wdrożenie        │   │
 │  │  ░      ░░             modelu whisper.                  │   │
 │  │  ░ ████ ░░  [14:33:10] SLUCHAM...                       │   │
 │  │  ░░░░░░░░░░                                              │   │
 │  │  ░░░░  ░░░░                                              │   │
 │  │──────────────────────────────────────────────────────── │   │
 │  │  GOTOWY  |  Log: ~/frinterflow_log.txt         [X]      │   │
 │  └─────────────────────────────────────────────────────────┘   │
 │        ↑ always on top · frameless · semi-transparent           │
 └─────────────────────────────────────────────────────────────────┘
```

---

## Installation

### Fastest: uvx (no Python setup required)

`uvx` runs FrinterFlow directly from PyPI — no venv, no PATH issues, no Python install needed.

```bash
# Install uv first (one-time, 30 seconds)
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then just run:

```bash
uvx frinterflow
```

To install as a persistent global command:

```bash
uv tool install frinterflow
frinterflow          # works from any terminal, always
uv tool upgrade frinterflow   # update later
```

> **Why uv?** It's 10-100x faster than pip and handles binary wheels reliably — no cmake or build tool errors.

---

<details>
<summary><b>Windows — pip / dev install (click to expand)</b></summary>

### Prerequisites
- Python 3.10+ ([download](https://python.org/downloads))
- FFmpeg: `winget install ffmpeg`

### Option A — pip

```powershell
pip install frinterflow
frinterflow
```

### Option B — dev install (for contributors)

```powershell
git clone https://github.com/YOUR_USERNAME/FrinterFlow.git
cd FrinterFlow
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
frinterflow
```

### Option C — Standalone Executable (no Python required)

Download `frinter-flow.exe` from [Releases](../../releases/latest) and run directly.

</details>

<details>
<summary><b>Linux — Installation Instructions (click to expand)</b></summary>

```bash
# System dependencies (Ubuntu/Debian)
sudo apt install python3-dev python3-tk portaudio19-dev ffmpeg
# Arch: sudo pacman -S python tk portaudio ffmpeg

pip install frinterflow
frinterflow
```

**Note:** `python3-tk` is required for the floating overlay. On Linux, audio beep uses terminal bell instead of `winsound`.

</details>

<details>
<summary><b>macOS — Installation Instructions (click to expand)</b></summary>

```bash
brew install python portaudio ffmpeg
pip install frinterflow
frinterflow
```

**Note:** macOS requires microphone permissions — grant in System Settings → Privacy & Security → Microphone.

</details>

> **Tip:** Restart your terminal after installation to ensure the `frinterflow` command is recognized.

---

## Get Started

| Step | What Happens |
|------|-------------|
| 1. Launch | Run `frinterflow` in any terminal — model loads, terminal shows progress |
| 2. Overlay appears | Frint_bot floating window appears at the **bottom of your screen** |
| 3. Minimize terminal | The floating overlay stays on top — terminal is no longer needed |
| 4. Speak | Hold `Left CTRL + SHIFT` — bot animates, status shows "SLUCHAM..." |
| 5. Release | Audio transcribed locally, text appears in overlay |
| 6. Done | Entry timestamped and logged to `~/frinterflow_log.txt`. Beep confirms. |

> **Pro tip:** The overlay floats above Chrome, VS Code, or any other app. You never have to switch windows to dictate.

---

## How It Works

FrinterFlow is built around a clean **push-to-talk pipeline:**

```
[KEYBOARD]   Left CTRL + SHIFT held down
      │
      ▼
[AUDIO]      sounddevice captures mic → numpy buffer
      │
      ▼
[RELEASE]    Buffer saved to temp .wav file
      │
      ▼
[WHISPER]    faster-whisper transcribes locally on CPU (or GPU)
      │
      ├──► [OVERLAY]   Text appears in floating Frint_bot window (always on top)
      │
      └──► [LOG]       Entry appended to ~/frinterflow_log.txt with timestamp
                       + audio beep confirms processing complete
```

Everything happens locally. No network calls after the one-time model download.

---

## Usage

Launch from any terminal:

```bash
frinterflow
```

### Controls

| Action | How |
|--------|-----|
| Start recording | Hold `Left CTRL + SHIFT` |
| Stop & transcribe | Release either key |
| Move overlay | Click and drag anywhere on it |
| Quit | Click `[X]` in the overlay status bar |

### Log Output Format

Every transcription is saved to `~/frinterflow_log.txt`:

```
[14:30:15] The main CTA button on this landing page is too small.
[14:31:02] We need to revisit the mobile breakpoints for the hero section.
[14:33:47] Reminder: check contrast ratio on the footer links.
```

---

## Configuration

All settings live in `frinterflow/config.py`:

```python
WHISPER_MODEL_SIZE = "small"   # tiny | base | small | medium | large-v3
WHISPER_LANGUAGE   = "pl"      # "pl" | "en" | None (auto-detect)
WHISPER_DEVICE     = "cpu"     # "cpu" | "cuda" (if GPU available)
LOG_FILE           = "~/frinterflow_log.txt"
```

### Whisper Model Sizes

| Model | RAM | Speed (CPU) | Accuracy | Best For |
|-------|-----|-------------|----------|----------|
| `tiny` | ~150 MB | Fastest | Basic | Quick notes, short phrases |
| `base` | ~300 MB | Fast | Good | General use |
| `small` | ~500 MB | Medium | Very Good | **Recommended default** |
| `medium` | ~1.5 GB | Slow | Excellent | High-stakes transcription |
| `large-v3` | ~3 GB | Slowest | Best | Studio-quality accuracy |

### GPU Acceleration (CUDA)

If you have an NVIDIA GPU:

```python
# frinterflow/config.py
WHISPER_DEVICE       = "cuda"
WHISPER_COMPUTE_TYPE = "float16"
```

Install CUDA dependencies:

```bash
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12
```

### Changing Language

```python
WHISPER_LANGUAGE = "en"   # English
WHISPER_LANGUAGE = "de"   # German
WHISPER_LANGUAGE = None   # Auto-detect (slightly slower)
```

---

## Features

| Feature | FrinterFlow | Cloud Tools | Other Local Tools |
|---------|:-----------:|:-----------:|:-----------------:|
| 100% local — no internet | YES | NO | YES |
| Free unlimited transcription | YES | NO | YES |
| Floating overlay (always on top) | YES | NO | NO |
| Frameless · semi-transparent window | YES | NO | NO |
| Push-to-talk (global hotkey) | YES | Varies | Rarely |
| Timestamped log file | YES | NO | Rarely |
| Works while other apps are focused | YES | YES | Rarely |
| No account / API key required | YES | NO | YES |
| Polish language optimized | YES | YES | Varies |
| Animated pixel-art mascot (Frint_bot) | YES | NO | NO |
| `uvx` zero-install | YES | N/A | Rarely |

---

## Privacy

> **Your audio never leaves your computer.**

- Microphone input is processed entirely in RAM
- Temporary `.wav` file is deleted immediately after transcription
- No telemetry, no analytics, no network calls (after model download)
- The Whisper model is cached locally in `~/.cache/huggingface/hub/`

---

## Build Standalone Executable

Compile FrinterFlow into a single `.exe` (Windows, no Python required):

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

> `--windowed` hides the console. If the overlay doesn't appear, test with `--console` first to see startup errors.

If you have an NVIDIA GPU and want to ship CUDA support in the `.exe`, also add:
```bash
--collect-all nvidia
```

---

## Tech Stack

| Component | Library | Why |
|-----------|---------|-----|
| AI Transcription | `faster-whisper` | 4x faster than openai-whisper, Int8 CPU quantization |
| Audio Capture | `sounddevice` + `numpy` | Cross-platform, low-latency stream |
| WAV Export | `scipy` | Lightweight buffer-to-file, no FFmpeg dependency |
| Hotkeys | `pynput` | Global OS-level listener, works while other apps are focused |
| Floating Overlay | `tkinter` | Built-in Python, supports `overrideredirect` + `-topmost` natively |
| Pixel Art | `tkinter.Canvas` | Per-cell rectangle drawing — precise retro pixel control |
| Terminal Splash | `rich` | Styled model loading progress in terminal |
| Audio Feedback | `winsound` (Windows) | Zero-dependency beep; terminal bell fallback on Linux/macOS |

---

## Roadmap

- [x] Push-to-talk recording
- [x] Local Whisper transcription
- [x] Floating always-on-top pixel overlay (tkinter)
- [x] Animated Frint_bot mascot with sine bobbing
- [x] Animated wave sprite (decorative)
- [x] Timestamped log file
- [x] Draggable overlay
- [x] `uvx frinterflow` zero-install distribution
- [ ] GPU (CUDA) one-click config
- [ ] Custom output file via CLI flag (`--output review.md`)
- [ ] Auto-translation (transcribe in Polish, output in English)
- [ ] Configurable hotkey via `config.py`
- [ ] Voice activity detection (VAD) — auto-start without holding keys
- [ ] Multiple language profiles
- [ ] Overlay position persistence (remember last position)
- [ ] Windows tray icon integration

---

## FAQ

**Q: Does FrinterFlow send my audio anywhere?**

No. All processing is local. The only network call is the one-time model download from HuggingFace on first launch.

**Q: Why does first launch take a while?**

FrinterFlow downloads the Whisper model (~500 MB for `small`) on first run. Subsequent launches are instant.

**Q: The hotkey doesn't work when a game / admin app is focused.**

Some elevated-privilege applications block global keyboard hooks. Run FrinterFlow as Administrator (`Right-click → Run as Administrator`) to fix this.

**Q: Can I change the hotkey from CTRL+SHIFT to something else?**

Yes — edit `HOTKEY_TRIGGER` in `frinterflow/config.py`:

```python
HOTKEY_TRIGGER = {"Key.ctrl_l", "Key.shift"}  # default
HOTKEY_TRIGGER = {"Key.ctrl_r", "Key.alt_l"}  # example alternative
```

**Q: Does it work with languages other than Polish?**

Yes. Set `WHISPER_LANGUAGE` in `config.py` to any [Whisper-supported language code](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py), or `None` for auto-detection.

**Q: Will there be a macOS/Linux native build?**

The Python source runs on all platforms now. Native binary packaging for macOS (`.app`) and Linux (AppImage) is on the roadmap.

**Q: What's Frint_bot?**

Frint_bot is FrinterFlow's pixel-art mascot — a retro robot rendered as colored rectangles on a tkinter Canvas. It sits in the left panel of the floating overlay, bobbing gently via a sine animation. Built from the three Frinter brand colors: teal body (`#4a8d83`), violet eyes (`#8a4e64`), gold antenna (`#d6b779`).

**Q: The overlay appears behind other windows.**

This shouldn't happen — `tkinter`'s `-topmost` flag is applied on launch. If a specific fullscreen or admin application covers it, right-click `frinter-flow.exe` → Run as Administrator.

---

## Contributing

FrinterFlow is open source and contributions are welcome.

**Ways to contribute:**
- [Bug Report](../../issues/new?template=bug_report.md) — Found something broken?
- [Feature Request](../../issues/new?template=feature_request.md) — Have an idea?
- [Pull Request](../../pulls) — Fix a bug or build a feature

**Before contributing, read [`CONTRIBUTING.md`](CONTRIBUTING.md)** for code style, branch naming, and PR checklist.

### Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/FrinterFlow.git
cd FrinterFlow
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest tests/ -v
```

**Code style:** `black` formatter + `ruff` linter. Run before committing:

```bash
black frinterflow/
ruff check frinterflow/
```

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=delta240mvt/FrinterFlow&type=Date)](https://star-history.com/#delta240mvt/FrinterFlow&Date)

---

## License

MIT — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

**FrinterFlow** — part of the [Frinter](https://frinter.app) personal productivity ecosystem

*Built with the Retro Pixel aesthetic. Local first. Always.*

</div>
