%define         tag     RELEASE.2020-03-14T02-21-58Z
%define         subver  %(echo %{tag} | sed -e 's/[^0-9]//g')
# git fetch https://github.com/minio/minio.git refs/tags/RELEASE.2020-03-14T02-21-58Z
# git rev-list -n 1 FETCH_HEAD
%define         commitid        2e9fed1a14e5640219c3fc5ef51b30b937f42c0c
Summary:        Cloud Storage Server.
Name:           minio
Version:        0.0.%{subver}
Release:        1%{?dist}
Vendor:         MinIO, Inc.
License:        Apache v2.0
Group:          Applications/File
Source0:        https://github.com/minio/minio/archive/%{tag}.tar.gz
URL:            https://www.min.io/
BuildRequires:  golang >= 1.7
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

## Disable debug packages.
%define         debug_package %{nil}

## Go related tags.
%define         gobuild(o:) go build -ldflags "${LDFLAGS:-}" %{?**};
%define         gopath          %{_libdir}/golang
%define         import_path     github.com/minio/minio

%description
MinIO is an object storage server released under Apache License v2.0.
It is compatible with Amazon S3 cloud storage service. It is best
suited for storing unstructured data such as photos, videos, log
files, backups and container / VM images. Size of an object can
range from a few KBs to a maximum of 5TiB.

%prep
%autosetup -p1 -n minio-%{tag}
rm go.mod

install -d src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}

%build
export GOPATH=$(pwd)

# setup flags like 'go run buildscripts/gen-ldflags.go' would do
tag=%{tag}
version=${tag#RELEASE.}
commitid=%{commitid}
scommitid=$(echo $commitid | cut -c1-12)
prefix=%{import_path}/cmd

export LDFLAGS="
-X $prefix.Version=$version
-X $prefix.ReleaseTag=$tag
-X $prefix.CommitID=$commitid
-X $prefix.ShortCommitID=$scommitid
"

GO111MODULE=on CGO_ENABLED=0 \
go build -v -o %{name} -tags kqueue -ldflags "$LDFLAGS" %{import_path}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -p %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md README_zh_CN.md
%attr(755,root,root) %{_sbindir}/minio
