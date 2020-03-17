%global tag RELEASE.2020-03-14T02-21-58Z
%global subver %(echo %{tag} | sed -e 's/[^0-9]//g')

# git fetch https://github.com/minio/minio.git refs/tags/RELEASE.2020-03-14T02-21-58Z
# git rev-list -n 1 FETCH_HEAD
%global commitid 2e9fed1a14e5640219c3fc5ef51b30b937f42c0c

%global miniouserhome /var/lib/minio
%global daemon_name %{name}

## Disable debug packages.
%global debug_package %{nil}

## Go related tags.
%global gobuild(o:) go build -ldflags "${LDFLAGS:-}" %{?**};
%global gopath %{_libdir}/golang
%global import_path github.com/minio/minio

Summary:        MinIO Cloud Storage Server
Name:           minio
Version:        0.0.%{subver}
Release:        1%{?dist}
Vendor:         MinIO, Inc.
License:        Apache v2.0
Group:          Applications/File
Source0:        https://github.com/minio/minio/archive/%{tag}.tar.gz
Source1:        minio.service
Source2:        minio.conf
URL:            https://www.min.io/
BuildRequires:  golang >= 1.7
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MinIO is an object storage server released under Apache License v2.0.
It is compatible with Amazon S3 cloud storage service. It is best
suited for storing unstructured data such as photos, videos, log
files, backups and container / VM images. Size of an object can
range from a few KBs to a maximum of 5TiB.

%prep
%autosetup -p1 -n minio-%{tag}
rm -f go.mod

cp %{SOURCE1} %{SOURCE2} .

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
install -d %{buildroot}%{_sbindir}
install -p %{name} %{buildroot}%{_sbindir}

install -D -p -m 0644 minio.service %{buildroot}%{_unitdir}/%{daemon_name}.service
install -D -p -m 0644 minio.conf %{buildroot}%{_sysconfdir}/%{daemon_name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd minio >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g minio -d %{miniouserhome} -s /sbin/nologin \
  -c "MinIO Cloud Storage Server" minio >/dev/null 2>&1 || :
 
%post
%systemd_post %{daemon_name}.service

%preun
%systemd_preun %{daemon_name}.service

%postun
%systemd_postun_with_restart %{daemon_name}.service

%files
%defattr(644,root,root,755)
%doc README.md README_zh_CN.md
%attr(755,root,root) %{_sbindir}/minio
%{_unitdir}/%{daemon_name}.service
%config(noreplace) %{_sysconfdir}/%{daemon_name}

%changelog
* Tue Mar 17 2020 Davide Madrisan <davide.madrisan@gmail.com> - 0.0.20200314022158-1
- Packaging of MinIO based on the specfile found in the git repository
