# Docker Python

> [!IMPORTANT]
> Python should **ONLY** be used for creating backend services related to AI or data science.

This repository contains Python parent Docker image source code for Defra.

The following table lists the versions of python available, and the parent Python image they are based on:

| Python version  | Development parent image       | Production parent image       |
|-----------------|--------------------------------|-------------------------------|
| 3.13.3          | 3.13.3-slim-bookworm           | gcr.io/distroless/cc-debian12 |
| 3.12.6          | 3.12.6-slim-bookworm           | gcr.io/distroless/cc-debian12 |

Two parent images are created for each version:

- defra-python
- defra-python-development

It is recommended that services use [multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build) to produce production and development images, each extending the appropriate parent, from a single Dockerfile.

By default, the following packages are installed in the parent images:
- `uv`
- `pydebug` - for the development image only

Examples have been provided in the [examples](./examples) directory to demonstrate how parent images can be extended.

The following example Dockerfiles have been provided:
- [uv](./examples/uv.Dockerfile) - Example of using `uv` to manage dependencies and run a Python service.

## Supported Python versions

Services should use the latest stable version of Python.

As such, the maintained parent images will align to stable Python version (starting with Python 3.12) that have not reached end-of-life (EOL).

## Internal CA certificates

The image includes the certificate for the internal [CA](https://en.wikipedia.org/wiki/Certificate_authority) so that traffic can traverse the network without encountering issues.

## Versioning

Images should be tagged according to the Dockerfile version and the version of Python on which the image is based. For example, for Dockerfile version `1.0.0` based on Python `3.12.10`, the built image would be tagged `1.0.0-python3.12.10`.

Any new features or changes to supported Python or Debian versions will be published as `minor` version updates.  Any breaking changes to dependencies or how images can be consumed will be published as `major` updates.

## CI/CD

On commit GitHub Actions will build both `python` and `python-development` images for the Python versions listed in the [image-matrix.json](image-matrix.json) file, and perform a vulnerability scan as described below.

In addition a commit to the master branch will push the images to the [defradigital](https://hub.docker.com/u/defradigital) organisation in Docker Hub using the version tag specified in the [JOB.env](JOB.env) file. This version tag is expected to be manually updated on each release.

In addition to the version, the images will also be tagged with the contents of the `tags` array from [image-matrix.json](image-matrix.json) when pushed to Docker Hub.

## Image vulnerability scanning

A GitHub Action runs a nightly scan of the images published to Docker using [Anchore Grype](https://github.com/anchore/grype/) and [Aqua Trivy](https://www.aquasec.com/products/trivy/). The latest images for each supported Python version are scanned.

New images are also scanned before release on any push to a branch.

This ensures Defra services that use the parent images are starting from a known secure foundation, and can limit patching to only newly added libraries.

For more details see [Image Scanning](IMAGE_SCANNING.md)

## Building images locally

To build the images locally, run:
```
docker build --no-cache --target <target> .
```
(where `<target>` is either `development` or `production`).

This will build an image using the default `BASE_VERSION` as set in the [Dockerfile](Dockerfile).

## Licence

THIS INFORMATION IS LICENSED UNDER THE CONDITIONS OF THE OPEN GOVERNMENT LICENCE found at:

<http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3>

The following attribution statement MUST be cited in your products and applications when using this information.

> Contains public sector information licensed under the Open Government license v3

### About the licence

The Open Government Licence (OGL) v3.0 was developed by the The National Archives to enable information providers in the public sector to license the use and re-use of their information under a common open licence.

It is designed to encourage use and re-use of information freely and flexibly, with only a few conditions.
