# Vulnerability scanning configuration and ignored vulnerabilities
[Anchore Grype](https://github.com/anchore/grype/) and [Aqua Trivy](https://www.aquasec.com/products/trivy/) are configured to report vulnerabilities that are of medium severity or higher. 

## OS / base image issues
The following OS / base image issues have been added to the policies exclusion list:
| CVE ID | Type | Component | Date Added | Reason |
|------------------------|------|-----------|------|--------|
| CVE-2025-7709 | Integer overflow | libsqlite3-0 | 07/11/2025 | Fixed in Debian testing - Risk not enough to warrant backport build time |
| CVE-2025-14104 | Buffer overread | util-linux | 19/12/2025 | Fixed in Debian testing (forky) but backport held up by glibc upgrade requirement - Fix might only be possible in next Debian stable release. |
| CVE-2025-15281 | Uninitialised memory | glibc (libc-bin, libc-dev-bin, libc6, libc6-dev) | 16/02/2026 | Fixed in Debian testing (forky) but significant system stability risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2026-0915 | Information Leak / Use of Uninitialized Resource | glibc (libc-bin, libc-dev-bin, libc6, libc6-dev) | 16/02/2026 | Fixed in Debian testing (forky) but significant system stability risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2026-0861 | Integer Overflow | glibc (libc-bin, libc-dev-bin, libc6, libc6-dev) | 16/02/2026 | Fixed in Debian testing (forky) but significant system stability risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2025-6141 | Stack-based Buffer Overflow | ncurses (libncursesw6, libtinfo6, ncurses-base, ncurses-bin) | 16/02/2026 | Fixed in Debian testing (forky) but backport held up by glibc upgrade requirement - Fix might only be possible in next Debian stable release. |
| CVE-2026-27171 | CPU Consumption / DoS | zlib1g | 26/02/2026 | Fixed in zlib 1.3.2. Awaiting release of Debian package with zlib 1.3.2 - fix might only be possible in next Debian stable release. |
| CVE-2026-4105 | Privilege escalation / PolicyKit interaction | systemd | 16/03/2026 | Not exploitable in this container image. Although vulnerable `systemd` is present, exploitation relies upon a custom `polkit` policy. Confirmed `polkit` is not installed in base image. |
| CVE-2025-69720 | Buffer overflow | ncurses (libncursesw6, libtinfo6, ncurses-base, ncurses-bin) | 26/03/2026 | Patch for ncurses release - waiting for Debian to release updated package - fix might only be possible in next Debian stable release. |
| CVE-2026-2673 | TLS Key Exchange | openssl | 26/03/2026 | Marked as 'wont-fix' for Debian Trixie. Will monitor for future Debian release with fix, but risk not significant enough to warrant backport build time. |
| CVE-2026-4437 | DNS Verification Bypass | libc (libc6, libc-bin) | 26/03/2026 | Still waiting for fix in unstable package. Risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2026-4438 | DNS Verification Bypass | libc (libc6, libc-bin) | 26/03/2026 | Still waiting for fix in unstable package. Risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2026-29111 | Execution freeze / DoS | systemd | 26/03/2026 | Fixed in Debian testing - Risk not enough to warrant backport build time. Can't be executed remotely and requires local access |

### Python issues
The following Python issues have been added to the policies exclusion list:
| CVE ID | Type | Component | Date Added | Affected Versions | Reason |
|--------|------|-----------|------|-------------------|--------|
| CVE-2025-12084 | XML DoS | python | 22/12/2025 | `<3.13.12` | Fix released in `3.12.13` — backported patch included in the `v3.12.13` release (see [v3.12.13](https://github.com/python/cpython/commits/v3.12.13) and commit [9c9dda6](https://github.com/python/cpython/commit/9c9dda6625a2a90d2a06c657eee021d6be19842d)). Grype DB still shows this as vulnerable; waiting for DB update. |
| CVE-2025-13836 | HTTP Response Handling (http.client) | python | 22/12/2025 | `<3.13.12` | Fix released in `3.12.13` — backported patch included in the `v3.12.13` release (see [v3.12.13](https://github.com/python/cpython/commits/v3.12.13) and commit [14b1fdb](https://github.com/python/cpython/commit/14b1fdb0a94b96f86fc7b86671ea9582b8676628)). Grype DB still shows this as vulnerable; waiting for DB update. |
| CVE-2026-0865 | HTTP Header Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15282 | CRLF Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2026-0672 | Cookie Header Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15366 | Command Injection (imaplib) | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15367 | Command Injection (poplib) | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-11468 | Email Header Folding Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-12781 | Base64 Decoding Behavior / Data Integrity | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2026-1299 | Email Header Injection (BytesGenerator) | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-6075 | Env Var Pattern Processing | python | 18/02/2026 | `<3.13.10` | Fixed in `3.13.10` - Limited exposure as only exploitable when parsing untrusted env var patterns with `os.path.expandvars()` Pending fix propagation to `3.12` releases. |
| CVE-2025-13837 | Plist parsing | python | 18/02/2026 | `<3.13.10` | Fixed in `3.13.10`; backported to `3.12.13` (see [v3.12.13](https://github.com/python/cpython/commits/v3.12.13) and commit [c8a5f34](https://github.com/python/cpython/commit/c8a5f3435c342964e0a432cc9fb448b7dbecd1ba)). Grype DB still shows this as vulnerable; waiting for DB update. |
| CVE-2026-2297 | Legacy .pyc validation hook bypass | python | 04/03/2026 | `<3.15` | Legacy `*.pyc` validation hook bypass - Pending fix propagation to `<3.15` releases. |
| CVE-2026-3644 | Cookie Input Validation Bypass | python | 26/03/2026 | `<3.14.3` | Pending fix release to `<3.14.3` releases. |
| CVE-2026-4224 | XML Parser Stackoverflow | python | 26/03/2026 | `<3.14.3` | Pending fix release to `<3.14.3` releases. Only affects deeply nested XML content models |
| CVE-2026-4519 | URL corruption | python | 26/03/2026 | `<3.14.3` | Patched in all version branches - Pending fix release to `<3.14.3` releases. |
