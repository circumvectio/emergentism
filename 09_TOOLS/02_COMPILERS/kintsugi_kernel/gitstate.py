from __future__ import annotations

import os
import json
import stat
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .codec import canonical_json_bytes, raw_hash
from .diagnostics import KintsugiError
from .markdown import synchronize_receipt_markdown
from .records import RECEIPT_IDENTITIES, attempt_paths, canonical_attempt


@dataclass(frozen=True, order=True)
class FileRecord:
    path: str
    kind: str
    sha256: str


@dataclass(frozen=True)
class WorktreeRecord:
    root: Path
    head: str
    branch: str | None


@dataclass(frozen=True)
class GitState:
    root: Path
    head: str
    branch: str | None
    common_dir: Path
    base_commit: str
    committed_paths: tuple[str, ...]
    staged_paths: tuple[str, ...]
    unstaged_paths: tuple[str, ...]
    unrepresentable_mode_paths: tuple[str, ...]
    noncanonical_index_paths: tuple[str, ...]
    untracked_records: tuple[FileRecord, ...]


@dataclass(frozen=True)
class AttemptPlan:
    id: str
    phase: str
    receipt_id: str
    predecessor_id: str | None
    paths: tuple[str, str, str, str]


@dataclass(frozen=True)
class _HistoricalAttemptRecord:
    phase: str
    receipt_id: str
    identity: tuple[Any, ...]
    statuses: frozenset[str]
    disappeared_on_lineage: bool


def _git_environment() -> dict[str, str]:
    environment = os.environ.copy()
    for name in (
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_DIR",
        "GIT_INDEX_FILE",
        "GIT_NAMESPACE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_REPLACE_REF_BASE",
        "GIT_SHALLOW_FILE",
        "GIT_WORK_TREE",
    ):
        environment.pop(name, None)
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    environment["LC_ALL"] = "C"
    return environment


def _run_git(root: Path, argv: tuple[str, ...], *, allowed: tuple[int, ...] = (0,)) -> bytes:
    environment = _git_environment()
    try:
        completed = subprocess.run(
            ["git", "-c", "core.fileMode=true", *argv],
            cwd=root,
            env=environment,
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "git", f"cannot execute Git: {exc.__class__.__name__}"
        ) from None
    if completed.returncode not in allowed:
        command = " ".join(argv)
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            "git",
            f"Git command failed with exit {completed.returncode}: {command}",
        )
    return completed.stdout


def _run_git_input(root: Path, argv: tuple[str, ...], payload: bytes) -> bytes:
    environment = _git_environment()
    try:
        completed = subprocess.run(
            ["git", "-c", "core.fileMode=true", *argv],
            cwd=root,
            env=environment,
            check=False,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "git", f"cannot execute Git: {exc.__class__.__name__}"
        ) from None
    if completed.returncode != 0:
        command = " ".join(argv)
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            "git",
            f"Git command failed with exit {completed.returncode}: {command}",
        )
    return completed.stdout


def _run_git_z(root: Path, argv: tuple[str, ...]) -> tuple[bytes, ...]:
    payload = _run_git(root, argv)
    if payload and not payload.endswith(b"\0"):
        raise KintsugiError("KIN-E-CONCURRENT", "git", "Git -z output lacks a terminal NUL")
    return tuple(payload.split(b"\0")[:-1]) if payload else ()


def _decode_git_path(payload: bytes) -> str:
    try:
        value = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        raise KintsugiError("KIN-E-CONCURRENT", "git", "Git path is not valid UTF-8") from None
    if (
        not value
        or value.startswith("/")
        or "\\" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise KintsugiError("KIN-E-CONCURRENT", "git", "Git emitted a non-repository path")
    return value


def _resolve_commit(root: Path, ref: str) -> str:
    if not isinstance(ref, str) or not ref:
        raise KintsugiError("KIN-E-CONCURRENT", "git", "commit reference is empty")
    payload = _run_git(root, ("rev-parse", "--verify", f"{ref}^{{commit}}"))
    try:
        commit = payload.decode("ascii", errors="strict").strip()
    except UnicodeDecodeError:
        raise KintsugiError("KIN-E-CONCURRENT", "git", "resolved commit is not ASCII") from None
    if len(commit) != 40 or any(character not in "0123456789abcdef" for character in commit):
        raise KintsugiError("KIN-E-CONCURRENT", "git", "resolved commit is not a full SHA-1")
    return commit


def resolve_git_common_dir(root: Path) -> Path:
    try:
        resolved_root = root.resolve(strict=True)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "git", f"worktree root is unavailable: {exc.__class__.__name__}"
        ) from None
    payload = _run_git(resolved_root, ("rev-parse", "--git-common-dir"))
    try:
        common_text = payload.decode("utf-8", errors="strict").strip()
    except UnicodeDecodeError:
        raise KintsugiError("KIN-E-CONCURRENT", "git", "Git common directory is not UTF-8") from None
    if not common_text:
        raise KintsugiError("KIN-E-CONCURRENT", "git", "Git common directory is empty")
    candidate = Path(common_text)
    if not candidate.is_absolute():
        candidate = resolved_root / candidate
    try:
        return candidate.resolve(strict=True)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "git", f"Git common directory is unavailable: {exc.__class__.__name__}"
        ) from None


def _branch(root: Path) -> str | None:
    payload = _run_git(
        root,
        ("symbolic-ref", "--quiet", "--short", "HEAD"),
        allowed=(0, 1),
    )
    if not payload:
        return None
    try:
        value = payload.decode("utf-8", errors="strict").strip()
    except UnicodeDecodeError:
        raise KintsugiError("KIN-E-CONCURRENT", "git", "branch name is not UTF-8") from None
    return value or None


def _parse_name_status(tokens: tuple[bytes, ...]) -> tuple[str, ...]:
    paths: set[str] = set()
    index = 0
    while index < len(tokens):
        try:
            status = tokens[index].decode("ascii", errors="strict")
        except UnicodeDecodeError:
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git status token is not ASCII") from None
        index += 1
        if not status or status[0] not in "ACDMRTUXB":
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git emitted an unknown status token")
        path_count = 2 if status[0] in "RC" else 1
        if index + path_count > len(tokens):
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git status record is truncated")
        for raw_path in tokens[index:index + path_count]:
            paths.add(_decode_git_path(raw_path))
        index += path_count
    return tuple(sorted(paths))


def _parse_unrepresentable_mode_paths(tokens: tuple[bytes, ...]) -> tuple[str, ...]:
    paths: set[str] = set()
    index = 0
    while index < len(tokens):
        try:
            fields = tokens[index].decode("ascii", errors="strict").split(" ")
        except UnicodeDecodeError:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "git", "Git raw diff header is not ASCII"
            ) from None
        index += 1
        if len(fields) != 5 or not fields[0].startswith(":"):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "git", "Git raw diff record is malformed"
            )
        old_mode = fields[0][1:]
        new_mode = fields[1]
        status = fields[4]
        if not status or status[0] not in "ACDMRTUXB":
            raise KintsugiError(
                "KIN-E-CONCURRENT", "git", "Git raw diff status is invalid"
            )
        path_count = 2 if status[0] in "RC" else 1
        if index + path_count > len(tokens):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "git", "Git raw diff paths are truncated"
            )
        record_paths = [
            _decode_git_path(value) for value in tokens[index:index + path_count]
        ]
        index += path_count
        supported_modes = {"000000", "100644", "100755", "120000"}
        unsupported_transition = (
            old_mode not in supported_modes or new_mode not in supported_modes
        )
        executable_transition = (
            (new_mode == "100755" and old_mode != "100755")
            or (
                old_mode == "100755"
                and new_mode not in {"100755", "000000"}
            )
        )
        if unsupported_transition or executable_transition:
            paths.update(record_paths)
    return tuple(sorted(paths))


def _parse_noncanonical_index_paths(tokens: tuple[bytes, ...]) -> tuple[str, ...]:
    paths: set[str] = set()
    for token in tokens:
        if len(token) < 3 or token[1:2] != b" ":
            raise KintsugiError(
                "KIN-E-CONCURRENT", "git", "Git index visibility record is malformed"
            )
        tag = token[:1]
        path = _decode_git_path(token[2:])
        if tag != b"H":
            paths.add(path)
    return tuple(sorted(paths))


def _exact_component_metadata(
    directory_descriptor: int,
    part: str,
    *,
    code: str,
    relative: str,
) -> os.stat_result:
    with os.scandir(directory_descriptor) as iterator:
        matches = [
            entry for entry in iterator
            if entry.name.casefold() == part.casefold()
        ]
        exact = [entry for entry in matches if entry.name == part]
        if len(matches) != 1 or len(exact) != 1:
            raise KintsugiError(
                code,
                relative,
                "path components must have one unique exact spelling",
            )
        return exact[0].stat(follow_symlinks=False)


