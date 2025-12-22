# Vulnerability scanning configuration and ignored vulnerabilities
[Anchore Grype](https://github.com/anchore/grype/) and [Aqua Trivy](https://www.aquasec.com/products/trivy/) are configured to report vulnerabilities that are of medium severity or higher. 

## Known issues
The following issues have been added to the policies exclusion list:
| CVE ID        | Type                | Component    | Date       | Reason                                                                       |
|---------------|---------------------|--------------|------------|------------------------------------------------------------------------------|
| CVE-2025-7709 | Integer Overflow    | libsqlite3-0 | 07/11/2025 | Fixed in Debian 14 (testing) - Waiting for fix to propagate down to Debian 13 (stable) |
| CVE-2025-14104 | Buffer Overread | util-linux | 19/12/2025 | Waiting for fix to be included in Debian stable release |
| CVE-2025-12084 | XML DoS | python | 22/12/2025 | Fixed in python 3.13, waiting for fix to propagate to 3.12 security release. Only impacts heavily nested XML files. |
| CVE-2025-13836 | HTTP Response Handling | python | 22/12/2025 | Fixed in python 3.13, waiting for fix to propagate to 3.12 security release. |
