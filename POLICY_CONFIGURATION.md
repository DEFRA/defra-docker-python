# Vulnerability scanning configuration and ignored vulnerabilities
[Anchore Grype](https://github.com/anchore/grype/) and [Aqua Trivy](https://www.aquasec.com/products/trivy/) are configured to report vulnerabilities that are of medium severity or higher. 

## OS / base image issues
The following OS / base image issues have been added to the policies exclusion list:
| CVE ID | Type | Component | Date Added | Reason |
|------------------------|------|-----------|------|--------|
| CVE-2025-7709 | Integer overflow | libsqlite3-0 | 07/11/2025 | Patched by backporting `3.46.1-9` from Debian testing - waiting for fix to propagate to Debian stable release. |
| CVE-2025-14104 | Buffer overread | util-linux | 19/12/2025 | Fixed in Debian testing (forky) but backport held up by glibc upgrade requirement - Fix might only be possible in next Debian stable release. |
| CVE-2025-15281 | Uninitialised memory | glibc (libc-bin, libc-dev-bin, libc6, libc6-dev) | 16/02/2026 | Fixed in Debian testing (forky) but significant system stability risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2026-0915 | Information Leak / Use of Uninitialized Resource | glibc (libc-bin, libc-dev-bin, libc6, libc6-dev) | 16/02/2026 | Fixed in Debian testing (forky) but significant system stability risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2026-0861 | Integer Overflow | glibc (libc-bin, libc-dev-bin, libc6, libc6-dev) | 16/02/2026 | Fixed in Debian testing (forky) but significant system stability risks with backporting / upgrading glibc - fix might only be possible in next Debian stable release. |
| CVE-2025-6141 | Stack-based Buffer Overflow | ncurses (libncursesw6, libtinfo6, ncurses-base, ncurses-bin) | 16/02/2026 | Fixed in Debian testing (forky) but backport held up by glibc upgrade requirement - Fix might only be possible in next Debian stable release. |

### Python issues
The following Python issues have been added to the policies exclusion list:
| CVE ID | Type | Component | Date Added | Affected Versions | Reason |
|--------|------|-----------|------|-------------------|--------|
| CVE-2025-12084 | XML DoS | python | 22/12/2025 | `<3.13.12` | Fixed in `3.13.12` - Only impacts heavily nested XML files. Pending fix propagation to `3.12` releases. |
| CVE-2025-13836 | HTTP Response Handling (http.client) | python | 22/12/2025 | `<3.13.12` | Fixed in `3.13.12` - Pending fix propagation to `3.12` releases. Can be mitigated by setting a max safe read when using `HTTPResponse.read()` |
| CVE-2026-0865 | HTTP Header Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15282 | CRLF Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2026-0672 | Cookie Header Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15366 | Command Injection (imaplib) | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-15367 | Command Injection (poplib) | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-11468 | Email Header Folding Injection | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-12781 | Base64 Decoding Behavior / Data Integrity | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2026-1299 | Email Header Injection (BytesGenerator) | python | 16/02/2026 | `<3.15.0` | Fixed in `3.15.0` - Pending fix propagation to `<3.15.0` releases. |
| CVE-2025-6075 | Env Var Pattern Processing | python | 18/02/2026 | `<3.13.10` | Fixed in `3.13.10` - Limited exposure as only exploitable when parsing untrusted env var patterns with `os.path.expandvars()` Pending fix propagation to `3.12` releases. |
| CVE-2025-13837 | Plist parsing | python | 18/02/2026 | `<3.13.10` | Fixed in `3.13.10` - Only impacts parsing of untrusted plist files. Pending fix propagation to `3.12` releases. |