@contextmanager
def _open_repo_parent_fd(
    root: Path,
    relative: str,
    *,
    code: str,
) -> Iterator[tuple[int, str, os.stat_result]]:
    """Hold a no-follow descriptor chain to the exact parent of a repo leaf."""

    directory_flag = getattr(os, "O_DIRECTORY", 0)
    nofollow_flag = getattr(os, "O_NOFOLLOW", 0)
    if directory_flag == 0 or nofollow_flag == 0:
        raise KintsugiError(
            code,
            relative,
            "safe descriptor-relative path traversal is unavailable",
        )
    descriptor: int | None = None

    try:
        _decode_git_path(relative.encode("utf-8", errors="strict"))
        parts = relative.split("/")
        root_path = root.resolve(strict=True)
        descriptor = os.open(
            root_path,
            os.O_RDONLY | directory_flag | nofollow_flag,
        )
        for part in parts[:-1]:
            expected_metadata = _exact_component_metadata(
                descriptor,
                part,
                code=code,
                relative=relative,
            )
            if not stat.S_ISDIR(expected_metadata.st_mode):
                raise KintsugiError(
                    code,
                    relative,
                    "path has a non-directory or symlinked parent",
                )
            child = os.open(
                part,
                os.O_RDONLY | directory_flag | nofollow_flag,
                dir_fd=descriptor,
            )
            child_metadata = os.fstat(child)
            current_metadata = _exact_component_metadata(
                descriptor,
                part,
                code=code,
                relative=relative,
            )
            expected_identity = (expected_metadata.st_dev, expected_metadata.st_ino)
            child_identity = (child_metadata.st_dev, child_metadata.st_ino)
            current_identity = (current_metadata.st_dev, current_metadata.st_ino)
            if (
                not stat.S_ISDIR(child_metadata.st_mode)
                or not stat.S_ISDIR(current_metadata.st_mode)
                or expected_identity != child_identity
                or child_identity != current_identity
            ):
                os.close(child)
                raise KintsugiError(
                    code,
                    relative,
                    "path component changed during descriptor-relative traversal",
                )
            os.close(descriptor)
            descriptor = child

        leaf = parts[-1]
        metadata = _exact_component_metadata(
            descriptor,
            leaf,
            code=code,
            relative=relative,
        )
        yield descriptor, leaf, metadata
    except KintsugiError:
        raise
    except (OSError, UnicodeError) as exc:
        raise KintsugiError(
            code,
            relative,
            f"cannot inspect path safely: {exc.__class__.__name__}",
        ) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _read_regular_no_symlinks(
    root: Path,
    relative: str,
    *,
    code: str = "KIN-E-SCOPE",
    require_single_link: bool = False,
) -> bytes:
    descriptor: int | None = None
    try:
        with _open_repo_parent_fd(root, relative, code=code) as (
            parent_descriptor,
            leaf,
            before,
        ):
            if not stat.S_ISREG(before.st_mode):
                raise KintsugiError(code, relative, "path is not an ordinary file")
            descriptor = os.open(
                leaf,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=parent_descriptor,
            )
            after = os.fstat(descriptor)
            if (
                not stat.S_ISREG(after.st_mode)
                or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
            ):
                raise KintsugiError(code, relative, "path changed during safe read")
            if require_single_link and (
                before.st_nlink != 1 or after.st_nlink != 1
            ):
                raise KintsugiError(code, relative, "path has a hard-link alias")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            current = os.stat(
                leaf,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(current.st_mode)
                or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)
            ):
                raise KintsugiError(code, relative, "path changed during safe read")
            if require_single_link and current.st_nlink != 1:
                raise KintsugiError(code, relative, "path has a hard-link alias")
            return b"".join(chunks)
    except KintsugiError:
        raise
    except OSError as exc:
        raise KintsugiError(
            code, relative, f"cannot read path safely: {exc.__class__.__name__}"
        ) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _lexical_entry_exists(root: Path, relative: str, *, code: str) -> bool:
    try:
        _decode_git_path(relative.encode("utf-8", errors="strict"))
        current = root.resolve(strict=True)
        parts = relative.split("/")
        for position, part in enumerate(parts):
            current = current / part
            try:
                metadata = os.lstat(current)
            except FileNotFoundError:
                return False
            if position < len(parts) - 1 and not stat.S_ISDIR(metadata.st_mode):
                raise KintsugiError(
                    code,
                    relative,
                    "path has a non-directory or symlinked parent",
                )
        return True
    except KintsugiError:
        raise
    except (OSError, UnicodeError) as exc:
        raise KintsugiError(
            code, relative, f"cannot inspect lexical path: {exc.__class__.__name__}"
        ) from None


def _hash_regular_or_symlink_with_mode(
    root: Path, relative: str
) -> tuple[FileRecord, int]:
    descriptor: int | None = None
    try:
        with _open_repo_parent_fd(
            root,
            relative,
            code="KIN-E-SCOPE",
        ) as (parent_descriptor, leaf, before):
            if stat.S_ISLNK(before.st_mode):
                target = os.readlink(leaf, dir_fd=parent_descriptor)
                after = os.stat(
                    leaf,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                if (
                    not stat.S_ISLNK(after.st_mode)
                    or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
                ):
                    raise KintsugiError(
                        "KIN-E-SCOPE",
                        relative,
                        "symlink changed during safe hash",
                    )
                return (
                    FileRecord(
                        relative,
                        "SYMLINK",
                        raw_hash(os.fsencode(target)),
                    ),
                    after.st_mode,
                )
            if not stat.S_ISREG(before.st_mode):
                raise KintsugiError(
                    "KIN-E-SCOPE",
                    relative,
                    "path is not a regular file or symlink",
                )
            descriptor = os.open(
                leaf,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
                dir_fd=parent_descriptor,
            )
            after = os.fstat(descriptor)
            if (
                not stat.S_ISREG(after.st_mode)
                or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
                or before.st_mode != after.st_mode
            ):
                raise KintsugiError(
                    "KIN-E-SCOPE",
                    relative,
                    "file changed during safe hash",
                )
            chunks: list[bytes] = []
            while True:
                chunk = os.read(descriptor, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            current = os.stat(
                leaf,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                not stat.S_ISREG(current.st_mode)
                or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino)
                or after.st_mode != current.st_mode
            ):
                raise KintsugiError(
                    "KIN-E-SCOPE",
                    relative,
                    "path changed during safe hash",
                )
            return (
                FileRecord(relative, "FILE", raw_hash(b"".join(chunks))),
                current.st_mode,
            )
    except KintsugiError:
        raise
    except (OSError, UnicodeError) as exc:
        raise KintsugiError(
            "KIN-E-SCOPE",
            relative,
            f"cannot hash path safely: {exc.__class__.__name__}",
        ) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _hash_regular_or_symlink(root: Path, relative: str) -> FileRecord:
    return _hash_regular_or_symlink_with_mode(root, relative)[0]


def _index_record(root: Path, relative: str) -> FileRecord | None:
    """Return the stage-zero index bytes for one path, or None for deletion.

    The caller already learned the path from a NUL-delimited Git diff.  Reading
    the index object itself prevents a staged payload from differing from the
    worktree payload that is frozen for review.
    """
    _decode_git_path(relative.encode("utf-8", errors="strict"))
    tokens = _run_git_z(root, ("ls-files", "--stage", "-z", "--", relative))
    if not tokens:
        return None
    if len(tokens) != 1:
        raise KintsugiError(
            "KIN-E-SCOPE", relative, "index path has multiple conflict stages"
        )
    try:
        header, raw_path = tokens[0].split(b"\t", 1)
        mode, object_id, stage = header.decode("ascii", errors="strict").split(" ")
    except (ValueError, UnicodeDecodeError):
        raise KintsugiError(
            "KIN-E-SCOPE", relative, "index record is malformed"
        ) from None
    if (
        _decode_git_path(raw_path) != relative
        or stage != "0"
        or mode not in {"100644", "100755", "120000"}
        or len(object_id) != 40
        or any(character not in "0123456789abcdef" for character in object_id)
    ):
        raise KintsugiError(
            "KIN-E-SCOPE", relative, "index record is unsupported"
        )
    payload = _run_git(root, ("cat-file", "blob", object_id))
    return FileRecord(
        relative,
        "SYMLINK" if mode == "120000" else "FILE",
        raw_hash(payload),
    )


def _snapshot_untracked(root: Path) -> tuple[tuple[FileRecord, ...], tuple[str, ...]]:
    paths = tuple(_decode_git_path(value) for value in _run_git_z(
        root, ("ls-files", "--others", "-z", "--")
    ))
    snapshots = tuple(
        _hash_regular_or_symlink_with_mode(root, path) for path in paths
    )
    records = tuple(sorted(record for record, _ in snapshots))
    executable_paths = tuple(sorted(
        record.path
        for record, mode in snapshots
        if record.kind == "FILE" and mode & 0o111
    ))
    return records, executable_paths


def _base_blob_records(root: Path, commit: str) -> tuple[FileRecord, ...]:
    resolved = _resolve_commit(root, commit)
    tokens = _run_git_z(
        root, ("ls-tree", "-r", "-z", "--full-tree", resolved, "--")
    )
    tree: list[tuple[str, str, str]] = []
    for token in tokens:
        try:
            header, raw_path = token.split(b"\t", 1)
            mode, object_type, object_id = header.decode("ascii", errors="strict").split(" ")
        except (ValueError, UnicodeDecodeError):
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git tree record is malformed") from None
        if object_type != "blob" or mode not in {"100644", "100755", "120000"}:
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git tree contains an unsupported entry")
        tree.append((_decode_git_path(raw_path), mode, object_id))

    request = b"".join(object_id.encode("ascii") + b"\n" for _, _, object_id in tree)
    response = _run_git_input(root, ("cat-file", "--batch"), request)
    offset = 0
    blobs: dict[str, bytes] = {}
    for _, _, requested_id in tree:
        line_end = response.find(b"\n", offset)
        if line_end < 0:
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git batch response is truncated")
        try:
            object_id, object_type, size_text = response[offset:line_end].decode(
                "ascii", errors="strict"
            ).split(" ")
            size = int(size_text)
        except (ValueError, UnicodeDecodeError):
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git batch header is malformed") from None
        if object_type != "blob" or object_id != requested_id or size < 0:
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git batch object does not match its request")
        start = line_end + 1
        end = start + size
        if end >= len(response) or response[end:end + 1] != b"\n":
            raise KintsugiError("KIN-E-CONCURRENT", "git", "Git batch payload is truncated")
        blobs[requested_id] = response[start:end]
        offset = end + 1
    if offset != len(response):
        raise KintsugiError("KIN-E-CONCURRENT", "git", "Git batch response has trailing bytes")

    return tuple(sorted(
        FileRecord(path, "SYMLINK" if mode == "120000" else "FILE", raw_hash(blobs[object_id]))
        for path, mode, object_id in tree
    ))


def _list_worktrees(root: Path) -> tuple[WorktreeRecord, ...]:
    tokens = _run_git_z(root, ("worktree", "list", "--porcelain", "-z"))
    records: list[WorktreeRecord] = []
    fields: dict[str, str] = {}

    def finish() -> None:
        if not fields:
            return
        if "worktree" not in fields or "HEAD" not in fields:
            raise KintsugiError("KIN-E-CONCURRENT", "git", "worktree record is incomplete")
        try:
            worktree_root = Path(fields["worktree"]).resolve(strict=True)
        except OSError as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "git", f"registered worktree is unavailable: {exc.__class__.__name__}"
            ) from None
        head = fields["HEAD"]
        if len(head) != 40 or any(character not in "0123456789abcdef" for character in head):
            raise KintsugiError("KIN-E-CONCURRENT", "git", "worktree HEAD is not a full SHA-1")
        branch = fields.get("branch")
        if branch is not None:
            prefix = "refs/heads/"
            if not branch.startswith(prefix):
                raise KintsugiError("KIN-E-CONCURRENT", "git", "worktree branch is not local")
            branch = branch[len(prefix):]
        records.append(WorktreeRecord(worktree_root, head, branch))

    for token in tokens:
        if token == b"":
            finish()
            fields = {}
            continue
        try:
            text = token.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            raise KintsugiError("KIN-E-CONCURRENT", "git", "worktree metadata is not UTF-8") from None
        key, separator, value = text.partition(" ")
        if not separator:
            if text not in {"bare", "detached"}:
                raise KintsugiError("KIN-E-CONCURRENT", "git", "worktree metadata is malformed")
            key, value = text, ""
        if key in fields:
            raise KintsugiError("KIN-E-CONCURRENT", "git", "worktree metadata is malformed")
        fields[key] = value
    finish()
    roots = [record.root for record in records]
    if len(roots) != len(set(roots)):
        raise KintsugiError("KIN-E-CONCURRENT", "git", "registered worktree roots are duplicated")
    return tuple(sorted(records, key=lambda record: record.root.as_posix()))


