🌊 Frinter Flow
Frinter Flow is a blazing-fast, 100% local, always-on-top voice transcription overlay. Designed for seamless real-time commentary, note-taking, and logging without interrupting your workflow or losing focus on your active window.

Unlike cloud-based dictation tools, Frinter Flow runs entirely on your local machine using the highly optimized faster-whisper engine. No API keys, no subscription costs, and total privacy.

✨ Key Features
🔒 100% Local & Private: Your audio never leaves your computer. Powered by faster-whisper running on your CPU/GPU.

🆓 Zero API Costs: Transcribe unlimited hours of audio for free.

📌 Always-on-Top Overlay: A sleek, semi-transparent UI that floats above your browser or active apps. Perfect for live website commentary or video reviews.

🎙️ "Walkie-Talkie" Mode: Press and hold Left CTRL + SHIFT to record. Release to instantly transcribe and log.

📝 Dual Logging: Transcribed text appears instantly in the floating UI and is simultaneously appended to a local .txt file with precise timestamps.

⚡ CLI-Ready: Built to be compiled as a standalone executable. Just type frinter-flow in your terminal to summon your dictation assistant.

🚀 How It Works
Launch frinter-flow from your terminal or shortcut.

A minimalist, dark-mode floating window appears on your screen.

Hold Left CTRL + SHIFT and speak your thoughts.

Release the keys. Frinter Flow processes the audio in milliseconds, plays a subtle beep, and logs your transcribed text like this:
[14:30:15] The main CTA button on this landing page is too small.

🛠️ Installation & Setup
Prerequisites
Python 3.10+ installed and added to your system PATH.

FFmpeg installed (required by Whisper for audio processing). On Windows, you can install it via: winget install ffmpeg

1. Clone & Setup Environment
Bash
git clone https://github.com/yourusername/frinter-flow.git
cd frinter-flow

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
2. Install Dependencies
Bash
pip install faster-whisper sounddevice scipy pynput pyinstaller
3. Build the Executable (CLI Tool)
To turn Frinter Flow into a portable .exe file without a background console window, run:

Bash
pyinstaller --noconsole --onefile --hidden-import=faster_whisper --name=frinter-flow main.py
Note: Make sure your main script is named main.py.

Once the build is complete, you will find frinter-flow.exe inside the dist/ folder.

💻 Usage
For the best experience, add the folder containing frinter-flow.exe to your system's PATH variables.

Then, simply open any terminal and type:

Bash
frinter-flow
Start Recording: Press and hold Left CTRL + Left SHIFT

Stop & Transcribe: Release the keys

Exit: Close the floating window

🧰 Tech Stack
AI Engine: faster-whisper (Int8 Quantization for max CPU speed)

Audio Capture: sounddevice & scipy

Hotkeys: pynput

GUI: tkinter

📝 To-Do / Roadmap
[ ] Add support for GPU acceleration (CUDA) out of the box.

[ ] Allow custom output file paths via CLI arguments (e.g., frinter-flow --output review.md).

[ ] Add auto-translation capabilities.
