%define rel 0
Summary:	The UPNP & NAT-PMP implementation
Name:		miniupnpd
Version:	1.5.20110302
Release:	%mkrel %rel
License:	GPL
Group:		System/Servers
URL:		http://miniupnp.free.fr
Source:		http://miniupnp.free.fr/files/download.php?file=/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	iptables-devel iptables-iptc-devel
Requires:	iptables

Source1:	miniupnpd.init.d.script

%description
The miniUPnP daemon is an UPnP IGD (internet gateway device)
which provide NAT traversal services to any UPnP enabled client on
the network.
See http://www.upnp.org/ for more details on UPnP.

%prep
%setup -q -n %{name}-%{version}

%build
%make -f Makefile.linux config.h

%install
PREFIX=%{buildroot} make -f Makefile.linux install
rm -f %{buildroot}%{_sysconfdir}/init.d/miniupnpd
rm -f %{buildroot}%{_sysconfdir}/miniupnpd/miniupnpd.conf~
install -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
mkdir -p %{buildroot}%{_mandir}/man1/
install -D -m 755 miniupnpd.1 %{buildroot}%{_mandir}/man1/

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{_sbindir}/miniupnpd
%{_initrddir}/miniupnpd
%doc %{_mandir}/man*/*
%config(noreplace) %{_sysconfdir}/miniupnpd/*
%doc README Changelog.txt
