%define snap	20140111
Summary:	Common software API for various radio hardware
Name:		gr-osmosdr
Version:	0.1.1
Release:	0.%{snap}.1
License:	GPL v3+
Group:		Applications/Engineering
URL:		http://sdr.osmocom.org/trac/wiki/GrOsmoSDR
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	15fbc7e472ee40669c083c1715c7bc58
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gnuradio-devel
BuildRequires:	graphviz
BuildRequires:	python-devel
BuildRequires:	rtl-sdr-devel
BuildRequires:	swig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Primarily gr-osmosdr supports the OsmoSDR hardware, but it also offers
a wrapper functionality for FunCube Dongle, Ettus UHD and rtl-sdr
radios. By using gr-osmosdr source you can take advantage of a common
software api in your application(s) independent of the underlying
radio hardware.

%package devel
Summary:	Development files for gr-osmosdr
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for gr-osmosdr.

%prep
%setup -q -n %{name}

%build
install -d build
cd build
%cmake \
	-DENABLE_DOXYGEN=on \
	-DGR_PKG_DOC_DIR=%{_docdir}/%{name} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*.so.*
%{py_sitedir}/*
%{_datadir}/gnuradio/grc/blocks/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/osmosdr
%{_libdir}/*.so
%{_pkgconfigdir}/*.pc
