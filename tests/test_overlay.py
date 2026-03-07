import queue


def test_overlay_imports():
    from frinterflow.overlay import FrinterOverlay
    assert FrinterOverlay is not None


def test_config_overlay_values():
    from frinterflow.config import (
        OVERLAY_WIDTH, OVERLAY_HEIGHT,
        OVERLAY_PIXEL_SIZE, OVERLAY_ALPHA,
        OVERLAY_MARGIN_BOTTOM,
    )
    assert OVERLAY_WIDTH > 0
    assert OVERLAY_HEIGHT > 0
    assert OVERLAY_PIXEL_SIZE >= 4
    assert 0.0 < OVERLAY_ALPHA <= 1.0
    assert OVERLAY_MARGIN_BOTTOM >= 0


def test_config_colors_are_hex():
    from frinterflow.config import (
        COLOR_BLOOM, COLOR_RELATION, COLOR_FOCUS,
        COLOR_BG, COLOR_DIM, COLOR_TEXT,
    )
    for color in (COLOR_BLOOM, COLOR_RELATION, COLOR_FOCUS,
                  COLOR_BG, COLOR_DIM, COLOR_TEXT):
        assert color.startswith("#"), f"Color {color!r} must be hex"
        assert len(color) == 7, f"Color {color!r} must be #rrggbb"


def test_config_hotkey_trigger():
    from frinterflow.config import HOTKEY_TRIGGER
    assert isinstance(HOTKEY_TRIGGER, set)
    assert "Key.ctrl_l" in HOTKEY_TRIGGER
    assert "Key.shift" in HOTKEY_TRIGGER


def test_logger_format():
    from frinterflow.config import LOG_FORMAT
    result = LOG_FORMAT.format(timestamp="12:34:56", text="hello")
    assert "12:34:56" in result
    assert "hello" in result


def test_logger_append(tmp_path):
    import os
    from frinterflow import config as cfg
    original = cfg.LOG_FILE
    cfg.LOG_FILE = str(tmp_path / "test_log.txt")
    try:
        from frinterflow.logger import append_entry
        append_entry("test line one")
        append_entry("test line two")
        with open(cfg.LOG_FILE, encoding="utf-8") as f:
            content = f.read()
        assert "test line one" in content
        assert "test line two" in content
        # verify append (not overwrite)
        assert content.count("\n") == 2
    finally:
        cfg.LOG_FILE = original
