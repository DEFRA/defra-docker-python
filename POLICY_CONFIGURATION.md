# Vulnerability scanning configuration and ignored vulnerabilities
[Anchore Grype](https://github.com/anchore/grype/) and [Aqua Trivy](https://www.aquasec.com/products/trivy/) are configured to report vulnerabilities that are of medium severity or higher. 

## Known issues
The following issues have been added to the policies exclusion list:
| CVE ID        | Type                | Component    | Date       | Reason                                                                       |
|---------------|---------------------|--------------|------------|------------------------------------------------------------------------------|
| CVE-2025-7709 | Integer Overflow    | libsqlite3-0 | 07/11/2025 | Fixed in Debian 14 (testing) - Waiting for fix to propagate down to Debian 13 (stable) |
| CVE-2025-8291 | Improper Validation | python       | 07/11/2025 | Waiting for 3.13 patch. Security fix pushed for 3.12                       |
