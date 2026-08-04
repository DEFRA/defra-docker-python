# Vulnerability scanning configuration and ignored vulnerabilities
[Anchore Grype](https://github.com/anchore/grype/) and [Aqua Trivy](https://www.aquasec.com/products/trivy/) are configured to report vulnerabilities that are of medium severity or higher. 

## OS / base image issues
The following OS / base image issues have been added to the policies exclusion list:
| CVE ID | Type | Component | Date Added | Reason |
|------------------------|------|-----------|------|--------|
| CVE-2025-14104 | Buffer overread | util-linux | 19/12/2025 | Fixed in Debian testing (forky) but backport held up by glibc upgrade requirement - Fix might only be possible in next Debian stable release. |
| CVE-2025-6141 | Stack-based Buffer Overflow | ncurses (libncursesw6, libtinfo6, ncurses-base, ncurses-bin) | 16/02/2026 | Fixed in Debian testing (forky) but backport held up by glibc upgrade requirement - Fix might only be possible in next Debian stable release. |
| CVE-2026-27171 | CPU Consumption / DoS | zlib1g | 26/02/2026 | Fixed in zlib 1.3.2. Awaiting release of Debian package with zlib 1.3.2 - fix might only be possible in next Debian stable release. |
| CVE-2025-69720 | Buffer overflow | ncurses (libncursesw6, libtinfo6, ncurses-base, ncurses-bin) | 26/03/2026 | Patch for ncurses release - waiting for Debian to release updated package - fix might only be possible in next Debian stable release. |
| CVE-2026-5704 | Hidden File Injection | tar | 07/04/2026 | Can be mitigated by not extracting untrusted tar files with `tar` - only a risk if users are extracting untrusted tar files within the container. |
| CVE-2026-27456 | TOCTOU / Unauthorized file read | util-linux | 07/04/2026 | Not exploitable in this container image. Exploitation requires an `/etc/fstab` entry with `user,loop` options |
| CVE-2026-3184 | Hostname spoofing | util-linux | 12/05/2026 | Waiting for fix in unstable - fix might only be possible in next Debian stable release. |
| CVE-2026-5435 | Out-of-bounds write | libc (libc6, libc-bin) | 12/05/2026 | Waiting for fix in unstable - risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. Issue only exists in deprecated C functions which are unlikely to be used in any Python dependencies. |
| CVE-2026-5450 | Buffer overflow | libc (libc6, libc-bin) | 12/05/2026 | Waiting for fix in unstable - risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2026-5928 | Buffer overread | libc (libc6, libc-bin) | 12/05/2026 | Waiting for fix in unstable - risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. Not possible within standard unicode character sets. |
| CVE-2026-6238 | DNS Verification Bypass | libc (libc6, libc-bin) | 12/05/2026 | Waiting for fix in unstable - risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. Issue only exists in deprecated C functions which are unlikely to be used in any Python dependencies. |
| CVE-2026-42496 | Arbitrary file access | perl | 03/07/2026 | Waiting for fix to be released by perl maintainers |
| CVE-2026-8376 | Buffer overflow | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable |
| CVE-2025-15649 | Denial of Service | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-12087 | Out-of-bounds read | perl | 03/07/2026 | Waiting for fix to be released by perl maintainers |
| CVE-2026-48959 | CPU consumption / DoS | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-48961 | DoS | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable. Vulnerability only exists in bundled CLI which can't be executed without shell access. |
| CVE-2026-7010 | Validation bypass | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-42497 | Arbitrary file access | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-48962 | Arbitrary code execution | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-9538 | Arbitrary code execution | perl | 03/07/2026 | Fix released by perl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-13221 | Regular expression trie overflow | perl | 04/08/2026 | Affects perl versions through 5.43.9; exploitation requires compiling a regex with more than 65,535 fixed-string alternation branches. Not exploitable in this image as shipped (no Perl-executed service, and trigger pattern is highly unlikely). Waiting for fix from Debian stable release. |
| CVE-2026-57432 | Integer overflow | perl | 04/08/2026 | Affects perl versions through 5.43.9; exploitation requires a crafted input to trigger an integer overflow in the regex engine. Not exploitable in this image as shipped (no Perl-executed service, and trigger pattern is highly unlikely). Waiting for fix from Debian stable release. |
| CVE-2026-41992 | Buffer overflow | gzip | 03/07/2026 | Waiting for fix to be released by gzip maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-54370 | Symlink traversal | acl | 03/07/2026 | Fix released by acl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-54369 | Symlink traversal / privilege escalation | acl | 03/07/2026 | Fix released by acl maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-54371 | Symlink traversal | attr | 03/07/2026 | Fix released by attr maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-13595 | Unallocated memory read | util-linux | 03/07/2026 | Fixed in Debian testing (forky) but backport held up by glibc upgrade requirement - Fix might only be possible in next Debian stable release. |
| CVE-2026-42250 | Denial of Service | bzip2 | 03/07/2026 | Waiting for fix to be released by bzip2 maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-41991 | Arbitrary file overwrite | gzip | 03/07/2026 | Fix available upstream (commit 4e6f8b24) - waiting for fix to be released in Debian stable |
| CVE-2026-54411 | Timing discrepancy / Plaintext password recovery | linux-pam (pam) | 03/07/2026 | Only exploitable when pam_userdb is configured with crypt=none - waiting for upstream fix |
| CVE-2026-11822 | Memory corruption / Buffer overflow | sqlite3 | 03/07/2026 | Fixed in sqlite3 3.53.2 - waiting for fix to be released in Debian stable |
| CVE-2026-11824 | Heap-based buffer overflow | sqlite3 | 03/07/2026 | Fixed in sqlite3 3.53.2 - waiting for fix to be released in Debian stable |
| CVE-2011-3374 | GPG Validation | apt | 03/07/2026 | Waiting for fix to be release by apt maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-53615 | Integer overflow | util-linux | 04/08/2026 | Waiting for fix to be released by util-linux maintainers - waiting for fix to be released in Debian stable |
| CVE-2026-50812 | Null pointer reference / Denial of Service | libsqlite3 | 04/08/2026 | Fixed in sqlite3 3.53.2-1 - waiting for fix to be released in Debian stable |
| CVE-2026-50813 | Information disclosure | libsqlite3 | 04/08/2026 | Fixed in sqlite3 3.53.2-1 - waiting for fix to be released in Debian stable - can only be exploited via local access |
| CVE-2026-18477 | Privilege escalation | tar | 04/08/2026 | Waiting for fix to be released by tar maintainers - only exploitable with local access and with a crafted tar file. |
| CVE-2026-18508 | symlink traversal / out-of-bounds write | tar | 04/08/2026 | Waiting for fix to be released by tar maintainers |

### Python issues
The following Python issues have been added to the policies exclusion list:
| CVE ID | Type | Component | Date Added | Affected Versions | Reason |
|--------|------|-----------|------|-------------------|--------|
| CVE-2026-0865 | HTTP Header Injection | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15282 | CRLF Injection | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2026-0672 | Cookie Header Injection | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15366 | Command Injection (imaplib) | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15367 | Command Injection (poplib) | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-11468 | Email Header Folding Injection | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-12781 | Base64 Decoding Behavior / Data Integrity | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2026-1299 | Email Header Injection (BytesGenerator) | python | 16/02/2026 | `<3.15` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-13837 | Plist parsing | python | 18/02/2026 | `<3.13` | Fixed in `3.13.10`; backported to `3.12.13` (see [v3.12.13](https://github.com/python/cpython/commits/v3.12.13) and commit [c8a5f34](https://github.com/python/cpython/commit/c8a5f3435c342964e0a432cc9fb448b7dbecd1ba)). Grype DB still shows this as vulnerable; waiting for DB update. |
| CVE-2026-2297 | Legacy .pyc validation hook bypass | python | 04/03/2026 | `<3.15` | Legacy `*.pyc` validation hook bypass - Pending fix propagation to `<3.15` releases. |
| CVE-2026-3644 | Cookie Input Validation Bypass | python | 26/03/2026 | `<3.14` | Pending fix release to `<3.14.3` releases. |
| CVE-2026-4224 | XML Parser Stackoverflow | python | 26/03/2026 | `<3.14` | Pending fix release to `<3.14.3` releases. Only affects deeply nested XML content models |
| CVE-2026-4519 | URL corruption | python | 26/03/2026 | `<3.14` | Additional CVE raised CCVE-2026-4786 - previous fixes did not fully address the issue. Pending fix release to `<3.14.3` releases. |
| CVE-2026-3298 | Boundary Check Bypass | python | 26/03/2026 | `<3.14` | Patched for 3.13 and 3.14 - Pending patch and fix release to `<3.14.3` releases. Only impacts Windows platforms. |
| CVE-2026-1502 | HTTP special char injection | python | 26/03/2026 | `<3.14` | Patched in all version branches - Pending fix release to `<3.14.3` releases. |
| CVE-2026-4786 | URL corruption | python | 12/05/2026 | `<3.14` | Additional CVE raised to address remaining URL corruption issue - previous fixes did not fully address the issue. Pending fix release to `<3.14.5` releases. |
| CVE-2026-6100 | Arbitrary code execution | python | 12/05/2026 | `<3.14.5` | Fix included in `3.14.5` release (see commit [48c3c7f](https://github.com/python/cpython/commit/48c3c7fb730e447ae1d8d2dec8f4a8b145687567)). Grype DB still shows this as vulnerable; waiting for DB update. Awaiting fix release to `3.13` and `3.12`. |
| CVE-2026-3446 | base64 decode failure | python | 12/05/2026 | `<3.13` | Fixed in `3.13.13` - Pending fix release to `3.12` releases. Only exploitable when parsing untrusted base64 data with `base64.b64decode()`. Use `validate=True` to mitigate in the meantime. |
| CVE-2026-11940 | Arbitrary file access | python | 12/05/2026 | `<3.15` | Fixed in upstream branches with the exception of `3.12` - Pending inclusion of fix in `3.12`, `3.13` and `3.14` releases. Only exploitable if uncompressing untrusted tar files with `tarfile` modules. |
| CVE-2026-11972 | Exponential archive parsing | python | 12/05/2026 | `<3.15` | Fixed in upstream branches with the exception of `3.12` - Pending inclusion of fix in `3.12`, `3.13` and `3.14` releases. Only exploitable if opening tar archives using streaming mode |
| CVE-2026-12003 | Installation path traversal | python | 12/05/2026 | `<3.15` | Doesn't impact this image - issue only impacts the Windows installer. Fixed in upstream branches with the exception of `3.12` - Pending inclusion of fix in `3.12`, `3.13` and `3.14` releases. |
| CVE-2026-0864 | CRLF injection | python | 12/05/2026 | `<3.15` | Fixed in upstream branches with the exception of `3.12` - Pending inclusion of fix in `3.12`, `3.13` and `3.14` releases. |
| CVE-2026-6019 | HTML / Script Injection (`Morsel.js_output()`) | python | 03/07/2026 | `<3.13.14` | Fixed in `3.13.14`, `3.14.5rc1`, `3.15.0b1`. No `3.12` backport available yet — pending fix release to `3.12`. |
| CVE-2026-8328 | SSRF (`ftplib.ftpcp()` PASV bypass) | python | 03/07/2026 | `<3.12.14` | Patch committed to `3.12` branch (see [3.12] [PR #149795](https://github.com/python/cpython/pull/149795), commit [c887044](https://github.com/python/cpython/commit/c88704431ea3248ca769384c13856330976fac1d)) — awaiting `3.12.14` release. |
| CVE-2026-7774 | Path Traversal (`tarfile.data_filter` bypass) | python | 03/07/2026 | `<3.12.14` | Patch committed to `3.12` branch (see [3.12] [PR #149556](https://github.com/python/cpython/pull/149556), commit [0d28f5e](https://github.com/python/cpython/commit/0d28f5e46e151718972dfabd91205444d0037b6d)) — awaiting `3.12.14` release. |
| CVE-2026-3276 | CPU Consumption / DoS (`unicodedata.normalize()`) | python | 03/07/2026 | `<3.13.14` | Fixed in `3.13.14`, `3.14.6`, `3.15.0b2`. `3.12` backport PR open ([cpython#150843](https://github.com/python/cpython/pull/150843)) — pending merge and release. |
| CVE-2026-9669 | Stack-based Buffer Overflow (`bz2.BZ2Decompressor` reuse after error) | python | 03/07/2026 | `<3.13.14` | Fixed in `3.13.14`, `3.14.6`, `3.15.0b3`. `3.12` backport PR open ([cpython#151057](https://github.com/python/cpython/pull/151057)) — pending merge and release. |
| CVE-2026-7210 | Hash Flooding / Insufficient Entropy (`xml.parsers.expat`, `xml.etree.ElementTree`) | python | 03/07/2026 | `<3.13.14` | Fixed in `3.13.14`, `3.14.6`, `3.15.0b2`. `3.12` backport blocked pending [cpython#151401](https://github.com/python/cpython/pull/151401) — awaiting fix in `3.12`. |

### pip vendored dependency issues
The following issues originate from copies of dependencies bundled inside pip's own `pip/_vendor` directory rather than the top-level installed packages (which are already pinned to fixed versions in the [Dockerfile](Dockerfile)). They cannot be resolved with `pip install --upgrade` and require a new pip release that updates its vendored copies.

| CVE ID | Type | Component | Date Added | Affected Versions | Reason |
|--------|------|-----------|------|-------------------|--------|
| GHSA-6v7p-g79w-8964 | Out-of-bounds read / crash on Unpacker reuse | pip (`pip/_vendor/msgpack`) | 04/08/2026 | `pip<=26.2` | msgpack 1.1.2 is bundled inside pip's own vendored dependencies (pip 26.2 is the latest release) and used only internally by pip's HTTP cache. The top-level `msgpack` package is already pinned to the fixed `1.2.1` release. Waiting for pip to update its vendored copy. |
| CVE-2025-47273 | Path Traversal Vulnerability in setuptools PackageIndex | pip (`pip/_vendor/vendor.txt`) | 04/08/2026 | `pip<=26.2` | setuptools 70.3.0 is referenced inside pip's own vendored dependency manifest (pip 26.2 is the latest release). The top-level `setuptools` package is already pinned to the fixed `83.0.0` release. Waiting for pip to update its vendored reference. |
| CVE-2026-59890 | MANIFEST.in exclusion bypass in sdist via Unicode normalization collision (NFC/NFD) | pip (`pip/_vendor/vendor.txt`) | 04/08/2026 | `pip<=26.2` | setuptools 70.3.0 is referenced inside pip's own vendored dependency manifest (pip 26.2 is the latest release). The top-level `setuptools` package is already pinned to the fixed `83.0.0` release. Waiting for pip to update its vendored reference. |
