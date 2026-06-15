"""CDLC PSARC builder disabled — sloppak/open-format only."""

import logging

log = logging.getLogger("slopsmith.lib.cdlc_builder")

_UNSUPPORTED = "Building encrypted Rocksmith PSARC archives is not supported"


def build_cdlc(*args, **kwargs):
    raise NotImplementedError(_UNSUPPORTED)
