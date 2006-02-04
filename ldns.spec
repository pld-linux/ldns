#
# Conditional build:
%bcond_without	static_libs # don't build static libraries
#
Summary:	ldns - a library with the aim to simplify DNS programing in C
Summary(pl):	ldns - biblioteka maj±ca na celu uproszczenie programowania DNS w C
Name:		ldns
Version:	1.0.1
Release:	0.1
License:	GPL
Group:		Libraries
Source0:	http://www.nlnetlabs.nl/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	39210ff3bb2673d57e024f7908d31be5
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

%description -l pl
ldns jest biblioteka maj±c± na celu uproszczenie programowania w C.
Jest w du¿ym stopniu oparta na module Perla Net::DNS.

%package devel
Summary:	Header files for ldns library
Summary(pl):	Pliki nag³ówkowe biblioteki ldns
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header files for ldns library.

%description devel -l pl
Pliki nag³ówkowe biblioteki ldns.

%package static
Summary:	Static ldns library
Summary(pl):	Statyczna biblioteka ldns
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ldns library.

%description static -l pl
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
%doc Changelog ProgrammingPhilosophy README ROADMAP TODO
%attr(755,root,root) %{_libdir}/lib*-*.*.*.so

%files devel
%defattr(644,root,root,755)
%doc doc/{*.html,LDNS_API,overview,PacketTypes,dns-lib-implementations,function_manpages,ldns_manpages,CodingStyle,html}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
%{_mandir}/man3/*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
