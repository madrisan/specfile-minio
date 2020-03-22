%global tag RELEASE.2020-03-14T01-23-37Z
%global subver %(echo %{tag} | sed -e 's/[^0-9]//g')

# git fetch https://github.com/minio/mc.git refs/tags/RELEASE.2020-03-14T01-23-37Z
# git rev-list -n 1 FETCH_HEAD
%global commitid 5b5d65a142c5562e412de022a3114e83378096a5

## Disable debug packages.
%global debug_package %{nil}

## Go related tags.
%global gobuild(o:) go build -ldflags "${LDFLAGS:-}" %{?**};
%global gopath %{_libdir}/golang
%global import_path github.com/minio/mc

Summary:        MinIO Client
Name:           minio-mc
Version:        0.0.%{subver}
Release:        1%{?dist}
Vendor:         MinIO, Inc.
License:        Apache v2.0
Group:          Applications/File
Source0:        https://github.com/minio/mc/archive/%{tag}.tar.gz
URL:            https://www.min.io/
BuildRequires:  golang >= 1.7
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MinIO Client (mc) provides a modern alternative to UNIX commands like
ls, cat, cp, mirror, diff, find etc.
It supports filesystems and Amazon S3 compatible cloud storage service
(AWS Signature v2 and v4).

%prep
%autosetup -p1 -n mc-%{tag}
rm -f go.mod

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

LDFLAGS="\
-X $prefix.Version=$version
-X $prefix.ReleaseTag=$tag
-X $prefix.CommitID=$commitid
-X $prefix.ShortCommitID=$scommitid"

GO111MODULE=on CGO_ENABLED=0 \
go build -v -o %{name} -tags kqueue -ldflags "$LDFLAGS" %{import_path}

%install
install -d %{buildroot}%{_bindir}
install -p %{name} %{buildroot}%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md README_zh_CN.md
%attr(755,root,root) %{_bindir}/minio-mc

%changelog
* Fri Mar 20 2020 Davide Madrisan <davide.madrisan@gmail.com> - 0.0.20200314T012337Z-1
- First build
