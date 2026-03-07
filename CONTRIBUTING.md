# Contributing to FrinterFlow

Thank you for your interest in contributing! FrinterFlow is open source and welcomes bug fixes, features, documentation improvements, and new sprites.

## Setup

```bash
git clone https://github.com/delta240mvt/FrinterFlow.git
cd FrinterFlow
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -e ".[dev]"
```

## Code Style

- Formatter: `black frinterflow/`
- Linter: `ruff check frinterflow/`
- Run both before committing.

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat/short-description` | `feat/vad-mode` |
| Bug fix | `fix/short-description` | `fix/hotkey-release` |
| Docs | `docs/short-description` | `docs/install-linux` |

## PR Checklist

Before opening a pull request:

- [ ] `pytest tests/ -v` — all tests pass
- [ ] `black --check frinterflow/` — no formatting issues
- [ ] `ruff check frinterflow/` — no lint errors
- [ ] No hardcoded values — all constants in `config.py`
- [ ] No tkinter calls from background threads — use `root.after(0, fn)`
- [ ] New sprites added to both `SPRITES` and `SPRITE_COLOR_MAP` in `sprites.py`

## Adding a New Sprite

1. Add a 2D matrix to `SPRITES` in `frinterflow/sprites.py`
2. Add color mapping to `SPRITE_COLOR_MAP` in the same file
3. Add a test in `tests/test_sprites.py` verifying dimensions and cell values
4. Document the sprite in `FrinterFlow.md`

Cell values:
- `0` — transparent (skip drawing)
- `1` — primary color
- `2` — highlight / secondary color
- `3` — accent color (currently bot-only)

## Reporting Bugs

Use [GitHub Issues](https://github.com/delta240mvt/FrinterFlow/issues) with the **bug report** template.
Include: OS version, Python version, steps to reproduce, error output.

## Feature Requests

Use [GitHub Issues](https://github.com/delta240mvt/FrinterFlow/issues) with the **feature request** template.

## Questions

Open a [GitHub Discussion](https://github.com/delta240mvt/FrinterFlow/discussions) for general questions.
