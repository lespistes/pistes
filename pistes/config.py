import os
from functools import cache
from pathlib import Path
from typing import Any

import tomlkit

CONFIG_FILE = "pistes.toml"


@cache
def path() -> Path:
    # https://specifications.freedesktop.org/basedir-spec/latest/
    try:
        path = os.environ["XDG_CONFIG_HOME"]
    except KeyError:
        try:
            home = os.environ["HOME"]
        except KeyError:
            home = "~"
        path = home + "/.config"
    return Path(path).expanduser() / CONFIG_FILE


@cache
def read() -> dict[str, Any]:
    return tomlkit.loads(path().read_text()) if path().exists() else {}


@cache
def write() -> None:
    # Do better
    path().write_text(tomlkit.dumps(read()))
