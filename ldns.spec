#
# Conditional build:
%bcond_without	static_libs # don't build static libraries
#
Summary:	ldns - a library with the aim to simplify DNS programing in C
Summary(pl.UTF-8):	ldns - biblioteka mająca na celu uproszczenie programowania DNS w C
Name:		ldns
Version:	1.6.10
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://www.nlnetlabs.nl/downloads/ldns/%{name}-%{version}.tar.gz
# Source0-md5:	fadf8e38fbd2d3434a2c46097d9932d5
URL:		http://www.nlnetlabs.nl/ldns/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ldns is a library with the aim to simplify DNS programing in C. It is
heavily based upon the Net::DNS module from perl.

%description -l pl.UTF-8
ldns jest biblioteka mającą na celu uproszczenie programowania w C.
Jest w dużym stopniu oparta na module Perla Net::DNS.

%package devel
Summary:	Header files for ldns library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ldns
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--enable-static=%{?with_static_libs:yes}%{!?with_static_libs:no}
%{__make}
%{__make} doc

# change symlinks into .so redirects
cd doc/man/man3
for f in `find . -type l`; do
	d=`readlink $f`
	rm -f $f
	echo ".so $d" > $f
done

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog README
%attr(755,root,root) %{_libdir}/libldns.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libldns.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ldns-config
%doc doc/{*.html,dns-lib-implementations,function_manpages,ldns_manpages,CodingStyle}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_mandir}/man3/*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