def _snapshot_protected_tree(
    root: Path, protected_paths: tuple[str, ...]
) -> tuple[FileRecord, ...]:
    records: list[FileRecord] = []
    directory_flag = getattr(os, "O_DIRECTORY", 0)
    nofollow_flag = getattr(os, "O_NOFOLLOW", 0)
    if directory_flag == 0 or nofollow_flag == 0:
        raise KintsugiError(
            "KIN-E-PROTECTED",
            "protectedPaths",
            "safe descriptor-relative protected traversal is unavailable",
        )

    def identity(metadata: os.stat_result) -> tuple[int, int]:
        return metadata.st_dev, metadata.st_ino

    def entries_at(
        directory_descriptor: int,
        relative: str,
    ) -> list[tuple[str, os.stat_result]]:
        with os.scandir(directory_descriptor) as iterator:
            entries = sorted(
                (
                    entry.name,
                    entry.stat(follow_symlinks=False),
                )
                for entry in iterator
            )
        names = [name for name, _ in entries]
        if len({name.casefold() for name in names}) != len(names):
            raise KintsugiError(
                "KIN-E-PROTECTED",
                relative,
                "protected directory contains a case-aliased entry",
            )
        return entries

    def entry_signature(
        entry: tuple[str, os.stat_result],
    ) -> tuple[str, int, int, int, int, int, int, int]:
        name, metadata = entry
        return (
            name,
            metadata.st_dev,
            metadata.st_ino,
            metadata.st_mode,
            metadata.st_nlink,
            metadata.st_size,
            metadata.st_mtime_ns,
            metadata.st_ctime_ns,
        )

    def visit(directory_descriptor: int, relative: str) -> None:
        before_directory = os.fstat(directory_descriptor)
        if not stat.S_ISDIR(before_directory.st_mode):
            raise KintsugiError(
                "KIN-E-PROTECTED",
                relative,
                "protected traversal descriptor is not a directory",
            )
        initial_entries = entries_at(directory_descriptor, relative)
        for name, before in initial_entries:
            child_relative = f"{relative}/{name}"
            _decode_git_path(child_relative.encode("utf-8", errors="strict"))
            if stat.S_ISLNK(before.st_mode):
                if before.st_nlink != 1:
                    raise KintsugiError(
                        "KIN-E-PROTECTED",
                        child_relative,
                        "protected symlink has a hard-link alias",
                    )
                target = os.readlink(name, dir_fd=directory_descriptor)
                current = os.stat(
                    name,
                    dir_fd=directory_descriptor,
                    follow_symlinks=False,
                )
                if not stat.S_ISLNK(current.st_mode) or identity(before) != identity(current):
                    raise KintsugiError(
                        "KIN-E-PROTECTED",
                        child_relative,
                        "protected symlink changed during snapshot",
                    )
                records.append(FileRecord(
                    child_relative,
                    "SYMLINK",
                    raw_hash(os.fsencode(target)),
                ))
                continue
            if stat.S_ISREG(before.st_mode):
                descriptor: int | None = None
                try:
                    descriptor = os.open(
                        name,
                        os.O_RDONLY | nofollow_flag,
                        dir_fd=directory_descriptor,
                    )
                    opened = os.fstat(descriptor)
                    if (
                        not stat.S_ISREG(opened.st_mode)
                        or identity(before) != identity(opened)
                        or before.st_nlink != 1
                        or opened.st_nlink != 1
                    ):
                        raise KintsugiError(
                            "KIN-E-PROTECTED",
                            child_relative,
                            "protected file changed or has a hard-link alias",
                        )
                    chunks: list[bytes] = []
                    while True:
                        chunk = os.read(descriptor, 1024 * 1024)
                        if not chunk:
                            break
                        chunks.append(chunk)
                    current = os.stat(
                        name,
                        dir_fd=directory_descriptor,
                        follow_symlinks=False,
                    )
                    if (
                        not stat.S_ISREG(current.st_mode)
                        or identity(opened) != identity(current)
                        or current.st_nlink != 1
                    ):
                        raise KintsugiError(
                            "KIN-E-PROTECTED",
                            child_relative,
                            "protected file changed during snapshot",
                        )
                    records.append(FileRecord(
                        child_relative,
                        "FILE",
                        raw_hash(b"".join(chunks)),
                    ))
                finally:
                    if descriptor is not None:
                        os.close(descriptor)
                continue
            if stat.S_ISDIR(before.st_mode):
                child_descriptor: int | None = None
                try:
                    child_descriptor = os.open(
                        name,
                        os.O_RDONLY | directory_flag | nofollow_flag,
                        dir_fd=directory_descriptor,
                    )
                    opened = os.fstat(child_descriptor)
                    current = os.stat(
                        name,
                        dir_fd=directory_descriptor,
                        follow_symlinks=False,
                    )
                    if (
                        not stat.S_ISDIR(opened.st_mode)
                        or not stat.S_ISDIR(current.st_mode)
                        or identity(before) != identity(opened)
                        or identity(opened) != identity(current)
                    ):
                        raise KintsugiError(
                            "KIN-E-PROTECTED",
                            child_relative,
                            "protected directory changed during traversal",
                        )
                    visit(child_descriptor, child_relative)
                    current = os.stat(
                        name,
                        dir_fd=directory_descriptor,
                        follow_symlinks=False,
                    )
                    if not stat.S_ISDIR(current.st_mode) or identity(opened) != identity(current):
                        raise KintsugiError(
                            "KIN-E-PROTECTED",
                            child_relative,
                            "protected directory changed during traversal",
                        )
                finally:
                    if child_descriptor is not None:
                        os.close(child_descriptor)
                continue
            raise KintsugiError(
                "KIN-E-PROTECTED",
                child_relative,
                "protected tree contains a special file",
            )

        final_entries = entries_at(directory_descriptor, relative)
        if (
            [entry_signature(entry) for entry in final_entries]
            != [entry_signature(entry) for entry in initial_entries]
        ):
            raise KintsugiError(
                "KIN-E-PROTECTED",
                relative,
                "protected directory membership or entry identity changed during snapshot",
            )
        after_directory = os.fstat(directory_descriptor)
        if identity(before_directory) != identity(after_directory):
            raise KintsugiError(
                "KIN-E-PROTECTED",
                relative,
                "protected directory descriptor changed during snapshot",
            )

    for relative in sorted(set(protected_paths)):
        _decode_git_path(relative.encode("utf-8", errors="strict"))
        protected_descriptor: int | None = None
        with _open_repo_parent_fd(
            root,
            relative,
            code="KIN-E-PROTECTED",
        ) as (parent_descriptor, leaf, before):
            if not stat.S_ISDIR(before.st_mode):
                raise KintsugiError(
                    "KIN-E-PROTECTED",
                    relative,
                    "protected root must be an ordinary directory",
                )
            try:
                protected_descriptor = os.open(
                    leaf,
                    os.O_RDONLY | directory_flag | nofollow_flag,
                    dir_fd=parent_descriptor,
                )
                opened = os.fstat(protected_descriptor)
                current = os.stat(
                    leaf,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                if (
                    not stat.S_ISDIR(opened.st_mode)
                    or not stat.S_ISDIR(current.st_mode)
                    or identity(before) != identity(opened)
                    or identity(opened) != identity(current)
                ):
                    raise KintsugiError(
                        "KIN-E-PROTECTED",
                        relative,
                        "protected root changed during descriptor open",
                    )
                visit(protected_descriptor, relative)
                current = os.stat(
                    leaf,
                    dir_fd=parent_descriptor,
                    follow_symlinks=False,
                )
                if not stat.S_ISDIR(current.st_mode) or identity(opened) != identity(current):
                    raise KintsugiError(
                        "KIN-E-PROTECTED",
                        relative,
                        "protected root changed during snapshot",
                    )
            finally:
                if protected_descriptor is not None:
                    os.close(protected_descriptor)
    return tuple(sorted(records))


def _canonical_attempt_number(attempt_id: str, phase: str) -> int:
    if not canonical_attempt(attempt_id, phase):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "attempt", "attempt ID is not canonical for its phase"
        )
    number = int(attempt_id.rsplit("-", 1)[1])
    if attempt_id != f"RVA-{phase}-{number:03d}":
        raise KintsugiError(
            "KIN-E-CONCURRENT", "attempt", "attempt ID does not round-trip canonically"
        )
    return number


