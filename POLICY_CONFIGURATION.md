# Vulnerability scanning configuration and ignored vulnerabilities
[Anchore Grype](https://github.com/anchore/grype/) and [Aqua Trivy](https://www.aquasec.com/products/trivy/) are configured to report vulnerabilities that are of medium severity or higher. 

## Known issues
The following issues have been added to the policies exclusion list:
| CVE ID         | Type               | Component | Date       | Reason                                                                                                   |
|----------------|--------------------|-----------|------------|----------------------------------------------------------------------------------------------------------|
| CVE-2025-4516  | Unicode escaping   | python    | 09/06/2025 | Affects 3.12 and 1.13 - Waiting for fix to propagate down from 3.14 (prerelease). Workaround possible using try-except rather than error=handler with "bytes.decode" and "unicode_escape". |
| CVE-2025-4947  | TLS                | curl      | 09/06/2025 | Waiting for fix - Only exploitable if using WolfSSL as TLS library.                                      |
| CVE-2025-5025  | TLS                | curl      | 09/06/2025 | Waiting for fix - Only exploitable if using WolfSSL as TLS library.                                      |
| CVE-2025-4802  | ACE                | libc6     | 09/06/2025 | Fixed in Debian 13 (trixie 2.41-8) - Limited exposure as only exploitable locally and production image has no shell.     |
| CVE-2025-5399  | DOS                | curl      | 10/06/2025 | Fixed in Debian 13 (trixie 8.14.1-1) - Waiting for fixed package to make it into stable - Will review in a month. |
