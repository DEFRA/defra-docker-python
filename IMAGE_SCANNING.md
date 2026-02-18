
#  Image vulnerability scanning

The repository runs a vulnerability scan of the latest Docker hub parent image nightly, and the 'work in progress' image on push to a branch via the GitHub actions workflows [nightly-scan.yml](.github/workflows/nightly-scan.yml) and [scan-on-commit.yml](.github/workflows/scan-on-commit.yml) respectively.

Scheduled actions only run on the `master` repository branch so will run once, regardless of the number of branches.

Both workflows read settings from the file [JOB.env](JOB.env) to ensure the same Python, Debian, and Defra versions are used during the image scan.

Scans are performed by [Anchore Grype](https://github.com/anchore/grype) using the configuration file [.grype.yaml](.grype.yaml) via the [Github Anchore Scan Action](https://github.com/anchore/scan-action).

The scan is configured to fail on vulnerabilities of `medium` or higher.

Details on the configuration file and exclusions can be found in [POLICY_CONFIGURATION.md](POLICY_CONFIGURATION.md).

## Addressing vulnerabilities

If the Grype scan finds a vulnerability the scan will fail and a report will be stored as an artifact against the failed GitHub [Action](https://github.com/DEFRA/defra-docker-python/actions).

There are two solutions to address an image vulnerability: patch the Dockerfile to upgrade the vulnerable library, or add the vulnerability to the exclusion list if deemed not exploitable.

### Adding a vulnerability to the exclusion list

Generally speaking the only vulnerabilities that are excluded are binaries used by the `npm` command line tool, as these are not exploitable in a running container, and are complicated to update.

The scan output and the artifacts on the GitHub Action log will provide details of the type and severity of the vulnerability, along with the CVE ID of the vulnerability.

To exclude the vulnerability add an item to the `.grype.yaml`'s `ignore` list. Full details on formatting the YAML can be found in the `grype` documenation under [Specifying Matches to Ignore](https://github.com/anchore/grype#specifying-matches-to-ignore).

The preferred option is to specify the CVE ID, along with the type of vulnerability and the package name itself. This makes it easier to tie the reported vulnerability to the file.

The example below shows the yaml to exclude the `CVE-2021-3807` vulnerability for the `npm` package `ansi-regex`, as well as the `npm` package itself as `CVE-2021-43616`:
```
ignore:
  - vulnerability: GHSA-93q8-gq69-wqmw
  - vulnerability: CVE-2021-3807
    package:
      type: npm
      name: ansi-regex
  - vulnerability:  CVE-2021-43616
    package:
      type: npm
      name: npm
```

Any exclusions should be recorded in the [POLICY_CONFIGURATION.md](POLICY_CONFIGURATION.md) with an explanation of why they are considered non-exploitable.

When updating an image to a newer version it is important to remove all existing ignores and only re-add ones that have still not been fixed to ensure the `.grype.yaml` file does not become cluttered with fixed vulnerabilities.

### Backporting packages from future Debian releases

In some cases, a vulnerability may be fixed in a future Debian release (such as Debian testing) but not yet available in the stable release used by the base image. If the vulnerability poses a significant risk and cannot be mitigated through application-level controls, it may be possible to backport the fixed package from the future release.

**Important:** Not all packages can be easily backported. Before attempting a backport, assess whether:
- The package has minimal dependencies that are satisfied by the current stable release
- The package does not require significant system-level changes (e.g., glibc upgrades carry high stability risks)
- The build process is straightforward and well-documented
- The risk of introducing instability through the backport is acceptable compared to the vulnerability risk
- The vulnerability risk is significant enough to justify the additional build time, particularly for multi-architecture builds (ARM64 compilation can take significantly longer than x86_64, which impacts CI/CD pipeline duration)

Here is an example of how to backport a package from Debian testing in the Dockerfile using a multi-stage build:

```dockerfile
FROM python:${BASE_VERSION} AS builder

RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        dpkg-dev \
        debian-keyring \
        devscripts \
        equivs \
    && rm -rf /var/lib/apt/lists/*

RUN printf "Types: deb-src\nURIs: http://deb.debian.org/debian\nSuites: testing\nComponents: main\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg\n" > /etc/apt/sources.list.d/testing-src.sources \
    && apt update

RUN mkdir -p /tmp/backport-builds/sqlite3 \
    && cd /tmp/backport-builds/sqlite3 \
    && apt source sqlite3=3.46.1-9/testing \
    && cd sqlite3-* \
    && mk-build-deps --install --tool='apt-get -y' --remove \
    && dch --bpo "CVE-2025-7709: backport to patch sqlite3 vulnerability" \
    && dpkg-buildpackage --build=binary --unsigned-changes

FROM python:${BASE_VERSION} AS production

# Install backported sqlite3 to patch CVE-2025-7709
RUN --mount=from=builder,type=bind,target=/tmp/backport-builds/sqlite3 \
    find /tmp/backport-builds/sqlite3 -name "lemon_*.deb" ! -name "*-dbgsym*" -exec apt install -y {} + \
    && find /tmp/backport-builds/sqlite3 -name "libsqlite3-*.deb" ! -name "*-dbgsym*" -exec apt install -y {} + \
    && find /tmp/backport-builds/sqlite3 -name "sqlite3*.deb" ! -name "*-dbgsym*" -exec apt install -y {} +
```

This approach uses a multi-stage build where:
1. A `builder` stage compiles the backported package from Debian testing source
2. The built `.deb` packages are installed in the `production` stage using a bind mount
3. The CVE is documented in the changelog entry using `dch --bpo`

Any backported packages should be documented in [POLICY_CONFIGURATION.md](POLICY_CONFIGURATION.md) with details of the vulnerability being addressed and the source of the backport.

## Running an Anchore Grype scan locally

Install `grype` on your machine as per the instructions at https://github.com/anchore/grype.

First build the production image locally with a known tag as described in the [README.md](README.md), i.e.
```
docker build --no-cache --tag defra-python:latest --target=production .
```

Scan the tagged image, i.e. `defra-python:latest`, using  the `grype` configuration file `.grype.yaml`. 
```
grype defra-python:latest --fail-on medium
```
or
```
grype defra-python:latest --fail-on medium -o json > report.json
```
**Note:** the configuration file is in the default location so does not need specifying on the command line.

Full documentation on `grype`` be found at https://github.com/anchore/grype

## Upgrading Anchore Grype

Grype updates are frequent. To update grype on a *nix system run the update `curl` at  https://github.com/anchore/grype as super user, i.e.
```
sudo -i
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
exit
```
