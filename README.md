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

    sudo dnf install -y rpm-build golang

### Build instructions

    mkdir ~/rpmbuild/{SPECS,SOURCES}
    
    cd ~/rpmbuild/SOURCES
    git clone --depth 1 https://github.com/madrisan/specfile-minio
    wget https://github.com/minio/minio/archive/RELEASE.2020-03-14T02-21-58Z.tar.gz
    mv minio.spec ../SPECS/
    
    cd ~/rpmbuild/SPECS
    rpmbuild -ba minio.spec
