%define		_rel	0.1
Summary:	Aethera - Email and PIM application
Summary(pl):	Aethera - aplikacja e-mail i zarz�dcy informacji osobistej (PIM)
Name:		aethera
Version:	1.2.1
Release:	050331.%{_rel}
License:	GPL
Group:		X11/Applications
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}-libs.patch
Patch1:		%{name}-includes.patch
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
Aethera jest aplikacj� zarz�dcy informacji osobistej (PIM). Obs�uguje
wszystkie rodzaje informacji osobistych: e-mail, kontakty, notatki,
zadania, sprawy do za�atwienia, dzienniki.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export QTDIR=/usr
# Use the new libraries in building process
export LD_LIBRARY_PATH=$dir/lib:$LD_LIBRARY_PATH
dir=$(pwd)


mkdir -p include/aethera
ln -sf ../../aethera/libs/clientskel/clientrmi.h include/aethera
ln -sf ../../aethera/libs/clientskel/vfsmodule.h include/aethera

# Compile tkcBase
cd tkcbase
echo > defines.pri
echo "TKCBASE_LIB="$dir/lib >> defines.pri
echo "TKCBASE_INCLUDE="$dir/tkcbase >> defines.pri
echo "CONFIG += release thread" >> defines.pri
qmake desktop.pro
%{__make}

# Compile tkcSSL
cd ../tkcssl
echo > defines.pri
echo "TKCSSL_LIB="$dir/lib >> defines.pri
echo "TKCSSL_INCLUDE="$dir/tkcssl >> defines.pri
echo "INCLUDEPATH += "$dir/tkcbase >> defines.pri
echo "DEPENDPATH += "$dir/tkcbase >> defines.pri
echo "CONFIG += release thread" >> defines.pri
qmake tkcssl.pro
%{__make}

# Compile webdav
cd ../webdav
echo > defines.pri
echo "WEBDAV_LIB="$dir/lib/ >> defines.pri
echo "WEBDAV_INCLUDE="$dir/tkcbase >> defines.pri
echo "CONFIG += release thread" >> defines.pri
qmake webdav.pro
%{__make}

# Compile Aethera
cd ../aethera
echo > defines.pri
echo "AETHERA_DIR="$dir/lib/theKompany/Aethera >> defines.pri
echo "AETHERA_BIN="$dir/bin >> defines.pri
echo "AETHERA_LIB="$dir/tkcbase >> defines.pri
echo "AETHERA_INCLUDE="$dir/include/aethera/ >> defines.pri
echo "AETHERA_INCLUDES="$dir/include/aethera/ >> defines.pri
echo "TINO_LIB="$dir/lib/lib >> defines.pri
echo "TINO_INCLUDE="$dir/include/tino >> defines.pri
echo "INCLUDEPATH += "$dir/include >> defines.pri
echo "INCLUDEPATH += "$dir/tkcbase >> defines.pri
echo "DEPENDPATH += "$dir/tkcbase >> defines.pri
echo "INCLUDEPATH += "$dir/tkcssl >> defines.pri
echo "DEPENDPATH += "$dir/tkcssl >> defines.pri

echo "CONFIG += qt warn_on release thread" >> defines.pri

qmake aethera.pro
%{__make}

# Compile KOrganizer plugin
cd ../koplugin
echo > defines.pri
echo "AETHERA_DIR="$dir/lib >> defines.pri
echo "INCLUDEPATH += "$dir/include >> defines.pri
echo "INCLUDEPATH += "$dir/tkcbase >> defines.pri
echo "DEPENDPATH += "$dir/tkcbase >> defines.pri
echo "INCLUDEPATH += "$dir/tkcssl >> defines.pri
echo "DEPENDPATH += "$dir/tkcssl >> defines.pri
echo "INCLUDEPATH += "$dir/aethera/libs >> defines.pri
echo "DEPENDPATH += "$dir/aethera/libs >> defines.pri
echo "INCLUDEPATH += "$dir/aethera/libs/aethera >> defines.pri
echo "DEPENDPATH += "$dir/aethera/libs/aethera >> defines.pri
echo "INCLUDEPATH += "$direbdav/webdav >> defines.pri
echo "DEPENDPATH += "$dir/webdav/webdav >> defines.pri
echo "INCLUDEPATH += "$dir/aethera/libs/clientskel >> defines.pri
echo "DEPENDPATH += "$dir/aethera/libs/clientskel >> defines.pri

echo "INCLUDEPATH += "$dir/include/aethera/libs/plugins/kommailplugin >> defines.pri
echo "DEPENDPATH += "$dir/include/aethera/libs/plugins/kommailplugin >> defines.pri
echo "INCLUDEPATH += "$dir/include/aethera/libs/plugins/komcontactsplugin >> defines.pri
echo "DEPENDPATH += "$dir/include/aethera/libs/plugins/komcontactsplugin >> defines.pri
echo "INCLUDEPATH += "$dir/include/tino >> defines.pri
echo "DEPENDPATH += "$dir/include/tino >> defines.pri

echo "CONFIG += qt warn_on release thread" >> defines.pri
echo "DEFINES += AETHERA_KOLAB" >> defines.pri

qmake KOPlugin.pro
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
export QTDIR=/usr
%{__make} -C tkcbase install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C tkcssl install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C webdav install \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C aethera install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
