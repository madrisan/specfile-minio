# Specfile for MinIO server

![Release Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![License](https://img.shields.io/badge/License-MPL--2.0-blue.svg)](https://spdx.org/licenses/MPL-2.0.html)

[![MinIO](https://raw.githubusercontent.com/minio/minio/master/.github/logo.svg?sanitize=true)](https://min.io)

MinIO is a open source, S3 compatible, enterprise hardened and high performance distributed object storage system.
* Official Site: https://min.io
* GitHub Site: https://github.com/minio/minio

This repository contains a *specfile* that you can use to build MinIO from the sources.

## Usage

### Pre-Requiments

    sudo dnf install -y rpm-build golang git
    
Note that git version 2 is required (tested with version 2.25.1).

### Build instructions

#### MinIO server

    mkdir -p ~/rpmbuild/{SPECS,SOURCES}
    
    for f in minio.conf minio.service; do
      curl -# https://raw.githubusercontent.com/madrisan/specfile-minio/master/$f \
        -o ~/rpmbuild/SOURCES/$f
    done
    curl -# https://raw.githubusercontent.com/madrisan/specfile-minio/master/minio.spec \
        -o ~/rpmbuild/SPECS/minio.spec
    
    curl -# -L https://github.com/minio/minio/archive/RELEASE.2020-03-14T02-21-58Z.tar.gz \
        -o ~/rpmbuild/SOURCES/RELEASE.2020-03-14T02-21-58Z.tar.gz
    
    rpmbuild -ba ~/rpmbuild/SPECS/minio.spec

#### Minio client (mc)

    mkdir -p ~/rpmbuild/{SPECS,SOURCES}
    
    curl -# https://raw.githubusercontent.com/madrisan/specfile-minio/master/mc.spec \
        -o ~/rpmbuild/SPECS/mc.spec
    
    curl -# -L https://github.com/minio/minio/archive/RELEASE.2020-03-14T01-23-37Z.tar.gz \
        -o ~/rpmbuild/SOURCES/RELEASE.2020-03-14T01-23-37Z.tar.gz
    
    rpmbuild -ba ~/rpmbuild/SPECS/mc.spec

### Installation

The resulting .rpm packages can be installed with `rpm` of `dnf`.

Before starting the *systemd* service `minio.service` you need to customize the configuration file `/etc/sysconfig/minio`.
The volumes managed by MinIO must be configured in the variable `MINIO_VOLUMES`.
You can optionally pass some extra options at service startup by modifying the variable `MINIO_OPTIONS`.

To improve the security you should also create the file `/etc/systemd/system/minio.service.d/environment.conf`owned by *root*, with a file mode `0640`, declaring the following two secrets:
```
[Service]
Environment=MINIO_ACCESS_KEY=ADD_A_KEY_HERE
Environment=MINIO_SECRET_KEY=ADD_A_SECRET_HERE
```

Here's a simple way to generate a random character sequence:
```
cat /dev/urandom | tr -dc '0-9a-zA-Z-._' | head -c 24; echo
```

### Security

See the official documentation pages:
 * https://docs.min.io/docs/minio-server-configuration-guide.html
 * https://docs.min.io/docs/how-to-secure-access-to-minio-server-with-tls.html
