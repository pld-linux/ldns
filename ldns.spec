# NOTE: included perl-DNS-LDNS module (--with-p5-dns-ldns) is older than in separate spec (0.61 vs 0.63)
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	python		# Python modules
#
Summary:	ldns - a library with the aim to simplify DNS programing in C
Summary(pl.UTF-8):	ldns - biblioteka mająca na celu uproszczenie programowania DNS w C
Name:		ldns
Version:	1.8.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.nlnetlabs.nl/downloads/ldns/%{name}-%{version}.tar.gz
# Source0-md5:	429b93dacb2d6ecc5ed63788b14c38e6
Patch0:		python-install.patch
Patch1:		%{name}-link.patch
URL:		http://www.nlnetlabs.nl/ldns/
BuildRequires:	autoconf >= 2.56
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libtool >= 2:2
BuildRequires:	openssl-devel >= 1.1.0
%if %{with python}
BuildRequires:	python-devel >= 1:2.4.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig-python >= 2.0.4
%endif
Requires:	openssl >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ldns is a library with the aim to simplify DNS programing in C. It is
heavily based upon the Net::DNS module from perl.

%description -l pl.UTF-8
ldns jest biblioteka mającą na celu uproszczenie programowania
związanego z usługą DNS w C. Jest w dużym stopniu oparta na module
Perla Net::DNS.

%package devel
Summary:	Header files for ldns library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ldns
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel >= 1.1.0

%description devel
Header files for ldns library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ldns.

%package static
Summary:	Static ldns library
Summary(pl.UTF-8):	Statyczna biblioteka ldns
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ldns library.

%description static -l pl.UTF-8
Statyczna biblioteka ldns.

%package -n python-ldns
Summary:	Python interface do ldns library
Summary(pl.UTF-8):	Pythonowy interfejs do biblioteki ldns
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-ldns
Python interface do ldns library.

%description -n python-ldns -l pl.UTF-8
Pythonowy interfejs do biblioteki ldns.

%package -n drill
Summary:	drill - tool to get all sorts of information out of the DNS(SEC)
Summary(pl.UTF-8):	drill - narzędzie do pobierania dowolnych informacji z DNS(SEC)
Group:		Applications/Network
Requires:	%{name} = %{version}-%{release}

%description -n drill
drill is a tool to get all sorts of information out of the DNS. It is
specifically designed to be used with DNSSEC.

%description -n drill -l pl.UTF-8
drill to narzędzie do pobierania dowolnych informacji z DNS. Jest
zaprojektowane szczególnie z myślą o użyciu z DNSSEC.

%package tools
Summary:	Example tools for ldns
Summary(pl.UTF-8):	Przykładowe narzędzie wykorzystujące ldns
Group:		Applications/Network
Requires:	%{name} = %{version}-%{release}

%description tools
These tools are examples of ldns usage. They are not meant for
production systems and will not be supported as such.

%description tools -l pl.UTF-8
Te narzędzia są przykładami użycia biblioteki ldns.
Nie są przeznaczone do produkcyjnego użycia i jako takie
nie będa wspierane.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--with-examples \
	--enable-gost-anyway \
	--enable-static%{!?with_static_libs:=no} \
	--with-drill \
	%{?with_python:--with-pyldns}
%{__make}
%{__make} doc

# change symlinks into .so redirects
cd doc/man/man3
for f in `find . -type l`; do
	d=`readlink $f`
	%{__rm} $f
	echo ".so $d" > $f
done

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libldns.la

%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_ldns.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_ldns.a
%endif
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog LICENSE README
%attr(755,root,root) %{_libdir}/libldns.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libldns.so.3

%files devel
%defattr(644,root,root,755)
%doc doc/{*.html,dns-lib-implementations,function_manpages,ldns_manpages,CodingStyle}
%attr(755,root,root) %{_bindir}/ldns-config
%attr(755,root,root) %{_libdir}/libldns.so
%{_pkgconfigdir}/ldns.pc
%{_includedir}/%{name}
%{_mandir}/man1/ldns-config.1*
%{_mandir}/man3/ldns_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libldns.a
%endif

%if %{with python}
%files -n python-ldns
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_ldns.so*
%{py_sitedir}/ldns.py[co]
%{py_sitedir}/ldnsx.py[co]
%endif

%files -n drill
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/drill
%{_mandir}/man1/drill.1*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ldns-chaos
%attr(755,root,root) %{_bindir}/ldns-compare-zones
%attr(755,root,root) %{_bindir}/ldns-dane
%attr(755,root,root) %{_bindir}/ldns-dpa
%attr(755,root,root) %{_bindir}/ldns-gen-zone
%attr(755,root,root) %{_bindir}/ldns-key2ds
%attr(755,root,root) %{_bindir}/ldns-keyfetcher
%attr(755,root,root) %{_bindir}/ldns-keygen
%attr(755,root,root) %{_bindir}/ldns-mx
%attr(755,root,root) %{_bindir}/ldns-notify
%attr(755,root,root) %{_bindir}/ldns-nsec3-hash
%attr(755,root,root) %{_bindir}/ldns-read-zone
%attr(755,root,root) %{_bindir}/ldns-resolver
%attr(755,root,root) %{_bindir}/ldns-revoke
%attr(755,root,root) %{_bindir}/ldns-rrsig
%attr(755,root,root) %{_bindir}/ldns-signzone
%attr(755,root,root) %{_bindir}/ldns-test-edns
%attr(755,root,root) %{_bindir}/ldns-testns
%attr(755,root,root) %{_bindir}/ldns-update
%attr(755,root,root) %{_bindir}/ldns-verify-zone
%attr(755,root,root) %{_bindir}/ldns-version
%attr(755,root,root) %{_bindir}/ldns-walk
%attr(755,root,root) %{_bindir}/ldns-zcat
%attr(755,root,root) %{_bindir}/ldns-zsplit
%attr(755,root,root) %{_bindir}/ldnsd
%{_mandir}/man1/ldns-chaos.1*
%{_mandir}/man1/ldns-compare-zones.1*
%{_mandir}/man1/ldns-dane.1*
%{_mandir}/man1/ldns-dpa.1*
%{_mandir}/man1/ldns-gen-zone.1*
%{_mandir}/man1/ldns-key2ds.1*
%{_mandir}/man1/ldns-keyfetcher.1*
%{_mandir}/man1/ldns-keygen.1*
%{_mandir}/man1/ldns-mx.1*
%{_mandir}/man1/ldns-notify.1*
%{_mandir}/man1/ldns-nsec3-hash.1*
%{_mandir}/man1/ldns-read-zone.1*
%{_mandir}/man1/ldns-resolver.1*
%{_mandir}/man1/ldns-revoke.1*
%{_mandir}/man1/ldns-rrsig.1*
%{_mandir}/man1/ldns-signzone.1*
%{_mandir}/man1/ldns-test-edns.1*
%{_mandir}/man1/ldns-testns.1*
%{_mandir}/man1/ldns-update.1*
%{_mandir}/man1/ldns-verify-zone.1*
%{_mandir}/man1/ldns-version.1*
%{_mandir}/man1/ldns-walk.1*
%{_mandir}/man1/ldns-zcat.1*
%{_mandir}/man1/ldns-zsplit.1*
%{_mandir}/man1/ldnsd.1*
