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
WHISPER_MODEL_SIZE   = "small"    # tiny | base | small | medium | large-v3
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
OVERLAY_PIXEL_SIZE    = 5     # px per sprite cell -> 12 cells * 5px = 60px bot width
OVERLAY_WIDTH         = 640   # Total overlay width in px
OVERLAY_HEIGHT        = 150   # Total overlay height in px
OVERLAY_ALPHA         = 0.92  # 0.0 = invisible, 1.0 = fully opaque
OVERLAY_MARGIN_BOTTOM = 48    # Distance from bottom of screen (px, clears taskbar)
OVERLAY_FONT          = ("Consolas", 11)
OVERLAY_FONT_TS       = ("Consolas", 10)

# --- Animation ---
ANIMATION_FPS  = 8    # Overlay canvas refresh rate
BOT_BOB_SPEED  = 0.7  # Seconds per full sine cycle

# --- Logging ---
LOG_FILE   = os.path.expanduser("~/frinterflow_log.txt")
LOG_FORMAT = "[{timestamp}] {text}\n"
