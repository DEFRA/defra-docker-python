#!/usr/bin/env python3
"""Build every image in image-matrix.json locally and scan it with Trivy and Grype.

Mirrors the build-scan-push workflow: same build args, same ignore files, and
a medium severity cutoff. Raw reports are saved under --out (default
/tmp/image-scans/<timestamp>, with a ``latest`` symlink) and a condensed view
is printed that separates findings common to every image (almost always OS
packages) from those that differ between Python versions.

Usage:
    scripts/scan_images.py                     # build + scan everything
    scripts/scan_images.py -v 3.14 -v 3.13     # only matching python versions
    scripts/scan_images.py --skip-build        # reuse images from a previous run
    scripts/scan_images.py --no-cache          # match CI's --no-cache build

Images are built and scanned concurrently (asyncio); per-command output goes to
<out>/logs/ so the console only shows progress lines.

Exits 1 if any medium+ finding remains after the ignore files are applied.
"""

import argparse
import asyncio
import csv
import json
import shutil
import sys
import time
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
RANK = {name: i for i, name in enumerate(SEVERITIES)}
TAG_PREFIX = "defra-scan/python"
COLOURS = {"CRITICAL": "35", "HIGH": "31", "MEDIUM": "33", "LOW": "36"}


@dataclass(frozen=True)
class Finding:
    id: str
    package: str
    installed: str
    fixed: str
    severity: str
    kind: str  # "os" or "lib"
    tool: str


class ScanError(Exception):
    pass


# Trivy and Grype keep a shared on-disk DB/cache that does not tolerate
# concurrent runs of the same tool, so each tool is serialised across images
# while the two tools (and image builds) still overlap.
TOOL_LOCKS: dict[str, asyncio.Lock] = {}


async def run(cmd: list[str], log: Path) -> None:
    """Run a command with output captured to ``log``; raise ScanError on failure."""
    label = log.stem
    print(f"[{label}] $ {' '.join(cmd)}", flush=True)
    start = time.monotonic()
    proc = await asyncio.create_subprocess_exec(
        *cmd, cwd=REPO, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
    )
    try:
        output, _ = await proc.communicate()
    except asyncio.CancelledError:
        proc.kill()
        await proc.wait()
        raise
    log.write_bytes(output)
    elapsed = time.monotonic() - start
    if proc.returncode:
        tail = "\n".join(output.decode(errors="replace").splitlines()[-15:])
        raise ScanError(f"[{label}] FAILED (exit {proc.returncode}, {elapsed:.0f}s), see {log}\n{tail}")
    print(f"[{label}] done in {elapsed:.0f}s", flush=True)


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def sev(name: str) -> str:
    return paint(f"{name:<8}", COLOURS.get(name, "0"))


def load_defra_version() -> str:
    for line in (REPO / "JOB.env").read_text().splitlines():
        key, _, value = line.partition("=")
        if key == "DEFRA_VERSION":
            return value.strip()
    sys.exit("DEFRA_VERSION not found in JOB.env")


def select_images(filters: list[str]) -> list[dict]:
    images = json.loads((REPO / "image-matrix.json").read_text())
    if filters:
        images = [i for i in images if any(i["pythonVersion"].startswith(f) for f in filters)]
    if not images:
        sys.exit("No images in image-matrix.json match the given --version filters")
    return images


async def build(image: dict, defra_version: str, tag: str, target: str, no_cache: bool, log: Path) -> None:
    base = f"{image['pythonVersion']}-{image['debianVersion']}"
    cmd = [
        "docker", "build", ".", "--file", "Dockerfile", "--target", target,
        "--build-arg", f"DEFRA_VERSION={defra_version}",
        "--build-arg", f"BASE_VERSION={base}",
        "--build-arg", f"PYTHON_VERSION={image['pythonVersion']}",
        "--tag", tag,
    ]
    if no_cache:
        cmd.append("--no-cache")
    await run(cmd, log)


async def scan_trivy(archive: Path, out: Path, name: str) -> list[Finding]:
    raw = out / f"{name}.trivy.json"
    cmd = [
        "trivy", "image", "--input", str(archive), "--scanners", "vuln",
        "--pkg-types", "os,library", "--ignorefile", ".trivyignore",
        "--severity", ",".join(SEVERITIES[1:]), "--quiet",
        "--format", "json", "--output", str(raw),
    ]
    logs = out / "logs"
    async with TOOL_LOCKS["trivy"]:
        await run(cmd, logs / f"{name}-trivy.log")
    await run(["trivy", "convert", "--format", "table", "--output", str(out / f"{name}.trivy.txt"), str(raw)],
              logs / f"{name}-trivy-convert.log")

    findings = []
    for result in json.loads(raw.read_text()).get("Results", []):
        kind = "os" if result.get("Class") == "os-pkgs" else "lib"
        for v in result.get("Vulnerabilities") or []:
            findings.append(Finding(
                v["VulnerabilityID"], v["PkgName"], v.get("InstalledVersion", ""),
                v.get("FixedVersion", ""), v.get("Severity", "UNKNOWN").upper(), kind, "trivy",
            ))
    return findings


