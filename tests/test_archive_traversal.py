"""Path-traversal rejection for sloppak zip extraction.

`lib/sloppak.py::_unpack_zip` consumes attacker-controlled archive entry
names from files that land in `DLC_DIR`. A crafted entry name with `..`
segments, an absolute path, or backslash separators must not write outside
the destination directory.
"""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

import pytest


# ── Sloppak zip-slip ──────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "evil_name_template",
    [
        "../escaped.txt",
        "../" * 8 + "tmp/SLOPSMITH_PWNED_SLOPPAK",
        "{abs}",
        "subdir/../../escaped.txt",
        ".",
        "subdir/..",
    ],
)
def test_unpack_sloppak_zip_rejects_traversal(tmp_path, evil_name_template, caplog):
    from sloppak import _unpack_zip

    src = tmp_path / "evil.sloppak"
    dest = tmp_path / "dest"
    abs_target = (tmp_path / "abs_sloppak.txt").resolve()
    evil_name = evil_name_template.format(abs=str(abs_target))

    with zipfile.ZipFile(src, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.yaml", b"title: t\n")
        zf.writestr(evil_name, b"pwned")

    with caplog.at_level(logging.WARNING, logger="slopsmith.lib.sloppak"):
        _unpack_zip(src, dest)

    # Manifest landed inside dest.
    assert (dest / "manifest.yaml").exists()
    # No file escaped the dest root.
    for p in dest.rglob("*"):
        if p.is_file():
            assert dest.resolve() in p.resolve().parents
    assert not (tmp_path / "escaped.txt").exists()
    assert not abs_target.exists()
    if evil_name in (".", "subdir/.."):
        assert any(
            "resolving to unpack root" in r.getMessage() for r in caplog.records
        ), caplog.records


def test_unpack_sloppak_zip_allows_safe_members(tmp_path):
    """Sanity: nested benign entries still extract."""
    from sloppak import _unpack_zip

    src = tmp_path / "good.sloppak"
    dest = tmp_path / "dest"

    with zipfile.ZipFile(src, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.yaml", b"title: t\n")
        zf.writestr("arrangements/lead.json", b"{}")
        zf.writestr("stems/full.ogg", b"oggdata")

    _unpack_zip(src, dest)

    assert (dest / "manifest.yaml").read_bytes().startswith(b"title:")
    assert (dest / "arrangements" / "lead.json").read_bytes() == b"{}"
    assert (dest / "stems" / "full.ogg").read_bytes() == b"oggdata"
