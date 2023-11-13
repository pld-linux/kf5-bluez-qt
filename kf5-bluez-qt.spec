#
# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	5.112
%define		qtver		5.15.2
%define		kfname		bluez-qt
Summary:	Qt wrapper for Bluez 5 DBus API
Name:		kf5-%{kfname}
Version:	5.112.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	24213adcbeb177c7e923e2ca3d19d99a
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt wrapper for Bluez 5 DBus API.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKF5BluezQt.so.*.*.*
%ghost %{_libdir}/libKF5BluezQt.so.6
/lib/udev/rules.d/61-kde-bluetooth-rfkill.rules
%dir %{_libdir}/qt5/qml/org/kde/bluezqt
%{_libdir}/qt5/qml/org/kde/bluezqt/qmldir
%{_libdir}/qt5/qml/org/kde/bluezqt/DevicesModel.qml
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/bluezqt/libbluezqtextensionplugin.so
%{_datadir}/qlogging-categories5/bluezqt.categories
%{_datadir}/qlogging-categories5/bluezqt.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5BluezQt.so
%{_includedir}/KF5/BluezQt
%{_libdir}/cmake/KF5BluezQt
%{_libdir}/qt5/mkspecs/modules/qt_BluezQt.pri
%{_pkgconfigdir}/KF5BluezQt.pc
