"""An empty but well-formed .gpl palette must be skipped, not crash."""
import os
import signal

if not hasattr(signal, "SIGPIPE"):
    # Windows has no SIGPIPE; the module installs a SIGPIPE handler at
    # import time, so provide the constant and ignore the failing call.
    signal.SIGPIPE = 13
_real_signal = signal.signal


def _safe_signal(sig, handler):
    try:
        return _real_signal(sig, handler)
    except (ValueError, AttributeError, OSError):
        return None


if os.name != "posix":
    signal.signal = _safe_signal

import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "colout"))

import colout


def test_empty_palette_is_skipped(tmp_path):
    pal = tmp_path / "empty.gpl"
    pal.write_text("GIMP Palette\nName: Empty\nColumns: 3\n")
    before = set(colout.context["colormaps"])
    colout.load_palettes(str(tmp_path))
    after = set(colout.context["colormaps"])
    assert "empty" not in after - before


def test_nonempty_palette_still_loads(tmp_path):
    pal = tmp_path / "one.gpl"
    pal.write_text("GIMP Palette\nName: One\n# comment\n255   0   0\tred\n")
    colout.load_palettes(str(tmp_path))
    assert "one" in colout.context["colormaps"]
    assert len(colout.context["colormaps"]["one"]) > 0