_TARGET_ROOT = "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts"
_REVIEW_ROOT = "11_UPLINK/50_AUDITS_AND_EXECUTIONS/KINTSUGI_REVIEW_ATTEMPTS"
_TARGET_PREFIX = _TARGET_ROOT + "/"
_REVIEW_PREFIX = _REVIEW_ROOT + "/"
_CANONICAL_CORE_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
_IMMUTABLE_ATTEMPT_FIELDS = (
    "id",
    "phase",
    "receiptId",
    "supersedesAttemptId",
    "reviewSubjectDigest",
    "reviewTargetPath",
    "logicReviewPath",
    "btjReviewPath",
    "validationBundlePath",
)


def _attempt_id_from_path(path: str) -> str | None:
    if path in {_TARGET_ROOT, _REVIEW_ROOT}:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            path,
            "attempt namespace root cannot be a file",
        )
    candidate: str | None = None
    if path.startswith(_TARGET_PREFIX):
        remainder = path[len(_TARGET_PREFIX):]
        candidate = remainder.split("/", 1)[0]
    elif path.startswith(_REVIEW_PREFIX):
        remainder = path[len(_REVIEW_PREFIX):]
        candidate = remainder.split("_", 1)[0]
    if candidate is None:
        return None
    parts = candidate.split("-")
    phase = parts[1] if len(parts) == 3 else ""
    _canonical_attempt_number(candidate, phase)
    if path not in attempt_paths(candidate):
        raise KintsugiError(
            "KIN-E-CONCURRENT", path, "attempt artifact path is not one of the four derived roles"
        )
    return candidate


def _reachable_attempt_ids(root: Path) -> tuple[str, ...]:
    result: set[str] = set()
    for raw_path in _run_git_z(
        root, ("log", "--all", "--name-only", "-z", "--format=", "--")
    ):
        attempt_id = _attempt_id_from_path(_decode_git_path(raw_path))
        if attempt_id is not None:
            result.add(attempt_id)
    return tuple(sorted(result, key=lambda value: (value.split("-")[1], _canonical_attempt_number(value, value.split("-")[1]))))


def _canonical_namespace_directory(root: Path, relative: str) -> Path | None:
    current = root.resolve(strict=True)
    for position, part in enumerate(relative.split("/")):
        try:
            with os.scandir(current) as iterator:
                matches = [
                    entry for entry in iterator
                    if entry.name.casefold() == part.casefold()
                ]
        except OSError as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                relative,
                f"cannot inspect attempt namespace: {exc.__class__.__name__}",
            ) from None
        exact = [entry for entry in matches if entry.name == part]
        aliases = [entry for entry in matches if entry.name != part]
        if aliases:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                relative,
                "attempt namespace has a non-canonical case alias",
            )
        if not exact:
            return None
        if len(exact) != 1:
            raise KintsugiError(
                "KIN-E-CONCURRENT", relative, "attempt namespace is ambiguous"
            )
        entry = exact[0]
        if entry.is_symlink() or not entry.is_dir(follow_symlinks=False):
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                relative,
                "attempt namespace path is not an ordinary directory",
            )
        current = Path(entry.path)
        if position == len(relative.split("/")) - 1:
            return current
    return current


def _filesystem_attempt_state(
    root: Path,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    attempt_ids: set[str] = set()
    obstructions: set[str] = set()

    target_root = _canonical_namespace_directory(root, _TARGET_ROOT)
    if target_root is not None:
        try:
            with os.scandir(target_root) as iterator:
                attempt_entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                _TARGET_ROOT,
                f"cannot inspect attempt target namespace: {exc.__class__.__name__}",
            ) from None
        for entry in attempt_entries:
            attempt_id = entry.name
            parts = attempt_id.split("-")
            phase = parts[1] if len(parts) == 3 else ""
            _canonical_attempt_number(attempt_id, phase)
            attempt_ids.add(attempt_id)
            attempt_relative = f"{_TARGET_ROOT}/{attempt_id}"
            if entry.is_symlink() or not entry.is_dir(follow_symlinks=False):
                obstructions.add(attempt_relative)
                continue
            try:
                with os.scandir(entry.path) as iterator:
                    role_entries = sorted(iterator, key=lambda child: child.name)
            except OSError as exc:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    attempt_relative,
                    f"cannot inspect attempt role directory: {exc.__class__.__name__}",
                ) from None
            for child in role_entries:
                role_relative = f"{attempt_relative}/{child.name}"
                parsed = _attempt_id_from_path(role_relative)
                if parsed != attempt_id:
                    raise KintsugiError(
                        "KIN-E-CONCURRENT",
                        role_relative,
                        "attempt role belongs to another attempt",
                    )
                if child.is_symlink() or not child.is_file(follow_symlinks=False):
                    obstructions.add(role_relative)

    review_root = _canonical_namespace_directory(root, _REVIEW_ROOT)
    if review_root is not None:
        try:
            with os.scandir(review_root) as iterator:
                review_entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                _REVIEW_ROOT,
                f"cannot inspect attempt review namespace: {exc.__class__.__name__}",
            ) from None
        for entry in review_entries:
            relative = f"{_REVIEW_ROOT}/{entry.name}"
            attempt_id = _attempt_id_from_path(relative)
            if attempt_id is None:
                raise KintsugiError(
                    "KIN-E-CONCURRENT", relative, "attempt review role is invalid"
                )
            attempt_ids.add(attempt_id)
            if entry.is_symlink() or not entry.is_file(follow_symlinks=False):
                obstructions.add(relative)

    return (
        tuple(sorted(
            attempt_ids,
            key=lambda value: (
                value.split("-")[1],
                _canonical_attempt_number(value, value.split("-")[1]),
            ),
        )),
        tuple(sorted(obstructions)),
    )


def _git_attempt_paths(root: Path) -> tuple[str, ...]:
    paths = tuple(sorted(
        _decode_git_path(raw_path)
        for raw_path in _run_git_z(
            root,
            (
                "ls-files",
                "--cached",
                "--others",
                "-z",
                "--",
                _TARGET_ROOT,
                _REVIEW_ROOT,
            ),
        )
    ))
    for relative in paths:
        if _attempt_id_from_path(relative) is None:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                relative,
                "attempt namespace path has no canonical derived role",
            )
    return paths


def _worktree_attempt_paths(root: Path) -> tuple[str, ...]:
    _, obstructions = _filesystem_attempt_state(root)
    if obstructions:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            obstructions[0],
            "attempt artifact role is obstructed by a directory or special file",
        )
    return _git_attempt_paths(root)


def _reservation_records(common_dir: Path) -> tuple[dict[str, Any], ...]:
    directory = common_dir / "kintsugi-attempt-reservations"
    if not directory.exists():
        return ()
    if directory.is_symlink() or not directory.is_dir():
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservations", "reservation directory is not an ordinary directory"
        )
    try:
        with os.scandir(directory) as iterator:
            entries = sorted(iterator, key=lambda entry: entry.name)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservations", f"cannot enumerate reservations: {exc.__class__.__name__}"
        ) from None
    records: list[dict[str, Any]] = []
    expected_keys = {"id", "phase", "receiptId", "expectedHead", "expectedCoreSha256"}
    for entry in entries:
        if entry.is_symlink() or not entry.is_file(follow_symlinks=False):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation entry is not a regular file"
            )
        if not entry.name.endswith(".json"):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation filename is not canonical"
            )
        try:
            payload = Path(entry.path).read_bytes()
            value = json.loads(payload.decode("utf-8", errors="strict"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", f"reservation is unreadable: {exc.__class__.__name__}"
            ) from None
        if not isinstance(value, dict) or set(value) != expected_keys:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation shape is malformed"
            )
        try:
            canonical_payload = canonical_json_bytes(value)
        except KintsugiError:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation bytes are not canonical JSON"
            ) from None
        if payload != canonical_payload:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation bytes are not canonical JSON"
            )
        attempt_id = value.get("id")
        phase = value.get("phase")
        if not isinstance(attempt_id, str) or not isinstance(phase, str):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation identity is malformed"
            )
        _canonical_attempt_number(attempt_id, phase)
        if entry.name != f"{attempt_id}.json":
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation filename and ID disagree"
            )
        identity = RECEIPT_IDENTITIES.get(phase)
        if identity is None or value.get("receiptId") != identity[0]:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation receipt is not canonical"
            )
        head = value.get("expectedHead")
        core_hash = value.get("expectedCoreSha256")
        if (
            not isinstance(head, str)
            or len(head) != 40
            or any(character not in "0123456789abcdef" for character in head)
            or not isinstance(core_hash, str)
            or not core_hash.startswith("sha256:")
            or len(core_hash) != 71
            or any(character not in "0123456789abcdef" for character in core_hash[7:])
        ):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "reservations", "reservation expectations are malformed"
            )
        records.append(value)
    return tuple(sorted(
        records,
        key=lambda record: (
            str(record["phase"]),
            _canonical_attempt_number(str(record["id"]), str(record["phase"])),
        ),
    ))