async def scan_grype(archive: Path, out: Path, name: str) -> list[Finding]:
    raw = out / f"{name}.grype.json"
    cmd = [
        "grype", f"docker-archive:{archive}", "--config", ".grype.yaml", "--quiet",
        "-o", f"json={raw}", "-o", f"table={out / f'{name}.grype.txt'}",
    ]
    async with TOOL_LOCKS["grype"]:
        await run(cmd, out / "logs" / f"{name}-grype.log")

    findings = []
    for m in json.loads(raw.read_text()).get("matches", []):
        v, a = m["vulnerability"], m["artifact"]
        severity = v.get("severity", "Unknown").upper()
        if severity not in RANK or RANK[severity] < RANK["MEDIUM"]:
            continue  # grype has no severity filter that stops after the report is written
        findings.append(Finding(
            v["id"], a["name"], a.get("version", ""), ", ".join(v.get("fix", {}).get("versions", [])),
            severity, "os" if a.get("type") == "deb" else "lib", "grype",
        ))
    return findings


async def scan_image(
    image: dict, defra_version: str, args: argparse.Namespace, out: Path, builds: asyncio.Semaphore,
) -> tuple[str, list[Finding]]:
    name = f"python-{image['pythonVersion']}"
    tag = f"{TAG_PREFIX}:{defra_version}-python{image['pythonVersion']}"
    archive = out / f"{name}.tar"
    logs = out / "logs"
    async with builds:
        if not args.skip_build:
            await build(image, defra_version, tag, args.target, args.no_cache, logs / f"{name}-build.log")
        await run(["docker", "save", tag, "-o", str(archive)], logs / f"{name}-save.log")
    try:
        trivy, grype = await asyncio.gather(scan_trivy(archive, out, name), scan_grype(archive, out, name))
    finally:
        if not args.keep_archives:
            archive.unlink(missing_ok=True)
    return name, trivy + grype


def merge(findings: list[Finding]) -> dict[tuple[str, str], dict]:
    """Collapse tool-specific findings into one row per (vulnerability id, package)."""
    merged: dict[tuple[str, str], dict] = {}
    for f in findings:
        row = merged.setdefault((f.id, f.package), {
            "id": f.id, "package": f.package, "installed": f.installed, "fixed": f.fixed,
            "severity": f.severity, "kind": f.kind, "tools": set(),
        })
        row["tools"].add(f.tool)
        row["fixed"] = row["fixed"] or f.fixed
        if RANK.get(f.severity, 0) > RANK.get(row["severity"], 0):
            row["severity"] = f.severity
    return merged


