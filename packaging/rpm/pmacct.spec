Name: pmacct
Version: %{__version}
Release: %{__release}%{?dist}
Summary: Accounting and aggregation toolsuite for IPv4 and IPv6

License: GPLv2+
Group: Applications/Engineering
URL: https://github.com/redBorder/pmacct
Source0: %{name}-%{version}.tar.gz

Requires: bash redborder-common redborder-rubyrvm bash-completion bash-completion-extras
BuildRequires: gcc
BuildRequires: make
BuildRequires: libpcap-devel
BuildRequires: libstdc++-static
BuildRequires: pkgconfig
BuildRequires: pkgconfig(geoip)
BuildRequires: pkgconfig(jansson)
BuildRequires: systemd
BuildRequires: librdkafka
BuildRequires: librdkafka-devel
BuildRequires: libtool

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
pmacct is a small set of passive network monitoring tools to measure, account,
classify and aggregate IPv4 and IPv6 traffic; a pluggable and flexible
architecture allows to store the collected traffic data into memory tables or
SQL (MySQL, SQLite, PostgreSQL) databases. pmacct supports fully customizable
historical data breakdown, flow sampling, filtering and tagging, recovery
actions, and triggers. Libpcap, sFlow v2/v4/v5 and NetFlow v1/v5/v7/v8/v9 are
supported, both unicast and multicast. Also, a client program makes it easy to
export data to tools like RRDtool, GNUPlot, Net-SNMP, MRTG, and Cacti.

%prep
%setup -qn %{name}-%{version}
# fix permissions
chmod -x sql/pmacct-*

%build
export CFLAGS="%{optflags} -Wno-return-type"
./autogen.sh
%configure \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --sbindir=%{_sbindir} \
    --enable-l2 \
    --enable-ipv6 \
    --enable-v4-mapped \
    --enable-geoip \
    --enable-jansson \
    --enable-64bit \
    --enable-threads \
    --enable-kafka


make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

# install sample configuration files
install -Dp examples/nfacctd-sql_v2.conf.example %{buildroot}/%{_sysconfdir}/%{name}/nfacctd.conf
install -Dp examples/pmacctd-sql_v2.conf.example %{buildroot}/%{_sysconfdir}/%{name}/pmacctd.conf

# install systemd units
install -d %{buildroot}/%{_unitdir} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
install packaging/rpm/*.service %{buildroot}/%{_unitdir}
install packaging/rpm/sysconfig_nfacctd %{buildroot}/%{_sysconfdir}/sysconfig/%{name}/nfacctd
install packaging/rpm/sysconfig_pmacctd %{buildroot}/%{_sysconfdir}/sysconfig/%{name}/pmacctd
install packaging/rpm/sysconfig_sfacctd %{buildroot}/%{_sysconfdir}/sysconfig/%{name}/sfacctd
install packaging/rpm/sysconfig_pmbgpd %{buildroot}/%{_sysconfdir}/sysconfig/%{name}/pmbgpd
install packaging/rpm/sysconfig_pmbmpd %{buildroot}/%{_sysconfdir}/sysconfig/%{name}/pmbmpd
install packaging/rpm/sysconfig_pmtelemetryd %{buildroot}/%{_sysconfdir}/sysconfig/%{name}/pmtelemetryd

%post
%systemd_post nfacctd.service
%systemd_post pmacctd.service
%systemd_post sfacctd.service

%preun
%systemd_preun nfacctd.service
%systemd_preun pmacctd.service
%systemd_preun sfacctd.service

%postun
%systemd_postun_with_restart nfacctd.service
%systemd_postun_with_restart pmacctd.service
%systemd_postun_with_restart sfacctd.service

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog CONFIG-KEYS COPYING FAQS TOOLS UPGRADE
%doc docs examples sql
%{_bindir}/pmacct
#
%{_sbindir}/nfacctd
%{_sbindir}/pmacctd
%{_sbindir}/sfacctd
%{_sbindir}/pmbgpd
%{_sbindir}/pmbmpd
%{_sbindir}/pmtelemetryd
#
%{_unitdir}/nfacctd.service
%{_unitdir}/pmacctd.service
%{_unitdir}/sfacctd.service
%{_unitdir}/pmbgpd.service
%{_unitdir}/pmbmpd.service
%{_unitdir}/pmtelemetryd.service
#
%{_sysconfdir}/sysconfig/%{name}/nfacctd
%{_sysconfdir}/sysconfig/%{name}/pmacctd
%{_sysconfdir}/sysconfig/%{name}/sfacctd
%{_sysconfdir}/sysconfig/%{name}/pmbgpd
%{_sysconfdir}/sysconfig/%{name}/pmbmpd
%{_sysconfdir}/sysconfig/%{name}/pmtelemetryd
#
%dir %{_sysconfdir}/pmacct
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/pmacct/nfacctd.conf
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/pmacct/pmacctd.conf

%changelog
* Thu Feb 8 2018 Juan J. Prieto <jjprieto@redborder.com> - 1.7.0-1
- redborder spec version