def _used_attempt_ids(
    root: Path,
    core: dict[str, object],
    phase: str,
    *,
    ignore_reservation_id: str | None = None,
) -> tuple[str, ...]:
    if phase not in RECEIPT_IDENTITIES:
        raise KintsugiError("KIN-E-CONCURRENT", "attempt", "attempt phase is invalid")
    if ignore_reservation_id is not None:
        _canonical_attempt_number(ignore_reservation_id, phase)
    common_dir = resolve_git_common_dir(root)
    used: set[str] = set()

    attempts = core.get("reviewAttempts") if isinstance(core, dict) else None
    if not isinstance(attempts, list):
        raise KintsugiError("KIN-E-CONCURRENT", "attempt", "reviewAttempts must be a list")
    for attempt in attempts:
        if not isinstance(attempt, dict):
            raise KintsugiError("KIN-E-CONCURRENT", "attempt", "review attempt is malformed")
        attempt_id = attempt.get("id")
        attempt_phase = attempt.get("phase")
        if not isinstance(attempt_id, str) or not isinstance(attempt_phase, str):
            raise KintsugiError("KIN-E-CONCURRENT", "attempt", "review attempt identity is malformed")
        _canonical_attempt_number(attempt_id, attempt_phase)
        expected_paths = attempt_paths(attempt_id)
        actual_paths = tuple(attempt.get(field) for field in (
            "reviewTargetPath", "logicReviewPath", "btjReviewPath", "validationBundlePath"
        ))
        if actual_paths != expected_paths:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "attempt", "review attempt paths are not exactly derived"
            )
        if attempt_phase == phase:
            used.add(attempt_id)

    for worktree in _list_worktrees(root):
        filesystem_ids, _ = _filesystem_attempt_state(worktree.root)
        for attempt_id in filesystem_ids:
            if attempt_id.split("-")[1] == phase:
                used.add(attempt_id)
        for relative in _git_attempt_paths(worktree.root):
            attempt_id = _attempt_id_from_path(relative)
            if attempt_id is not None and attempt_id.split("-")[1] == phase:
                used.add(attempt_id)

    for attempt_id in _reachable_attempt_ids(root):
        if attempt_id.split("-")[1] == phase:
            used.add(attempt_id)
    for attempt_id, historical in _reachable_core_attempt_history(
        root, _CANONICAL_CORE_PATH
    ).items():
        if historical.phase == phase:
            used.add(attempt_id)
    for reservation in _reservation_records(common_dir):
        if (
            reservation["phase"] == phase
            and reservation["id"] != ignore_reservation_id
        ):
            used.add(str(reservation["id"]))
    return tuple(sorted(used, key=lambda value: _canonical_attempt_number(value, phase)))


def _unique_chain_leaf(
    attempts: list[dict[str, Any]], *, context: str
) -> dict[str, Any] | None:
    if not attempts:
        return None
    by_id: dict[str, dict[str, Any]] = {}
    for attempt in attempts:
        attempt_id = attempt.get("id")
        if not isinstance(attempt_id, str) or attempt_id in by_id:
            raise KintsugiError(
                "KIN-E-CONCURRENT", context, "attempt chain identity is malformed"
            )
        by_id[attempt_id] = attempt

    roots: list[str] = []
    children: dict[str, list[str]] = {attempt_id: [] for attempt_id in by_id}
    for attempt_id, attempt in by_id.items():
        predecessor_id = attempt.get("supersedesAttemptId")
        if predecessor_id is None:
            roots.append(attempt_id)
            continue
        if not isinstance(predecessor_id, str) or predecessor_id not in by_id:
            raise KintsugiError(
                "KIN-E-CONCURRENT", context, "attempt chain predecessor is absent"
            )
        children[predecessor_id].append(attempt_id)

    if len(roots) != 1 or any(len(successors) > 1 for successors in children.values()):
        raise KintsugiError(
            "KIN-E-CONCURRENT", context, "attempt chain lacks one unique root-to-leaf path"
        )

    ordered: list[str] = []
    seen: set[str] = set()
    current: str | None = roots[0]
    while current is not None:
        if current in seen:
            raise KintsugiError(
                "KIN-E-CONCURRENT", context, "attempt chain contains a cycle"
            )
        seen.add(current)
        ordered.append(current)
        successors = children[current]
        current = successors[0] if successors else None
    if len(ordered) != len(by_id):
        raise KintsugiError(
            "KIN-E-CONCURRENT", context, "attempt chain is disconnected or cyclic"
        )
    if tuple(attempt.get("id") for attempt in attempts) != tuple(ordered):
        raise KintsugiError(
            "KIN-E-CONCURRENT", context, "attempt chain is not stored root-to-leaf"
        )
    return by_id[ordered[-1]]


def _plan_next_attempt(
    root: Path,
    core: dict[str, object],
    phase: str,
    receipt_id: str,
    *,
    ignore_reservation_id: str | None = None,
) -> AttemptPlan:
    identity = RECEIPT_IDENTITIES.get(phase)
    if identity is None or receipt_id != identity[0]:
        raise KintsugiError("KIN-E-CONCURRENT", "attempt", "attempt receipt is not canonical")
    attempts = [
        attempt for attempt in core.get("reviewAttempts", [])
        if isinstance(attempt, dict)
        and attempt.get("phase") == phase
        and attempt.get("receiptId") == receipt_id
    ]
    predecessor = _unique_chain_leaf(attempts, context="attempt")
    if predecessor is not None and predecessor.get("status") not in {"FAILED", "ABANDONED"}:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "attempt", "successor requires a FAILED or ABANDONED predecessor"
        )
    used = set(
        _used_attempt_ids(
            root,
            core,
            phase,
            ignore_reservation_id=ignore_reservation_id,
        )
    )
    number = 1
    while f"RVA-{phase}-{number:03d}" in used:
        number += 1
    attempt_id = f"RVA-{phase}-{number:03d}"
    return AttemptPlan(
        id=attempt_id,
        phase=phase,
        receipt_id=receipt_id,
        predecessor_id=(str(predecessor["id"]) if predecessor is not None else None),
        paths=attempt_paths(attempt_id),
    )


def _fsync_directory(directory: Path, context: str) -> None:
    try:
        descriptor = os.open(directory, os.O_RDONLY)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            context,
            f"cannot open directory for durability: {exc.__class__.__name__}",
        ) from None
    try:
        os.fsync(descriptor)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            context,
            f"cannot persist directory entry: {exc.__class__.__name__}",
        ) from None
    finally:
        os.close(descriptor)


@contextmanager
def _transition_lock(common_dir: Path) -> Iterator[Path]:
    try:
        resolved = common_dir.resolve(strict=True)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "lock", f"Git common directory is unavailable: {exc.__class__.__name__}"
        ) from None
    lock_path = resolved / ".kintsugi-transition.lock"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except FileExistsError:
        raise KintsugiError("KIN-E-CONCURRENT", "lock", "transition lock already exists") from None
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "lock", f"cannot create transition lock: {exc.__class__.__name__}"
        ) from None
    created_stat = os.fstat(descriptor)
    created_identity = (created_stat.st_dev, created_stat.st_ino)
    try:
        try:
            payload = b"KINTSUGI-TRANSITION-LOCK-V1\n"
            written = 0
            while written < len(payload):
                count = os.write(descriptor, payload[written:])
                if count <= 0:
                    raise OSError("zero-byte lock write")
                written += count
            os.fsync(descriptor)
            os.close(descriptor)
            descriptor = -1
            _fsync_directory(resolved, "lock")
        except OSError as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                "lock",
                f"cannot persist transition lock: {exc.__class__.__name__}",
            ) from None
        yield lock_path
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            current_stat = lock_path.lstat()
        except FileNotFoundError:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "lock", "transition lock disappeared while held"
            ) from None
        if (current_stat.st_dev, current_stat.st_ino) != created_identity:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "lock", "transition lock was replaced while held"
            )
        try:
            lock_path.unlink()
            _fsync_directory(resolved, "lock")
        except OSError as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "lock", f"cannot remove transition lock: {exc.__class__.__name__}"
            ) from None


def _reserve_attempt_id(
    common_dir: Path,
    plan: AttemptPlan,
    expected_head: str,
    expected_core_sha256: str,
) -> Path:
    lock_path = common_dir / ".kintsugi-transition.lock"
    if lock_path.is_symlink() or not lock_path.is_file():
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", "attempt reservation requires the shared lock"
        )
    _canonical_attempt_number(plan.id, plan.phase)
    if plan.paths != attempt_paths(plan.id):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", "attempt plan paths are not exactly derived"
        )
    identity = RECEIPT_IDENTITIES.get(plan.phase)
    if identity is None or plan.receipt_id != identity[0]:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", "attempt plan receipt is not canonical"
        )
    if (
        len(expected_head) != 40
        or any(character not in "0123456789abcdef" for character in expected_head)
        or len(expected_core_sha256) != 71
        or not expected_core_sha256.startswith("sha256:")
        or any(character not in "0123456789abcdef" for character in expected_core_sha256[7:])
    ):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", "reservation expectations are malformed"
        )
    directory = common_dir / "kintsugi-attempt-reservations"
    if directory.exists() and (directory.is_symlink() or not directory.is_dir()):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", "reservation directory is not ordinary"
        )
    directory_existed = directory.exists()
    try:
        directory.mkdir(mode=0o700, exist_ok=True)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", f"cannot create reservation directory: {exc.__class__.__name__}"
        ) from None
    if not directory_existed:
        _fsync_directory(common_dir, "reservation")
    value = {
        "id": plan.id,
        "phase": plan.phase,
        "receiptId": plan.receipt_id,
        "expectedHead": expected_head,
        "expectedCoreSha256": expected_core_sha256,
    }
    payload = canonical_json_bytes(value)
    path = directory / f"{plan.id}.json"
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", "attempt ID is already reserved"
        ) from None
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "reservation", f"cannot create reservation: {exc.__class__.__name__}"
        ) from None
    try:
        try:
            written = 0
            while written < len(payload):
                count = os.write(descriptor, payload[written:])
                if count <= 0:
                    raise OSError("zero-byte reservation write")
                written += count
            os.fsync(descriptor)
        except OSError as exc:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                "reservation",
                f"cannot persist reservation: {exc.__class__.__name__}",
            ) from None
    finally:
        os.close(descriptor)
    _fsync_directory(directory, "reservation")
    return path


def _check_head_core_cas(
    root: Path,
    core_relative: str,
    expected_head: str,
    expected_core_sha256: str,
) -> None:
    if _resolve_commit(root, "HEAD") != expected_head:
        raise KintsugiError("KIN-E-CONCURRENT", "cas", "HEAD changed from the caller expectation")
    try:
        core_bytes = _read_regular_no_symlinks(
            root,
            core_relative,
            code="KIN-E-CONCURRENT",
            require_single_link=True,
        )
    except KintsugiError:
        raise KintsugiError("KIN-E-CONCURRENT", "cas", "core path is unsafe") from None
    actual = raw_hash(core_bytes)
    if actual != expected_core_sha256:
        raise KintsugiError("KIN-E-CONCURRENT", "cas", "raw core hash changed from the caller expectation")


