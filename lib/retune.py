"""Pitch-shift helpers — PSARC retune disabled (sloppak/open-format only)."""

import logging

log = logging.getLogger("slopsmith.lib.retune")

_UNSUPPORTED = "Encrypted Rocksmith PSARC archives are not supported"


def get_tuning(psarc_path: str) -> tuple[list[int], bool]:
    raise NotImplementedError(_UNSUPPORTED)


def retune_to_standard(psarc_path: str, output_path: str | None = None, on_progress=None) -> str:
    raise NotImplementedError(_UNSUPPORTED)
