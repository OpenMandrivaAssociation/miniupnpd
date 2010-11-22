%define rel 0
Summary:	The UPNP & NAT-PMP implementation
Name:		miniupnpd
Version:	1.4.20100511
Release:	%mkrel %rel
License:	GPL
Group:		Applications/Internet
Source:		%{name}-%{version}.tar.gz
Buildroot:	/tmp/%{name}-%{version}-root
Prefix:		/usr
BuildPrereq:	iptables-devel iptables-iptc-devel
Requires:	iptables

Source1:	miniupnpd.init.d.script
Patch0:		Makefile.linux.patch

%description
The miniUPnP daemon is an UPnP IGD (internet gateway device)
which provide NAT traversal services to any UPnP enabled client on
the network.
See http://www.upnp.org/ for more details on UPnP.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

%install
PREFIX=%{buildroot} make -f Makefile.linux config.h
sed '/#define ENABLE_LEASEFILE/ c\#define ENABLE_LEASEFILE' config.h > config.h.new
mv -f config.h.new config.h
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

%changelog
* Mon Nov 22 2010 Ostroukhov Zamir <zamir@mandriva.com> - 1.4.20100511
   - Fixed makefile for mandriva 2010.1