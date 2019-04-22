#
# Conditional build:
%bcond_with	python		# build with python support
#
Summary:	Common software API for various radio hardware
Name:		gr-osmosdr
Version:	0.1.4
Release:	7
License:	GPL v3+
Group:		Applications/Engineering
URL:		http://sdr.osmocom.org/trac/wiki/GrOsmoSDR
Source0:	http://git.osmocom.org/gr-osmosdr/snapshot/%{name}-%{version}.tar.xz
# Source0-md5:	da9733eee05e1409beb1c606c2db4521
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gnuradio-devel >= 3.7.3
BuildRequires:	graphviz
BuildRequires:	log4cpp-devel
BuildRequires:	librtlsdr-devel
%{?with_python:BuildRequires:	python-devel}
%{?with_python:BuildRequires:	swig}
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
%setup -q

%build
install -d build
cd build
%cmake \
	%{!?with_python:-DENABLE_PYTHON=OFF} \
	-DENABLE_DOXYGEN=on \
	-DGR_PKG_DOC_DIR=%{_docdir}/%{name} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf doc-inst
mv $RPM_BUILD_ROOT%{_docdir}/%{name} doc-inst

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING doc-inst/*
%if %{with python}
%attr(755,root,root) %{_bindir}/osmocom_fft
%attr(755,root,root) %{_bindir}/osmocom_siggen
%attr(755,root,root) %{_bindir}/osmocom_siggen_nogui
%attr(755,root,root) %{_bindir}/osmocom_spectrum_sense
%dir %{py_sitedir}/osmosdr
%attr(755,root,root) %{py_sitedir}/osmosdr/*.so
%{py_sitedir}/osmosdr/*.py*
%{_datadir}/gnuradio/grc/blocks/osmosdr_sink.xml
%{_datadir}/gnuradio/grc/blocks/osmosdr_source.xml
%{_datadir}/gnuradio/grc/blocks/rtlsdr_source.xml
%endif
%attr(755,root,root) %{_libdir}/libgnuradio-osmosdr-*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libgnuradio-osmosdr-*.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/osmosdr
%attr(755,root,root) %{_libdir}/libgnuradio-osmosdr.so
%attr(755,root,root) %{_libdir}/libgnuradio-osmosdr-*.so
%{_pkgconfigdir}/gnuradio-osmosdr.pc
