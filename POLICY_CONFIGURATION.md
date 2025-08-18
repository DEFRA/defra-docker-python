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
| CVE-2025-6069  | HTML Parsing       | python    | 18/08/2025 | Affects 3.12 and < 3.13.6 - DoS vulnerability when processing malformed HTML. Waiting for updated Python base image. |
| CVE-2025-8058  | ACE                | libc6     | 18/08/2025 | Fixed in Debian 13 (trixie 2.41-11) - Waiting for updated Debian image. |
