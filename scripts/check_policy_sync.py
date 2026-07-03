#!/usr/bin/env python3
"""Validates that vulnerability ignore lists are in sync with POLICY_CONFIGURATION.md.

All CVEs listed in .grype.yaml and .trivyignore must have a corresponding entry
in POLICY_CONFIGURATION.md. Run this before builds to catch undocumented exclusions.
"""

import re
import sys
from pathlib import Path

POLICY_FILE = Path("POLICY_CONFIGURATION.md")
GRYPE_FILE = Path(".grype.yaml")
TRIVY_FILE = Path(".trivyignore")

CVE_PATTERN = re.compile(r"CVE-\d{4}-\d+")


def extract_policy_cves(path: Path) -> set[str]:
    """Extract all CVE IDs from markdown table rows in the policy document."""
    cves: set[str] = set()

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            cves.update(CVE_PATTERN.findall(line))

    return cves


def extract_grype_cves(path: Path) -> set[str]:
    """Extract active (non-commented) CVE IDs from .grype.yaml."""
    cves: set[str] = set()

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if stripped.startswith("#"):
            continue

        match = CVE_PATTERN.search(stripped)

        if match:
            cves.add(match.group())

    return cves


def extract_trivy_cves(path: Path) -> set[str]:
    """Extract active (non-commented) CVE IDs from .trivyignore."""
    cves: set[str] = set()

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        match = CVE_PATTERN.match(stripped)

        if match:
            cves.add(match.group())

    return cves


def find_undocumented(
    policy_cves: set[str],
    ignore_cves: set[str],
    ignore_name: str,
) -> list[str]:
    """Return error lines for CVEs in an ignore file that are absent from the policy."""
    undocumented = ignore_cves - policy_cves

    if not undocumented:
        return []

    return [
        f"  {cve}  <- in {ignore_name} but missing from {POLICY_FILE.name}"
        for cve in sorted(undocumented)
    ]


def find_unignored(
    policy_cves: set[str],
    grype_cves: set[str],
    trivy_cves: set[str],
) -> list[str]:
    """Return error lines for CVEs in the policy that are absent from both ignore files."""
    unignored = policy_cves - (grype_cves | trivy_cves)

    if not unignored:
        return []

    return [
        f"  {cve}  <- in {POLICY_FILE.name} but not in {GRYPE_FILE.name} or {TRIVY_FILE.name}"
        for cve in sorted(unignored)
    ]


def main() -> int:
    policy_cves = extract_policy_cves(POLICY_FILE)
    grype_cves = extract_grype_cves(GRYPE_FILE)
    trivy_cves = extract_trivy_cves(TRIVY_FILE)

    errors: list[str] = []

    grype_errors = find_undocumented(policy_cves, grype_cves, GRYPE_FILE.name)

    if grype_errors:
        errors.append(f"\n{GRYPE_FILE.name} contains undocumented exclusions:")
        errors.extend(grype_errors)

    trivy_errors = find_undocumented(policy_cves, trivy_cves, TRIVY_FILE.name)

    if trivy_errors:
        errors.append(f"\n{TRIVY_FILE.name} contains undocumented exclusions:")
        errors.extend(trivy_errors)

    unignored_errors = find_unignored(policy_cves, grype_cves, trivy_cves)

    if unignored_errors:
        errors.append(f"\n{POLICY_FILE.name} documents CVEs not present in either ignore file:")
        errors.extend(unignored_errors)

    if errors:
        print("Policy sync check FAILED\n")

        for error in errors:
            print(error)

        print(
            f"\nEnsure all CVEs in {POLICY_FILE.name} are actively ignored in "
            f"{GRYPE_FILE.name} or {TRIVY_FILE.name}, and vice versa."
        )

        return 1

    print(
        f"Policy sync check passed - {GRYPE_FILE.name} and {TRIVY_FILE.name} "
        f"are in sync with {POLICY_FILE.name}."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
