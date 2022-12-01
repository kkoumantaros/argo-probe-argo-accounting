Name:		argo-probe-argo-accounting
Release:	1%{?dist}
Summary:	Monitoring scripts that check accounting service status
License:	GPLv3+

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}
AutoReqProv:    no
Requires:       python-requests

%description
An ARGO probe to check service availabilty of accounting

%prep
%setup -q

%define _unpackaged_files_terminate_build 0

%install
install -d %{buildroot}/%{_libexecdir}/argo/probes/argo-accounting
install -m 755 check_status.py %{buildroot}/%{_libexecdir}/argo/probes/argo-accounting/check_status.py

%files
%dir /%{_libexecdir}/argo
%dir /%{_libexecdir}/argo/probes/
%dir /%{_libexecdir}/argo/probes/argo-accounting

%attr(0755,root,root) /%{_libexecdir}/argo/probes/argo-accounting/check_status.py

%changelog
* Tue Oct 4 2022 Kostis Triantafyllakis <kostastriantaf@gmail.com> - 0.1.2-1
- ARGO-3840 Fix wrong exit status code
* Tue May 24 2022 Katarina Zailac <katarina.zailac@gmail.com> - 0.1.1-1
- ARGO-3840 Fix wrong exit status code
* Mon May 16 2022 Katarina Zailac <katarina.zailac@gmail.com> - 0.1.0-1
- Initial version of the package.