def report(results: dict[str, list[Finding]], out: Path) -> int:
    names = list(results)
    per_image = {n: merge(fs) for n, fs in results.items()}
    all_keys = sorted({k for rows in per_image.values() for k in rows})
    lines: list[str] = []

    def emit(text: str = "") -> None:
        lines.append(text)
        print(text)

    emit("\n" + "=" * 78)
    emit("SUMMARY (medium+ after ignore files)")
    emit("=" * 78)
    emit(f"{'image':<14}" + "".join(f"{s:>10}" for s in reversed(SEVERITIES[1:])) + f"{'trivy':>8}{'grype':>8}")
    for n in names:
        rows = per_image[n].values()
        counts = [sum(r["severity"] == s for r in rows) for s in reversed(SEVERITIES[1:])]
        t = sum("trivy" in r["tools"] for r in rows)
        g = sum("grype" in r["tools"] for r in rows)
        emit(f"{n:<14}" + "".join(f"{c:>10}" for c in counts) + f"{t:>8}{g:>8}")

    common = [k for k in all_keys if all(k in per_image[n] for n in names)]
    differing = [k for k in all_keys if k not in common]

    def row_for(key):
        return next(per_image[n][key] for n in names if key in per_image[n])

    emit("\n" + "=" * 78)
    emit(f"COMMON TO ALL {len(names)} IMAGES: {len(common)} (usually OS packages; review once)")
    emit("=" * 78)
    by_pkg: dict[str, list[dict]] = {}
    for k in common:
        by_pkg.setdefault(row_for(k)["package"], []).append(row_for(k))
    for pkg, rows in sorted(by_pkg.items(), key=lambda kv: -max(RANK.get(r["severity"], 0) for r in kv[1])):
        top = max(rows, key=lambda r: RANK.get(r["severity"], 0))["severity"]
        fixed = "fix available" if any(r["fixed"] for r in rows) else "no fix"
        emit(f"{sev(top)} {pkg} {rows[0]['installed']} [{rows[0]['kind']}] ({fixed})")
        emit(f"         {', '.join(sorted(r['id'] for r in rows))}")

    emit("\n" + "=" * 78)
    emit(f"DIFFERS BETWEEN IMAGES: {len(differing)} (python version specific; focus here)")
    emit("=" * 78)
    w = max(len(n) for n in names) + 2
    if differing:
        emit(f"{'':<9}{'vulnerability':<24}{'package':<22}{'installed':<14}{'fixed':<14}"
             + "".join(f"{n:<{w}}" for n in names) + "tools")
        for k in sorted(differing, key=lambda k: (-RANK.get(row_for(k)["severity"], 0), k)):
            r = row_for(k)
            marks = "".join(f"{('yes' if k in per_image[n] else '-'):<{w}}" for n in names)
            emit(f"{sev(r['severity'])} {r['id']:<24}{r['package']:<22}{r['installed']:<14}"
                 f"{(r['fixed'] or '-'):<14}{marks}{'+'.join(sorted(r['tools']))}")
    else:
        emit("(none, every image has the same findings)")

    tool_only = [k for k in all_keys if len(row_for(k)["tools"]) == 1 and all(
        per_image[n][k]["tools"] == row_for(k)["tools"] for n in names if k in per_image[n])]
    emit("\n" + "=" * 78)
    emit(f"SEEN BY ONLY ONE SCANNER: {len(tool_only)} (id naming differences e.g. GHSA vs CVE are common)")
    emit("=" * 78)
    for k in tool_only:
        r = row_for(k)
        emit(f"{sev(r['severity'])} {r['id']:<24}{r['package']:<22}only {next(iter(r['tools']))}")

    if all_keys:
        emit("\n" + "=" * 78)
        emit("IGNORE STUBS (paste into the ignore files after triage; keep both in sync)")
        emit("=" * 78)
        emit(".trivyignore:")
        for k in all_keys:
            emit(f"# {k[1]}: <reason>\n{k[0]}")
        emit(".grype.yaml:")
        for k in all_keys:
            emit(f"  # {k[1]}: <reason>\n  - vulnerability: {k[0]}")

    with (out / "findings.csv").open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "package", "installed", "fixed", "severity", "kind", "scope", "tools", *names])
        for k in all_keys:
            r = row_for(k)
            writer.writerow([r["id"], r["package"], r["installed"], r["fixed"], r["severity"], r["kind"],
                             "common" if k in common else "differs", "+".join(sorted(r["tools"])),
                             *["yes" if k in per_image[n] else "" for n in names]])
    (out / "report.txt").write_text("\n".join(lines) + "\n")
    return len(all_keys)


async def scan_all(images: list[dict], defra_version: str, args: argparse.Namespace, out: Path) -> dict[str, list[Finding]]:
    TOOL_LOCKS.update(trivy=asyncio.Lock(), grype=asyncio.Lock())
    builds = asyncio.Semaphore(args.jobs or len(images))
    try:
        pairs = await asyncio.gather(*(scan_image(i, defra_version, args, out, builds) for i in images))
    except ScanError as exc:
        sys.exit(str(exc))
    return dict(pairs)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="append", default=[], help="python version prefix filter (repeatable)")
    parser.add_argument("--target", default="production", help="Dockerfile target to build and scan")
    parser.add_argument("--out", type=Path, help="output directory (default /tmp/image-scans/<timestamp>)")
    parser.add_argument("--skip-build", action="store_true", help="scan images already tagged by a previous run")
    parser.add_argument("--no-cache", action="store_true", help="build with --no-cache like CI")
    parser.add_argument("--jobs", type=int, help="max concurrent image builds (default: all images at once)")
    parser.add_argument("--keep-archives", action="store_true", help="keep docker save tarballs in the output dir")
    args = parser.parse_args()

    for tool in ("docker", "trivy", "grype"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH")

    out = args.out or Path("/tmp/image-scans") / time.strftime("%Y%m%d-%H%M%S")
    out.mkdir(parents=True, exist_ok=True)
    latest = out.parent / "latest"
    if not args.out:
        latest.unlink(missing_ok=True)
        latest.symlink_to(out)

    (out / "logs").mkdir(exist_ok=True)

    results = asyncio.run(scan_all(select_images(args.version), load_defra_version(), args, out))
    total = report(results, out)
    print(f"\nArtifacts saved to {out}")
    print("  report.txt, findings.csv, <image>.trivy.{json,txt}, <image>.grype.{json,txt}, logs/")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
