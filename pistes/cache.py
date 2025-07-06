from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar


_T = TypeVar("_T")


class NotFoundError(ValueError):
    pass


class Cache(ABC, Generic[T]):
    def get(self, address: str) -> T:
        if (v := self._get_from_cache(address)) is not None:
            return v
        v = self._create(address)
        self._add_to_cache(v)
        return v

    @abstractmethod
    def _get_from_cache(self, address: str) -> T | None: ...

    @abstractmethod
    def _create(self, address: str) -> T: ...

    @abstractmethod
    def _add_to_cache(self, address: str, value: T) -> None: ...


FORBIDDEN = {k: f"-{ord(c):x}" for k in "-/<>:|?*\"\\"}
FORBIDDEN_INV = {v: k for k, v in FORBIDDEN.items()}


def _clean_string(s: str) -> str:
    return ''.join(FORBIDDEN.get(c, c) for c in s)


def _undo_clean(s: str) -> str:
    def parts():
        for i, p in s.split("-"):
            if not i:
                yield p
            else:
                try:
                    yield FORBIDDEN_INV["-" + p[:2]]
                    yield p[2:]
                except KeyError:
                    yield p
    return "".join(parts)


class FilesystemCache(Cache[Path]):
    def __init__(self, root: Path) -> None:
        self.root = root

    def _get_from_cache(self, address: str) -> Path | None:
        if (fname := root / _clean_string(address)).exists():
            return fname
        return None

    @abstractmethod
    def _create(self, address: str) -> T: ...

    @abstractmethod
    def _add_to_cache(self, address: str, value: T) -> None:
        pass  # Creating the file adds it to the cache!
