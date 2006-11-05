%define		_rel	0.2
Summary:	Aethera - Email and PIM application
Summary(pl):	Aethera - aplikacja e-mail i zarz±dcy informacji osobistej (PIM)
Name:		aethera
Version:	1.2.1
Release:	050331.%{_rel}
License:	GPL
Group:		X11/Applications
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}-libs.patch
Patch1:		%{name}-includes.patch
Patch2:		%{name}-install.patch
Patch3:		%{name}-fpic.patch
# Source0-md5:	f3efd064b5e9884bd7adf49bf763e213
URL:		http://www.thekompany.com/projects/aethera/
BuildRequires:	korelib-devel
BuildRequires:	qt-devel
#Requires: thekompany-support
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aethera is a pim application, i.e. it handles all kinds of personal
information: email, contacts, notes, tasks, todos, journals.

%description -l pl
Aethera jest aplikacj± zarz±dcy informacji osobistej (PIM). Obs³uguje
wszystkie rodzaje informacji osobistych: e-mail, kontakty, notatki,
zadania, sprawy do za³atwienia, dzienniki.

%package devel
Summary:	Header files for Aethera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Aethera library.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%ifarch %{x8664}
%patch3 -p1
%endif

mkdir -p include/aethera
ln -sf ../../aethera/libs/clientskel/clientrmi.h include/aethera
ln -sf ../../aethera/libs/clientskel/vfsmodule.h include/aethera

%build
export QTDIR=/usr
export QMAKE_STRIP=:

# Use the new libraries in building process
export LD_LIBRARY_PATH=$dir/lib:$LD_LIBRARY_PATH
dir=$(pwd)

# Compile tkcBase
cd tkcbase
cat <<EOF > defines.pri
TKCBASE_LIB=%{_libdir}
TKCBASE_INCLUDE=%{_includedir}/tkcbase
CONFIG += release thread
EOF
qmake desktop.pro
%{__make}

# Compile tkcSSL
cd ../tkcssl
cat <<EOF > defines.pri
TKCSSL_LIB=%{_libdir}
TKCSSL_INCLUDE=%{_includedir}/tkcssl
INCLUDEPATH += $dir/tkcbase
DEPENDPATH += $dir/tkcbase
CONFIG += release thread
EOF
qmake tkcssl.pro
%{__make}

# Compile webdav
cd ../webdav
cat <<EOF > defines.pri
WEBDAV_LIB=%{_libdir}
WEBDAV_INCLUDE=%{_includedir}/tkcbase
CONFIG += release thread
EOF
qmake webdav.pro
%{__make}

# Compile Aethera
cd ../aethera
cat <<EOF > defines.pri
AETHERA_DIR=%{_libdir}/aethera
AETHERA_BIN=%{_bindir}
AETHERA_LIB=%{_libdir}
AETHERA_INCLUDE=%{_includedir}/aethera
TINO_LIB=%{_libdir}
TINO_INCLUDE=%{_includedir}/tino
INCLUDEPATH += $dir/include
INCLUDEPATH += $dir/tkcbase
DEPENDPATH += $dir/tkcbase
INCLUDEPATH += $dir/tkcssl
DEPENDPATH += $dir/tkcssl

CONFIG += qt warn_on release thread
EOF

qmake aethera.pro
%{__make}

# Compile KOrganizer plugin
cd ../koplugin
cat <<EOF > defines.pri
AETHERA_DIR = %{_libdir}/aethera

INCLUDEPATH += $dir/include
INCLUDEPATH += $dir/tkcbase
DEPENDPATH += $dir/tkcbase

INCLUDEPATH += $dir/tkcssl
DEPENDPATH += $dir/tkcssl

INCLUDEPATH += $dir/aethera/libs
DEPENDPATH += $dir/aethera/libs

INCLUDEPATH += $dir/aethera/libs/aethera
DEPENDPATH += $dir/aethera/libs/aethera

INCLUDEPATH += $direbdav/webdav
DEPENDPATH += $dir/webdav/webdav

INCLUDEPATH += $dir/aethera/libs/clientskel
DEPENDPATH += $dir/aethera/libs/clientskel

