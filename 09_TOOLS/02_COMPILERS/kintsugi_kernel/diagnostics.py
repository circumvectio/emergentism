from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Issue:
    path: str
    code: str
    message: str


@dataclass(frozen=True)
class BaselineResult:
    collected: int
    failures: int
    issues: tuple[Issue, ...]


class KintsugiError(Exception):
    def __init__(self, code: str, path: str, message: str):
        super().__init__(message)
        self.code = code
        self.path = path
        self.message = message
