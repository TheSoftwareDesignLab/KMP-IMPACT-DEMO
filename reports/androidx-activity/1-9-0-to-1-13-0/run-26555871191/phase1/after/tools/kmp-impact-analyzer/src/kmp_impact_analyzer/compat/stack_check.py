"""Detect KMP stack versions and warn about incompatibilities with the bumped dependency.

Reads ``gradle/libs.versions.toml`` (and optionally ``build.gradle.kts``) to discover the
project's Kotlin / AGP / Compose versions and contrasts them with known minimum
requirements of the dependency being upgraded. Produces structured warnings that the
report and the PR comment can render.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..contracts import CompatibilityWarning, StackCompatibilityReport


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------

_VERSION_KEY_RE = re.compile(r'^\s*([\w-]+)\s*=\s*"([^"]+)"', re.MULTILINE)


def _find_catalog(repo_path: Path) -> Path | None:
    for candidate in [
        repo_path / "gradle" / "libs.versions.toml",
        repo_path / "libs.versions.toml",
    ]:
        if candidate.exists():
            return candidate
    return None


def _read_versions(catalog: Path) -> dict[str, str]:
    """Parse the ``[versions]`` section of a Gradle Version Catalog."""
    text = catalog.read_text(encoding="utf-8", errors="replace")
    versions: dict[str, str] = {}
    in_versions = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("["):
            in_versions = line == "[versions]"
            continue
        if not in_versions or not line or line.startswith("#"):
            continue
        m = _VERSION_KEY_RE.match(raw)
        if m:
            versions[m.group(1).lower()] = m.group(2)
    return versions


def _pick(versions: dict[str, str], *keys: str) -> str:
    for k in keys:
        v = versions.get(k.lower())
        if v:
            return v
    return ""


def detect_stack(repo_path: str | Path) -> dict[str, str]:
    """Best-effort detection of Kotlin, AGP, Compose versions used by the project."""
    repo = Path(repo_path)
    catalog = _find_catalog(repo)
    if not catalog:
        return {}
    versions = _read_versions(catalog)
    return {
        "kotlin": _pick(versions, "kotlin", "kotlinVersion", "kotlin-version"),
        "agp": _pick(
            versions, "agp", "android-gradle-plugin", "androidGradlePlugin", "android"
        ),
        "compose": _pick(
            versions,
            "compose",
            "compose-multiplatform",
            "composeMultiplatform",
            "composeBom",
            "compose-bom",
        ),
        "compose-compiler": _pick(
            versions, "compose-compiler", "composeCompiler", "compose-compiler-extension"
        ),
        "gradle": _pick(versions, "gradle", "gradleVersion"),
    }


# ---------------------------------------------------------------------------
# Compatibility rules
# ---------------------------------------------------------------------------

def _semver_tuple(v: str) -> tuple[int, ...]:
    """Coerce a version string to a comparable integer tuple."""
    if not v:
        return (0,)
    pieces = re.split(r"[.\-_+]", v)
    out: list[int] = []
    for p in pieces:
        m = re.match(r"^(\d+)", p)
        if m:
            out.append(int(m.group(1)))
        else:
            break
    return tuple(out) if out else (0,)


def _gte(actual: str, required: str) -> bool:
    return _semver_tuple(actual) >= _semver_tuple(required)


def _ktor_warning(after_version: str, stack: dict[str, str]) -> CompatibilityWarning | None:
    """Ktor 3.x requires Kotlin 2.x and a recent KMP toolchain."""
    if not after_version.startswith("3.") and not after_version.startswith("4."):
        return None
    kotlin = stack.get("kotlin", "")
    if not kotlin:
        return None
    if _gte(kotlin, "2.0.0"):
        return None
    return CompatibilityWarning(
        severity="warning",
        title=f"Ktor {after_version} requires Kotlin 2.x",
        detail=(
            f"Detected Kotlin {kotlin}. Ktor 3.x ships as a Kotlin 2.x library, "
            "and its iOS/Native targets often fail to link against Kotlin 1.9. "
            "AGP and Compose typically need to move at the same time."
        ),
        suggestion=(
            "Either upgrade Kotlin to 2.0+ (and AGP / Compose accordingly), "
            "or pin Ktor on the 2.3.x line."
        ),
        detected={"kotlin": kotlin, **{k: v for k, v in stack.items() if k != "kotlin" and v}},
        required={"kotlin": ">= 2.0.0"},
    )


def _compose_compiler_warning(
    dep_group: str, after_version: str, stack: dict[str, str]
) -> CompatibilityWarning | None:
    if not dep_group.startswith("androidx.compose"):
        return None
    kotlin = stack.get("kotlin", "")
    cc = stack.get("compose-compiler", "")
    if not kotlin or not cc:
        return None
    # The compose-compiler version must match the Kotlin version.
    if _semver_tuple(kotlin)[:2] != _semver_tuple(cc)[:2] and not _gte(kotlin, "2.0.0"):
        return CompatibilityWarning(
            severity="warning",
            title="Compose compiler may not match Kotlin version",
            detail=(
                f"Detected Kotlin {kotlin} alongside compose-compiler {cc}. "
                "Bumping Compose Foundation often forces a matching compose-compiler "
                "release tied to a specific Kotlin minor."
            ),
            suggestion=(
                "Cross-check the Compose / Kotlin compatibility table before merging. "
                "If iOS or commonMain fails to compile, update Kotlin and "
                "compose-compiler in lockstep."
            ),
            detected={"kotlin": kotlin, "compose-compiler": cc},
            required={"kotlin": "matches compose-compiler"},
        )
    return None


_RULES = [
    ("io.ktor", _ktor_warning),
    ("androidx.compose", _compose_compiler_warning),
]


def build_compatibility_report(
    repo_path: str | Path,
    dependency_group: str,
    after_version: str,
) -> StackCompatibilityReport:
    """Run all applicable rules and return a structured report."""
    stack = detect_stack(repo_path)
    warnings: list[CompatibilityWarning] = []
    for prefix, rule in _RULES:
        if not dependency_group.startswith(prefix):
            continue
        w = rule(after_version, stack) if prefix == "io.ktor" else rule(
            dependency_group, after_version, stack
        )
        if w:
            warnings.append(w)
    return StackCompatibilityReport(warnings=warnings, detected={k: v for k, v in stack.items() if v})