INCLUDEPATH += $dir/include/aethera/libs/plugins/kommailplugin
DEPENDPATH += $dir/include/aethera/libs/plugins/kommailplugin

INCLUDEPATH += $dir/include/aethera/libs/plugins/komcontactsplugin
DEPENDPATH += $dir/include/aethera/libs/plugins/komcontactsplugin

INCLUDEPATH += $dir/include/tino
DEPENDPATH += $dir/include/tino

CONFIG += qt warn_on release thread
DEFINES += AETHERA_KOLAB
EOF

qmake KOPlugin.pro
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/aethera

export QTDIR=/usr
%{__make} -C tkcbase install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C tkcssl install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C webdav install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C aethera install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C koplugin install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

# x86 binary
rm $RPM_BUILD_ROOT%{_libdir}/aethera/bin/sox
# unneccessary wrappers
rm $RPM_BUILD_ROOT%{_libdir}/aethera/bin/aethera_sound
rm $RPM_BUILD_ROOT%{_prefix}/local/bin/aethera

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p	/sbin/ldconfig
%postun	-p	/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aethera
%attr(755,root,root) %{_libdir}/libaethera.so.1.0.1
%attr(755,root,root) %{_libdir}/libfilebrowser.so.1.0.0
%attr(755,root,root) %{_libdir}/libtino.so.1.0.0
%attr(755,root,root) %{_libdir}/libtkcbase.so.1.0.0
%attr(755,root,root) %{_libdir}/libtkcssl.so.1.0.0
%dir %{_libdir}/aethera
%dir %{_libdir}/aethera/plugins
%attr(755,root,root) %{_libdir}/aethera/plugins/libhomeplugin.so.1.0.0
%attr(755,root,root) %{_libdir}/aethera/plugins/libkomcontactsplugin.so.1.0.0
%attr(755,root,root) %{_libdir}/aethera/plugins/libkommailplugin.so.1.0.0
%attr(755,root,root) %{_libdir}/aethera/plugins/libkomnotesplugin.so.1.0.0
%attr(755,root,root) %{_libdir}/aethera/plugins/libkorganizer.so.1.0.0
%attr(755,root,root) %{_libdir}/aethera/plugins/libmailimport.so.1.0.0
%{_libdir}/aethera/help
%{_libdir}/aethera/pics
%{_libdir}/aethera/sound
%{_libdir}/aethera/data
%dir %{_libdir}/aethera/i18n
%lang(de) %{_libdir}/aethera/i18n/aethera_de.qm
%lang(de) %{_libdir}/aethera/i18n/aethera_de.ts
%lang(de) %{_libdir}/aethera/i18n/koplugin_de.ts
%lang(en) %{_libdir}/aethera/i18n/aethera_en.ts
%lang(en) %{_libdir}/aethera/i18n/koplugin_en.ts
%lang(fr) %{_libdir}/aethera/i18n/aethera_fr.qm
%lang(fr) %{_libdir}/aethera/i18n/aethera_fr.ts
%lang(fr) %{_libdir}/aethera/i18n/koplugin_fr.qm
%lang(fr) %{_libdir}/aethera/i18n/koplugin_fr.ts
%lang(pt) %{_libdir}/aethera/i18n/aethera_pt.qm
%lang(pt) %{_libdir}/aethera/i18n/aethera_pt.ts
%lang(pt) %{_libdir}/aethera/i18n/koplugin_pt.qm
%lang(pt) %{_libdir}/aethera/i18n/koplugin_pt.ts
%lang(pt) %{_libdir}/aethera/i18n/qt_pt.qm
%lang(pt) %{_libdir}/aethera/i18n/qt_pt.ts
%lang(ru) %{_libdir}/aethera/i18n/aethera_ru.qm
%lang(ru) %{_libdir}/aethera/i18n/aethera_ru.ts
%{_desktopdir}/aethera.desktop
%{_iconsdir}/hicolor/*/apps/aethera.png
%{_pixmapsdir}/*.png

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtkwidgets.a
%{_libdir}/libwebdav.a
%{_includedir}/aethera
%{_includedir}/tino
%{_includedir}/tkcbase
%{_includedir}/tkcssl