def _committed_regular_bytes(root: Path, relative: str) -> bytes:
    try:
        current = _read_regular_no_symlinks(
            root,
            relative,
            code="KIN-E-CONCURRENT",
        )
    except KintsugiError:
        raise
    committed = _run_git(root, ("show", f"HEAD:{relative}"))
    if current != committed:
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "predecessor artifact differs from the committed HEAD bytes"
        )
    return current


def _require_absent_at_head_and_worktree(root: Path, relative: str) -> None:
    if _lexical_entry_exists(root, relative, code="KIN-E-CONCURRENT"):
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "unrecorded predecessor closure artifact exists"
        )
    names = {
        _decode_git_path(value)
        for value in _run_git_z(
            root, ("ls-tree", "-r", "-z", "--name-only", "HEAD", "--")
        )
    }
    if relative in names:
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "unrecorded predecessor closure artifact is committed"
        )


def _reachable_history_graph(
    root: Path,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    replacement_refs = _run_git(
        root,
        ("for-each-ref", "--format=%(refname)", "refs/replace/"),
    )
    try:
        replacement_names = tuple(
            line
            for line in replacement_refs.decode("utf-8", errors="strict").splitlines()
            if line
        )
    except UnicodeDecodeError:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "history", "replacement reference names are not UTF-8"
        ) from None
    if replacement_names:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "history", "replacement references make history non-canonical"
        )
    common_dir = resolve_git_common_dir(root)
    if _lexical_entry_exists(common_dir, "info/grafts", code="KIN-E-CONCURRENT"):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "history", "legacy grafts make history non-canonical"
        )
    shallow = _run_git(root, ("rev-parse", "--is-shallow-repository"))
    if shallow != b"false\n":
        raise KintsugiError(
            "KIN-E-CONCURRENT", "history", "terminal history requires a complete repository"
        )
    payload = _run_git(
        root,
        (
            "rev-list",
            "--topo-order",
            "--reverse",
            "--parents",
            "--all",
            "HEAD",
        ),
    )
    try:
        lines = tuple(
            line.split()
            for line in payload.decode("ascii", errors="strict").splitlines()
            if line
        )
    except UnicodeDecodeError:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "history", "historical graph is not ASCII"
        ) from None
    if not lines:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "history", "repository has no reachable commits"
        )
    graph: list[tuple[str, tuple[str, ...]]] = []
    seen: set[str] = set()
    for values in lines:
        if not values:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "history", "historical graph line is empty"
            )
        for value in values:
            if len(value) != 40 or any(character not in "0123456789abcdef" for character in value):
                raise KintsugiError(
                    "KIN-E-CONCURRENT", "history", "historical graph ID is not a full SHA-1"
                )
        commit, parents = values[0], tuple(values[1:])
        if commit in seen or any(parent not in seen for parent in parents):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "history", "historical graph is not unique parent-first order"
            )
        seen.add(commit)
        graph.append((commit, parents))
    return tuple(graph)


def _regular_blob_at_commit(root: Path, commit: str, relative: str) -> bytes | None:
    try:
        decoded_relative = _decode_git_path(relative.encode("utf-8", errors="strict"))
    except (UnicodeEncodeError, KintsugiError):
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "historical artifact path is not repository-relative UTF-8"
        ) from None
    entries = _run_git_z(
        root,
        ("ls-tree", "-z", commit, "--", f":(literal){decoded_relative}"),
    )
    if not entries:
        return None
    if len(entries) != 1 or b"\t" not in entries[0]:
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "historical artifact tree entry is ambiguous"
        )
    metadata, raw_path = entries[0].split(b"\t", 1)
    if _decode_git_path(raw_path) != decoded_relative:
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "historical artifact tree entry changed path"
        )
    fields = metadata.split(b" ")
    if len(fields) != 3 or fields[0] != b"100644" or fields[1] != b"blob":
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "historical artifact is not an ordinary non-executable file"
        )
    try:
        object_id = fields[2].decode("ascii", errors="strict")
    except UnicodeDecodeError:
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "historical artifact object ID is not ASCII"
        ) from None
    if len(object_id) != 40 or any(character not in "0123456789abcdef" for character in object_id):
        raise KintsugiError(
            "KIN-E-CONCURRENT", relative, "historical artifact object ID is not a full SHA-1"
        )
    return _run_git(root, ("cat-file", "blob", object_id))


def _decode_canonical_history_core(
    payload: bytes,
    *,
    relative: str,
    commit: str,
) -> dict[str, Any]:
    def closed_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    def reject_constant(constant: str) -> None:
        raise ValueError(f"invalid constant: {constant}")

    try:
        text = payload.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=closed_object,
            parse_constant=reject_constant,
        )
        canonical = canonical_json_bytes(value)
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError, KintsugiError):
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            relative,
            f"historical core snapshot at {commit} is not strict canonical JSON",
        ) from None
    if not isinstance(value, dict) or payload != canonical:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            relative,
            f"historical core snapshot at {commit} is not a canonical object",
        )
    return value


def _historical_attempt_identity(
    attempt: dict[str, Any], *, context: str
) -> tuple[Any, ...]:
    attempt_id = attempt.get("id")
    phase = attempt.get("phase")
    receipt_id = attempt.get("receiptId")
    if not isinstance(attempt_id, str) or not isinstance(phase, str):
        raise KintsugiError(
            "KIN-E-CONCURRENT", context, "historical attempt identity is malformed"
        )
    _canonical_attempt_number(attempt_id, phase)
    receipt_identity = RECEIPT_IDENTITIES.get(phase)
    if receipt_identity is None or receipt_id != receipt_identity[0]:
        raise KintsugiError(
            "KIN-E-CONCURRENT", attempt_id, "historical attempt receipt is non-canonical"
        )
    predecessor_id = attempt.get("supersedesAttemptId")
    if predecessor_id is not None:
        if not isinstance(predecessor_id, str):
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                attempt_id,
                "historical attempt predecessor is malformed",
            )
        _canonical_attempt_number(predecessor_id, phase)
        if predecessor_id == attempt_id:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                attempt_id,
                "historical attempt cannot supersede itself",
            )
    if not isinstance(attempt.get("reviewSubjectDigest"), str):
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            attempt_id,
            "historical attempt subject digest is malformed",
        )
    expected_paths = attempt_paths(attempt_id)
    actual_paths = tuple(
        attempt.get(field)
        for field in (
            "reviewTargetPath",
            "logicReviewPath",
            "btjReviewPath",
            "validationBundlePath",
        )
    )
    if actual_paths != expected_paths:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            attempt_id,
            "historical attempt paths are not exactly derived",
        )
    return tuple(attempt.get(field) for field in _IMMUTABLE_ATTEMPT_FIELDS)


def _reachable_core_attempt_history(
    root: Path, core_relative: str
) -> dict[str, _HistoricalAttemptRecord]:
    identities: dict[str, tuple[Any, ...]] = {}
    phases: dict[str, str] = {}
    receipt_ids: dict[str, str] = {}
    statuses: dict[str, set[str]] = {}
    disappeared_ids: set[str] = set()
    commit_states: dict[str, dict[str, tuple[tuple[Any, ...], str]]] = {}
    allowed_statuses = {"PENDING", "PASSED", "FAILED", "ABANDONED"}

    for commit, parents in _reachable_history_graph(root):
        payload = _regular_blob_at_commit(root, commit, core_relative)
        historical_core = (
            {}
            if payload is None
            else _decode_canonical_history_core(
                payload,
                relative=core_relative,
                commit=commit,
            )
        )
        attempts = historical_core.get("reviewAttempts")
        if attempts is None:
            attempts = []
        if not isinstance(attempts, list):
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                "history",
                "historical reviewAttempts collection is malformed",
            )

        current: dict[str, tuple[tuple[Any, ...], str]] = {}
        for attempt in attempts:
            if not isinstance(attempt, dict):
                raise KintsugiError(
                    "KIN-E-CONCURRENT", "history", "historical attempt is malformed"
                )
            identity = _historical_attempt_identity(attempt, context=commit)
            attempt_id = str(attempt["id"])
            status = attempt.get("status")
            if not isinstance(status, str) or status not in allowed_statuses:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    attempt_id,
                    "historical attempt status is malformed",
                )
            if attempt_id in current:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    attempt_id,
                    "historical attempt identity is duplicated",
                )
            previous_identity = identities.get(attempt_id)
            if previous_identity is not None and previous_identity != identity:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    attempt_id,
                    "historical attempt immutable identity changed",
                )
            identities.setdefault(attempt_id, identity)
            phases.setdefault(attempt_id, str(attempt["phase"]))
            receipt_ids.setdefault(attempt_id, str(attempt["receiptId"]))
            statuses.setdefault(attempt_id, set()).add(str(status))
            current[attempt_id] = (identity, str(status))

        for parent in parents:
            parent_state = commit_states[parent]
            missing = set(parent_state) - set(current)
            if missing:
                disappeared_ids.update(missing)
            for attempt_id, (parent_identity, parent_status) in parent_state.items():
                if attempt_id not in current:
                    continue
                child_identity, child_status = current[attempt_id]
                if child_identity != parent_identity:
                    raise KintsugiError(
                        "KIN-E-CONCURRENT",
                        attempt_id,
                        "historical attempt immutable identity changed",
                    )
                if parent_status != "PENDING" and child_status != parent_status:
                    raise KintsugiError(
                        "KIN-E-CONCURRENT",
                        attempt_id,
                        "terminal attempt changed or reopened on a reachable lineage",
                    )
        commit_states[commit] = current

    return {
        attempt_id: _HistoricalAttemptRecord(
            phase=phases[attempt_id],
            receipt_id=receipt_ids[attempt_id],
            identity=identity,
            statuses=frozenset(statuses[attempt_id]),
            disappeared_on_lineage=attempt_id in disappeared_ids,
        )
        for attempt_id, identity in sorted(identities.items())
    }


