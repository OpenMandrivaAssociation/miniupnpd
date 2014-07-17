Summary:	The UPNP & NAT-PMP implementation
Name:		miniupnpd
Version:	1.8.20140523
Release:	1
License:	GPLv2
Group:		System/Servers
URL:		http://miniupnp.free.fr
Source0:	http://miniupnp.free.fr/files/download.php?file=/%{name}-%{version}.tar.gz
BuildRequires:	iptables-ip4tc-devel
BuildRequires:	iptables-devel
BuildRequires:	pkgconfig(libiptc)
BuildRequires:	pkgconfig(libnetfilter_conntrack)
Requires:	iptables
Source1:	miniupnpd.service

%description
The miniUPnP daemon is an UPnP IGD (internet gateway device)
which provide NAT traversal services to any UPnP enabled client on
the network.
See http://www.upnp.org/ for more details on UPnP.

%prep
%setup -q

%build
    mv Makefile.linux Makefile
    sed -i \
        -e "s#^CFLAGS = .*-D#CPPFLAGS += -I/usr/include -D#" \
        -e '/^CFLAGS :=/s/CFLAGS/CPPFLAGS/g' \
        -e "s/CFLAGS += -ansi/#CFLAGS += -ansi/g" \
        -e "s/LIBS = -liptc/LIBS = -lip4tc/g" \
        -e 's/genuuid||//' \
        Makefile || die
    sed -i \
        -e 's/\(strncpy(\([->a-z.]\+\), "[a-zA-Z]\+", \)IPT_FUNCTION_MAXNAMELEN);/\1sizeof(\2));/' \
        netfilter/iptcrdr.c || die

    make config.h

    sed -i \
        -e 's/\/\*#define ENABLE_LEASEFILE\*\//#define ENABLE_LEASEFILE/g' \
        config.h || die

%make CC=gcc

%install
mkdir -p %{buildroot}%{_mandir}/man8/

make install  PREFIX="%{buildroot}" STRIP="true"
rm -f %{buildroot}%{_sysconfdir}/init.d/miniupnpd
rm -f %{buildroot}%{_sysconfdir}/miniupnpd/miniupnpd.conf~
install -D -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%files
%{_sbindir}/miniupnpd
%{_unitdir}/miniupnpd*
%doc %{_mandir}/man*/*
%config(noreplace) %{_sysconfdir}/miniupnpd/*
%doc README Changelog.txt
