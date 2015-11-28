#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	python		# Python modules
#
Summary:	ldns - a library with the aim to simplify DNS programing in C
Summary(pl.UTF-8):	ldns - biblioteka mająca na celu uproszczenie programowania DNS w C
Name:		ldns
Version:	1.6.17
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://www.nlnetlabs.nl/downloads/ldns/%{name}-%{version}.tar.gz
# Source0-md5:	a79423bcc4129e6d59b616b1cae11e5e
URL:		http://www.nlnetlabs.nl/ldns/
BuildRequires:	autoconf >= 2.56
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 1.0.0
%if %{with python}
BuildRequires:	python-devel >= 1:2.4.0
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig-python
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
Requires:	openssl-devel >= 1.0.0

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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
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
%attr(755,root,root) %ghost %{_libdir}/libldns.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/{*.html,dns-lib-implementations,function_manpages,ldns_manpages,CodingStyle}
%attr(755,root,root) %{_bindir}/ldns-config
%attr(755,root,root) %{_libdir}/libldns.so
%{_libdir}/libldns.la
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