def _unique_history_record(
    core: dict[str, Any],
    collection: str,
    identity_field: str,
    identity: str,
    *,
    context: str,
) -> dict[str, Any]:
    values = core.get(collection)
    if not isinstance(values, list):
        raise KintsugiError(
            "KIN-E-CONCURRENT", context, f"historical {collection} collection is malformed"
        )
    matches = [
        value
        for value in values
        if isinstance(value, dict) and value.get(identity_field) == identity
    ]
    if len(matches) != 1:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            context,
            f"historical {collection} record is missing or duplicated",
        )
    return matches[0]


def _terminal_snapshots(
    root: Path,
    core_relative: str,
    attempt_id: str,
) -> tuple[tuple[str, dict[str, Any], dict[str, Any]], ...]:
    snapshots: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    terminal_lineage: dict[str, bool] = {}
    for commit, parents in _reachable_history_graph(root):
        inherited_terminal = any(terminal_lineage[parent] for parent in parents)
        payload = _regular_blob_at_commit(root, commit, core_relative)
        if payload is None:
            if inherited_terminal:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    core_relative,
                    "terminal core disappeared on a reachable terminal lineage",
                )
            terminal_lineage[commit] = False
            continue
        historical_core = _decode_canonical_history_core(
            payload,
            relative=core_relative,
            commit=commit,
        )
        attempts = historical_core.get("reviewAttempts")
        if attempts is None:
            if inherited_terminal:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    attempt_id,
                    "terminal attempt disappeared on its terminal lineage",
                )
            terminal_lineage[commit] = False
            continue
        if not isinstance(attempts, list):
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                attempt_id,
                "historical reviewAttempts collection is malformed",
            )
        matches = [
            value
            for value in attempts
            if isinstance(value, dict) and value.get("id") == attempt_id
        ]
        if len(matches) > 1:
            raise KintsugiError(
                "KIN-E-CONCURRENT", attempt_id, "historical attempt identity is duplicated"
            )
        if not matches:
            if inherited_terminal:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    attempt_id,
                    "terminal attempt disappeared on its terminal lineage",
                )
            terminal_lineage[commit] = False
            continue
        status = matches[0].get("status")
        if status in {"PASSED", "FAILED", "ABANDONED"}:
            snapshots.append((commit, historical_core, matches[0]))
            terminal_lineage[commit] = True
            continue
        if status != "PENDING":
            raise KintsugiError(
                "KIN-E-CONCURRENT", attempt_id, "historical attempt status is malformed"
            )
        if inherited_terminal:
            raise KintsugiError(
                "KIN-E-CONCURRENT", attempt_id, "terminal attempt reopened on its terminal lineage"
            )
        terminal_lineage[commit] = False
    if not snapshots:
        raise KintsugiError(
            "KIN-E-CONCURRENT", attempt_id, "first terminal commit is absent from reachable history"
        )
    return tuple(snapshots)


def _reachable_terminal_attempt_statuses(
    root: Path,
    core_relative: str,
    phase: str,
    receipt_id: str,
) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for commit, _ in _reachable_history_graph(root):
        payload = _regular_blob_at_commit(root, commit, core_relative)
        if payload is None:
            continue
        historical_core = _decode_canonical_history_core(
            payload,
            relative=core_relative,
            commit=commit,
        )
        attempts = historical_core.get("reviewAttempts")
        if attempts is None:
            continue
        if not isinstance(attempts, list):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "history", "historical reviewAttempts is malformed"
            )
        seen_in_commit: set[str] = set()
        for value in attempts:
            if not isinstance(value, dict):
                continue
            if value.get("phase") != phase or value.get("receiptId") != receipt_id:
                continue
            attempt_id = value.get("id")
            if not isinstance(attempt_id, str):
                raise KintsugiError(
                    "KIN-E-CONCURRENT", "history", "historical attempt ID is malformed"
                )
            _canonical_attempt_number(attempt_id, phase)
            if attempt_id in seen_in_commit:
                raise KintsugiError(
                    "KIN-E-CONCURRENT", attempt_id, "historical attempt ID is duplicated"
                )
            seen_in_commit.add(attempt_id)
            status = value.get("status")
            if status not in {"PENDING", "PASSED", "FAILED", "ABANDONED"}:
                raise KintsugiError(
                    "KIN-E-CONCURRENT", attempt_id, "historical attempt status is malformed"
                )
            if status == "PENDING":
                continue
            prior_status = statuses.get(attempt_id)
            if prior_status is not None and prior_status != status:
                raise KintsugiError(
                    "KIN-E-CONCURRENT", attempt_id, "terminal attempt status changed in history"
                )
            statuses[attempt_id] = status
    return statuses


def _terminal_record_projection(
    core: dict[str, Any],
    attempt: dict[str, Any],
    *,
    context: str,
) -> dict[str, Any]:
    attempt_id = str(attempt.get("id"))
    artifact = _unique_history_record(
        core,
        "reviewAttemptArtifacts",
        "attemptId",
        attempt_id,
        context=context,
    )
    attestations: list[dict[str, Any]] = []
    for field in ("logicAttestationId", "btjAttestationId"):
        attestation_id = attempt.get(field)
        if attestation_id is None:
            continue
        if not isinstance(attestation_id, str) or not attestation_id:
            raise KintsugiError(
                "KIN-E-CONCURRENT", context, "terminal attestation identity is malformed"
            )
        attestations.append(_unique_history_record(
            core,
            "reviewAttestations",
            "id",
            attestation_id,
            context=context,
        ))
    findings_value = core.get("reviewFindings")
    dispositions_value = core.get("reviewFindingDispositions")
    if not isinstance(findings_value, list) or not isinstance(dispositions_value, list):
        raise KintsugiError(
            "KIN-E-CONCURRENT", context, "terminal review-history collection is malformed"
        )
    findings = [
        value
        for value in findings_value
        if isinstance(value, dict) and value.get("attemptId") == attempt_id
    ]
    dispositions = [
        value
        for value in dispositions_value
        if isinstance(value, dict) and value.get("successorAttemptId") == attempt_id
    ]
    return {
        "attempt": attempt,
        "artifact": artifact,
        "attestations": attestations,
        "findings": findings,
        "dispositions": dispositions,
    }


def _validate_terminal_history_anchor(
    root: Path,
    current_core: dict[str, object],
    current_attempt: dict[str, Any],
    current_artifact: dict[str, Any],
    core_relative: str,
) -> None:
    attempt_id = str(current_attempt["id"])

    def record_changed(historical: object, current: object) -> bool:
        try:
            return canonical_json_bytes(historical) != canonical_json_bytes(current)
        except KintsugiError:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                attempt_id,
                "terminal record cannot be compared as canonical JSON",
            ) from None

    current_projection = _terminal_record_projection(
        current_core,
        current_attempt,
        context=attempt_id,
    )
    if record_changed(current_projection["artifact"], current_artifact):
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            attempt_id,
            "terminal artifact record differs from the current attempt projection",
        )
    snapshots = _terminal_snapshots(root, core_relative, attempt_id)
    for commit, historical_core, historical_attempt in snapshots:
        historical_projection = _terminal_record_projection(
            historical_core,
            historical_attempt,
            context=attempt_id,
        )
        if record_changed(historical_projection, current_projection):
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                attempt_id,
                "terminal records differ across reachable terminal commits",
            )
        target_digest = current_artifact.get("reviewTargetSha256")
        bindings = (
            ("reviewTargetPath", "reviewTargetSha256", target_digest is not None),
            (
                "logicReviewPath",
                "logicReviewSha256",
                current_attempt.get("logicAttestationId") is not None,
            ),
            (
                "btjReviewPath",
                "btjReviewSha256",
                current_attempt.get("btjAttestationId") is not None,
            ),
        )
        for path_field, hash_field, referenced in bindings:
            relative = str(current_attempt.get(path_field))
            digest = current_artifact.get(hash_field)
            if referenced != (digest is not None):
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    relative,
                    "terminal historical path and artifact hash are not biconditional",
                )
            payload = _regular_blob_at_commit(root, commit, relative)
            if digest is None:
                if payload is not None:
                    raise KintsugiError(
                        "KIN-E-CONCURRENT",
                        relative,
                        "unreferenced artifact existed at a terminal commit",
                    )
                continue
            if payload is None or raw_hash(payload) != digest:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    relative,
                    "artifact bytes at a terminal commit do not match the terminal hash",
                )

        validation_path = str(current_attempt.get("validationBundlePath"))
        if (
            current_attempt.get("status") != "PASSED"
            and _regular_blob_at_commit(root, commit, validation_path) is not None
        ):
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                validation_path,
                "terminal attempt had a validation bundle at a terminal commit",
            )


