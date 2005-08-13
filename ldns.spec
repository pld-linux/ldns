#
# Conditional build:
%bcond_without	static_libs # don't build static libraries
#
Summary:	ldns is a library with the aim to simplify DNS programing in C
Summary(pl):	ldns jest bibliotek± maj±c± na celu uproszczenie programowania DNS w C
Name:		ldns
Version:	0.70
Release:	0.1
License:	GPL
Group:		Libraries
Source0:	http://www.nlnetlabs.nl/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	d94b88a090aaba2e6b79d02b4eb4752f
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.nlnetlabs.nl/ldns/
BuildRequires:	autoconf
BuildRequires:	libtool
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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	%{!?with_static_libs:--enable-static=no}
%{__make}
%{__make} doc

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
%doc Changelog COMPILE DEADJOE ProgrammingPhilosophy README ROADMAP TODO
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/%{name}
# don't remove `.gz' (because you'll get plenty of dead symlinks)
%{_mandir}/man3/*.gz

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