def _validate_reachable_terminal_chain(
    root: Path,
    core: dict[str, object],
    phase: str,
    receipt_id: str,
    core_relative: str,
) -> None:
    historical_attempts = {
        attempt_id: historical
        for attempt_id, historical in _reachable_core_attempt_history(
            root, core_relative
        ).items()
        if historical.phase == phase and historical.receipt_id == receipt_id
    }
    disappeared = sorted(
        attempt_id
        for attempt_id, historical in historical_attempts.items()
        if historical.disappeared_on_lineage
    )
    if disappeared:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            disappeared[0],
            "allocated attempt disappeared on a reachable lineage",
        )
    historical_statuses = _reachable_terminal_attempt_statuses(
        root,
        core_relative,
        phase,
        receipt_id,
    )
    if not historical_attempts and not historical_statuses:
        return
    attempts_value = core.get("reviewAttempts")
    artifacts_value = core.get("reviewAttemptArtifacts")
    receipts_value = core.get("phaseReceipts")
    if (
        not isinstance(attempts_value, list)
        or not isinstance(artifacts_value, list)
        or not isinstance(receipts_value, list)
    ):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "history", "current review history collections are malformed"
        )
    chain = [
        value
        for value in attempts_value
        if isinstance(value, dict)
        and value.get("phase") == phase
        and value.get("receiptId") == receipt_id
    ]
    leaf = _unique_chain_leaf(chain, context="reachable terminal history")
    if leaf is None:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            "history",
            "reachable terminal history has no current chain",
        )
    current_by_id: dict[str, dict[str, Any]] = {}
    for attempt in chain:
        attempt_id = attempt.get("id")
        if not isinstance(attempt_id, str) or attempt_id in current_by_id:
            raise KintsugiError(
                "KIN-E-CONCURRENT", "history", "current attempt history is malformed"
            )
        current_by_id[attempt_id] = attempt
    missing = set(historical_attempts) - set(current_by_id)
    if missing:
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            sorted(missing)[0],
            "reachable allocated attempt is missing from the current chain",
        )
    for attempt_id, historical in sorted(historical_attempts.items()):
        attempt = current_by_id[attempt_id]
        if _historical_attempt_identity(
            attempt, context=attempt_id
        ) != historical.identity:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                attempt_id,
                "current attempt differs from its immutable historical identity",
            )
        current_status = attempt.get("status")
        if not isinstance(current_status, str) or current_status not in {
            "PENDING",
            "PASSED",
            "FAILED",
            "ABANDONED",
        }:
            raise KintsugiError(
                "KIN-E-CONCURRENT", attempt_id, "current attempt status is malformed"
            )
        terminal_statuses = historical.statuses - {"PENDING"}
        if len(terminal_statuses) > 1 or (
            terminal_statuses and current_status not in terminal_statuses
        ):
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                attempt_id,
                "current attempt is not a legal continuation of reachable history",
            )
    receipts = [
        value
        for value in receipts_value
        if isinstance(value, dict) and value.get("id") == receipt_id
    ]
    if len(receipts) != 1 or receipts[0].get("reviewAttemptId") != leaf.get("id"):
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            receipt_id,
            "receipt pointer must name the unique terminal-history leaf",
        )
    for attempt_id, historical_status in sorted(historical_statuses.items()):
        attempt = current_by_id[attempt_id]
        if attempt.get("status") != historical_status:
            raise KintsugiError(
                "KIN-E-CONCURRENT", attempt_id, "terminal attempt status changed from history"
            )
        artifacts = [
            value
            for value in artifacts_value
            if isinstance(value, dict) and value.get("attemptId") == attempt_id
        ]
        if len(artifacts) != 1:
            raise KintsugiError(
                "KIN-E-CONCURRENT", attempt_id, "terminal artifact record is missing or duplicated"
            )
        _validate_terminal_history_anchor(
            root,
            core,
            attempt,
            artifacts[0],
            core_relative,
        )


def _validate_predecessor_fence(
    root: Path,
    core: dict[str, object],
    phase: str,
    receipt_id: str,
    core_relative: str,
) -> None:
    identity = RECEIPT_IDENTITIES.get(phase)
    if identity is None or receipt_id != identity[0]:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "predecessor", "predecessor receipt is not canonical"
        )
    attempts_value = core.get("reviewAttempts") if isinstance(core, dict) else None
    artifacts_value = core.get("reviewAttemptArtifacts") if isinstance(core, dict) else None
    receipts_value = core.get("phaseReceipts") if isinstance(core, dict) else None
    if not isinstance(attempts_value, list) or not isinstance(artifacts_value, list) or not isinstance(receipts_value, list):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "predecessor", "predecessor collections are malformed"
        )
    chain = [
        attempt for attempt in attempts_value
        if isinstance(attempt, dict)
        and attempt.get("phase") == phase
        and attempt.get("receiptId") == receipt_id
    ]
    ids = {attempt.get("id") for attempt in chain}
    if not chain or any(not isinstance(value, str) for value in ids) or len(ids) != len(chain):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "predecessor", "predecessor chain identities are malformed"
        )
    for attempt in chain:
        attempt_id = str(attempt["id"])
        _canonical_attempt_number(attempt_id, phase)
        if tuple(attempt.get(field) for field in (
            "reviewTargetPath", "logicReviewPath", "btjReviewPath", "validationBundlePath"
        )) != attempt_paths(attempt_id):
            raise KintsugiError(
                "KIN-E-CONCURRENT", "predecessor", "predecessor artifact paths are not exactly derived"
            )
    predecessor = _unique_chain_leaf(chain, context="predecessor")
    if predecessor is None:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "predecessor", "predecessor chain is empty"
        )
    if any(attempt.get("status") not in {"FAILED", "ABANDONED"} for attempt in chain):
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            "predecessor",
            "predecessor chain contains a non-terminal attempt",
        )

    artifacts_by_attempt: dict[str, dict[str, Any]] = {}
    for attempt in chain:
        attempt_id = str(attempt["id"])
        matches = [
            artifact
            for artifact in artifacts_value
            if isinstance(artifact, dict) and artifact.get("attemptId") == attempt_id
        ]
        if len(matches) != 1:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                "predecessor",
                "predecessor artifact record is missing or duplicated",
            )
        artifacts_by_attempt[attempt_id] = matches[0]
    receipts = [
        receipt for receipt in receipts_value
        if isinstance(receipt, dict) and receipt.get("id") == receipt_id
    ]
    if len(receipts) != 1 or receipts[0].get("reviewAttemptId") != predecessor.get("id"):
        raise KintsugiError(
            "KIN-E-CONCURRENT", "predecessor", "receipt does not point to the terminal predecessor"
        )
    receipt = receipts[0]

    core_bytes = _read_regular_no_symlinks(
        root,
        core_relative,
        code="KIN-E-CONCURRENT",
        require_single_link=True,
    )
    if core_bytes != canonical_json_bytes(core):
        raise KintsugiError(
            "KIN-E-CONCURRENT",
            core_relative,
            "working core bytes do not equal the supplied successor records",
        )
    receipt_bytes = _read_regular_no_symlinks(
        root,
        str(receipt.get("path")),
        code="KIN-E-CONCURRENT",
        require_single_link=True,
    )
    synchronized = synchronize_receipt_markdown(
        receipt_bytes,
        receipt,
        path=str(receipt.get("path")),
        target_frozen=False,
    )
    if synchronized.issues or synchronized.receipt_record != receipt:
        raise KintsugiError(
            "KIN-E-CONCURRENT", str(receipt.get("path")), "terminal receipt fence is not synchronized"
        )

    for attempt in sorted(
        chain,
        key=lambda value: _canonical_attempt_number(str(value["id"]), phase),
    ):
        attempt_id = str(attempt["id"])
        artifact = artifacts_by_attempt[attempt_id]
        _validate_terminal_history_anchor(
            root,
            core,
            attempt,
            artifact,
            core_relative,
        )
        target_digest = artifact.get("reviewTargetSha256")
        if attempt.get("status") == "FAILED" and target_digest is None:
            raise KintsugiError(
                "KIN-E-CONCURRENT",
                "predecessor",
                "FAILED predecessor has no target hash",
            )
        bindings = (
            ("reviewTargetPath", "reviewTargetSha256", target_digest is not None),
            (
                "logicReviewPath",
                "logicReviewSha256",
                attempt.get("logicAttestationId") is not None,
            ),
            (
                "btjReviewPath",
                "btjReviewSha256",
                attempt.get("btjAttestationId") is not None,
            ),
        )
        for path_field, hash_field, referenced in bindings:
            relative = str(attempt.get(path_field))
            digest = artifact.get(hash_field)
            if referenced != (digest is not None):
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    relative,
                    "predecessor path and artifact hash are not biconditional",
                )
            if digest is None:
                _require_absent_at_head_and_worktree(root, relative)
                continue
            payload = _committed_regular_bytes(root, relative)
            if raw_hash(payload) != digest:
                raise KintsugiError(
                    "KIN-E-CONCURRENT",
                    relative,
                    "predecessor artifact hash does not match committed bytes",
                )
        _require_absent_at_head_and_worktree(
            root, str(attempt.get("validationBundlePath"))
        )


def inspect_git_state(root: Path, base_commit: str) -> object:
    try:
        resolved_root = root.resolve(strict=True)
    except OSError as exc:
        raise KintsugiError(
            "KIN-E-CONCURRENT", "git", f"worktree root is unavailable: {exc.__class__.__name__}"
        ) from None
    head = _resolve_commit(resolved_root, "HEAD")
    base = _resolve_commit(resolved_root, base_commit)
    committed = _parse_name_status(_run_git_z(
        resolved_root,
        ("diff", "--name-status", "-z", "--find-renames", base, head, "--"),
    ))
    staged = _parse_name_status(_run_git_z(
        resolved_root,
        ("diff", "--cached", "--name-status", "-z", "--find-renames", "--"),
    ))
    unstaged = _parse_name_status(_run_git_z(
        resolved_root,
        ("diff", "--name-status", "-z", "--find-renames", "--"),
    ))
    mode_paths = set(_parse_unrepresentable_mode_paths(_run_git_z(
        resolved_root,
        ("diff", "--raw", "--no-abbrev", "-z", base, head, "--"),
    )))
    mode_paths.update(_parse_unrepresentable_mode_paths(_run_git_z(
        resolved_root,
        ("diff", "--cached", "--raw", "--no-abbrev", "-z", "--"),
    )))
    mode_paths.update(_parse_unrepresentable_mode_paths(_run_git_z(
        resolved_root,
        ("diff", "--raw", "--no-abbrev", "-z", "--"),
    )))
    untracked, untracked_mode_paths = _snapshot_untracked(resolved_root)
    mode_paths.update(untracked_mode_paths)
    noncanonical_index_paths = _parse_noncanonical_index_paths(
        _run_git_z(resolved_root, ("ls-files", "-v", "-z", "--"))
    )
    return GitState(
        root=resolved_root,
        head=head,
        branch=_branch(resolved_root),
        common_dir=resolve_git_common_dir(resolved_root),
        base_commit=base,
        committed_paths=committed,
        staged_paths=staged,
        unstaged_paths=unstaged,
        unrepresentable_mode_paths=tuple(sorted(mode_paths)),
        noncanonical_index_paths=noncanonical_index_paths,
        untracked_records=untracked,
    )


__all__ = ["inspect_git_state", "resolve_git_common_dir"]
